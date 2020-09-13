import hashlib
import json
import unicodedata

from collections import defaultdict
from html import unescape
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from autoscraper.utils import get_random_str, unique_hashable, unique_stack_list


class AutoScraper(object):
    """
    AutoScraper : A Smart, Automatic, Fast and Lightweight Web Scraper for Python.
    AutoScraper automatically learns a set of rules required to extract the needed content
        from a web page. So the programmer doesn't need to explicitly construct the rules.

    Attributes
    ----------
    stack_list: list
        List of rules learned by AutoScraper

    Methods
    -------
    build() - Learns a set of rules represented as stack_list based on the wanted_list,
        which can be reused for scraping similar elements from other web pages in the future.
    get_result_similar() - Gets similar results based on the previously learned rules.
    get_result_exact() - Gets exact results based on the previously learned rules.
    get_results() - Gets exact and similar results based on the previously learned rules.
    save() - Serializes the stack_list as JSON and saves it to disk.
    load() - De-serializes the JSON representation of the stack_list and loads it back.
    remove_rules() - Removes one or more learned rule[s] from the stack_list.
    keep_rules() - Keeps only the specified learned rules in the stack_list and removes the others.
    """

    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }

    def __init__(self, stack_list=None):
        self.stack_list = stack_list or []

    def save(self, file_path):
        """
        Serializes the stack_list as JSON and saves it to the disk.

        Parameters
        ----------
        file_path: str
            Path of the JSON output

        Returns
        -------
        None
        """

        data = dict(stack_list=self.stack_list)
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def load(self, file_path):
        """
        De-serializes the JSON representation of the stack_list and loads it back.

        Parameters
        ----------
        file_path: str
            Path of the JSON file to load stack_list from.

        Returns
        -------
        None
        """

        with open(file_path, 'r') as f:
            data = json.load(f)

        # for backward compatibility
        if isinstance(data, list):
            self.stack_list = data
            return

        self.stack_list = data['stack_list']

    @classmethod
    def _get_soup(cls, url=None, html=None, request_args=None):
        request_args = request_args or {}

        if html:
            return BeautifulSoup(html, 'lxml')

        headers = dict(cls.request_headers)
        if url:
            headers['Host'] = urlparse(url).netloc

        user_headers = request_args.pop('headers', {})
        headers.update(user_headers)
        html = requests.get(url, headers=headers, **request_args).text
        html = unicodedata.normalize("NFKD", unescape(html))
        
        return BeautifulSoup(html, 'lxml')

    @staticmethod
    def _get_valid_attrs(item):
        return {
            k: v if v != [] else '' for k, v in item.attrs.items() if k in {'class', 'style'}
        }

    @staticmethod
    def _child_has_text(child, text, url):
        child_text = child.getText().strip()
        if text == child_text:
            child.wanted_attr = None
            return True

        for key, value in child.attrs.items():
            if not isinstance(value, str):
                continue

            value = value.strip()
            if text == value:
                child.wanted_attr = key
                return True

            if key in {'href', 'src'}:
                full_url = urljoin(url, value)
                if text == full_url:
                    child.wanted_attr = key
                    child.is_full_url = True
                    return True

        return False

    def _get_children(self, soup, text, url):
        text = text.strip()
        children = reversed(soup.findChildren())
        children = [x for x in children if self._child_has_text(x, text, url)]
        return children

    def build(self, url=None, wanted_list=None, html=None, request_args=None, update=False):
        """
        Automatically constructs a set of rules to scrape the specified target[s] from a web page.
            The rules are represented as stack_list.

        Parameters:
        ----------
        url: str, optional
            URL of the target web page. You should either pass url or html or both.

        wanted_list: list, optional
            A list of needed contents to be scraped.
                AutoScraper learns a set of rules to scrape these targets.

        html: str, optional
            An HTML string can also be passed instead of URL.
                You should either pass url or html or both.

        request_args: dict, optional
            A dictionary used to specify a set of additional request parameters used by requests
                module. You can specify proxy URLs, custom headers etc.

        update: bool, optional, defaults to False
            If True, new learned rules will be added to the previous ones.
            If False, all previously learned rules will be removed.

        Returns:
        --------
        None
        """

        soup = self._get_soup(url=url, html=html, request_args=request_args)

        result_list = []

        if update is False:
            self.stack_list = []

        for wanted in wanted_list:
            children = self._get_children(soup, wanted, url)

            for child in children:
                result, stack = self._get_result_for_child(child, soup, url)
                result_list += result
                self.stack_list.append(stack)

        result_list = unique_hashable(result_list)

        if all(w in result_list for w in wanted_list):
            self.stack_list = unique_stack_list(self.stack_list)
            return result_list

        return None

    @classmethod
    def _build_stack(cls, child, url):
        content = [(child.name, cls._get_valid_attrs(child))]

        parent = child
        while True:
            grand_parent = parent.findParent()
            if not grand_parent:
                break

            children = grand_parent.findAll(parent.name, cls._get_valid_attrs(parent),
                                                         recursive=False)
            for i, c in enumerate(children):
                if c == parent:
                    content.insert(
                        0, (grand_parent.name, cls._get_valid_attrs(grand_parent), i))
                    break

            if grand_parent.name == 'html':
                break

            parent = grand_parent

        wanted_attr = getattr(child, 'wanted_attr', None)
        is_full_url = getattr(child, 'is_full_url', False)
        stack = dict(content=content, wanted_attr=wanted_attr, is_full_url=is_full_url)
        stack['url'] = url if is_full_url else ''
        stack['hash'] = hashlib.sha256(str(stack).encode('utf-8')).hexdigest()
        stack['stack_id'] = 'rule_' + get_random_str(4)
        return stack

    def _get_result_for_child(self, child, soup, url):
        stack = self._build_stack(child, url)
        result = self._get_result_with_stack(stack, soup, url)
        return result, stack

    @staticmethod
    def _fetch_result_from_child(child, wanted_attr, is_full_url, url):
        if wanted_attr is None:
            return child.getText().strip()

        if wanted_attr not in child.attrs:
            return None

        if is_full_url:
            return urljoin(url, child.attrs[wanted_attr])

        return child.attrs[wanted_attr]

    def _get_result_with_stack(self, stack, soup, url):
        parents = [soup]
        for _, item in enumerate(stack['content']):
            children = []
            for parent in parents:
                children += parent.findAll(item[0], item[1], recursive=False)

            parents = children

        wanted_attr = stack['wanted_attr']
        is_full_url = stack['is_full_url']
        result = [self._fetch_result_from_child(i, wanted_attr, is_full_url, url) for i in parents]
        result = [x for x in result if x]
        return result

    def _get_result_with_stack_index_based(self, stack, soup, url):
        p = soup.findChildren(recursive=False)[0]
        stack_content = stack['content']
        for index, item in enumerate(stack_content[:-1]):
            content = stack_content[index + 1]
            p = p.findAll(content[0], content[1], recursive=False)
            if not p:
                return []
            idx = min(len(p) - 1, item[2])
            p = p[idx]

        result = [self._fetch_result_from_child(p, stack['wanted_attr'], stack['is_full_url'], url)]
        result = [x for x in result if x]
        return result

    def _get_result_by_func(self, func, url, html, soup, request_args, grouped):
        if not soup:
            soup = self._get_soup(url=url, html=html, request_args=request_args)

        result_list = []
        grouped_result = defaultdict(list)
        for stack in self.stack_list:
            if not url:
                url = stack.get('url', '')

            result = func(stack, soup, url)

            if not grouped:
                result_list += result
                continue

            stack_id = stack['stack_id']
            grouped_result[stack_id] += result

        return dict(grouped_result) if grouped else unique_hashable(result_list)

    def get_result_similar(self, url=None, html=None, soup=None, request_args=None, grouped=False):
        """
        Gets similar results based on the previously learned rules.

        Parameters:
        ----------
        url: str, optional
            URL of the target web page. You should either pass url or html or both.

        html: str, optional
            An HTML string can also be passed instead of URL.
                You should either pass url or html or both.

        request_args: dict, optional
            A dictionary used to specify a set of additional request parameters used by requests
                module. You can specify proxy URLs, custom headers etc.

        grouped: bool, optional, defaults to False
            If set to True, the result will be a dictionary with the rule_ids as keys
                and a list of scraped data per rule as values.

        Returns:
        --------
        List of similar results scraped from the web page.
        Dictionary if grouped=True.
        """

        func = self._get_result_with_stack
        return self._get_result_by_func(func, url, html, soup, request_args, grouped)

    def get_result_exact(self, url=None, html=None, soup=None, request_args=None, grouped=False):
        """
        Gets exact results based on the previously learned rules.

        Parameters:
        ----------
        url: str, optional
            URL of the target web page. You should either pass url or html or both.

        html: str, optional
            An HTML string can also be passed instead of URL.
                You should either pass url or html or both.

        request_args: dict, optional
            A dictionary used to specify a set of additional request parameters used by requests
                module. You can specify proxy URLs, custom headers etc.

        grouped: bool, optional, defaults to False
            If set to True, the result will be a dictionary with the rule_ids as keys
                and a list of scraped data per rule as values.

        Returns:
        --------
        List of exact results scraped from the web page.
        Dictionary if grouped=True.
        """

        func = self._get_result_with_stack_index_based
        return self._get_result_by_func(func, url, html, soup, request_args, grouped)

    def get_result(self, url=None, html=None, request_args=None, grouped=False):
        """
        Gets similar and exact results based on the previously learned rules.

        Parameters:
        ----------
        url: str, optional
            URL of the target web page. You should either pass url or html or both.

        html: str, optional
            An HTML string can also be passed instead of URL.
                You should either pass url or html or both.

        request_args: dict, optional
            A dictionary used to specify a set of additional request parameters used by requests
                module. You can specify proxy URLs, custom headers etc.

        grouped: bool, optional, defaults to False
            If set to True, the result will be dictionaries with the rule_ids as keys
                and a list of scraped data per rule as values.

        Returns:
        --------
        Pair of (similar, exact) results.
        See get_result_similar and get_result_exact methods.
        """

        soup = self._get_soup(url=url, html=html, request_args=request_args)
        similar = self.get_result_similar(url=url, soup=soup, grouped=grouped)
        exact = self.get_result_exact(url=url, soup=soup, grouped=grouped)
        return similar, exact

    def remove_rules(self, rules):
        """
        Removes a list of learned rules from stack_list.

        Parameters:
        ----------
        rules : list
            A list of rules to be removed

        Returns:
        --------
        None
        """

        self.stack_list = [x for x in self.stack_list if x['stack_id'] not in rules]

    def keep_rules(self, rules):
        """
        Removes all other rules except the specified ones.

        Parameters:
        ----------
        rules : list
            A list of rules to keep in stack_list.
        """

        self.stack_list = [x for x in self.stack_list if x['stack_id'] in rules]

    def generate_python_code(self):
        # deprecated
        print('This function is deprecated. Please use save() and load() instead.')
