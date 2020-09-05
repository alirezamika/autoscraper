from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class GeneratedAutoScraper(object):
    request_headers = {
        'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; \
            Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36'
    }

    def __init__(self):
        self.url = ''
        self.stack_list = "{STACK_LIST}"

    @staticmethod
    def _get_soup(url=None, html=None, request_args=None):
        if html:
            return BeautifulSoup(html, 'lxml')
        request_args = request_args if request_args else {}
        headers = dict(GeneratedAutoScraper.request_headers)
        if url:
            headers['Host'] = urlparse(url).netloc
        headers = request_args.get('headers', headers)
        html = requests.get(url, headers=headers, **request_args).text
        return BeautifulSoup(html, 'lxml')

    @staticmethod
    def unique(item_list):
        unique_list = []
        for item in item_list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list

    def _fetch_result_from_child(self, child, wanted_attr, is_full_url):
        if wanted_attr is None:
            return child.getText().strip().rstrip()
        if wanted_attr not in child.attrs:
            return None
        if is_full_url:
            return urljoin(self.url, child.attrs[wanted_attr])
        return child.attrs[wanted_attr]

    def _get_result_with_stack(self, stack, soup):
        parents = [soup]
        for _, item in enumerate(stack['content']):
            children = []
            for parent in parents:
                children += parent.findAll(item[0], item[1], recursive=False)
            parents = children

        wanted_attr = stack['wanted_attr']
        is_full_url = stack['is_full_url']
        result = [self._fetch_result_from_child(i, wanted_attr, is_full_url) for i in parents]
        result = list(filter(lambda x: x, result))
        return result

    def _get_result_with_stack_index_based(self, stack, soup):
        p = soup.findChildren(recursive=False)[0]
        stack_content = stack['content']
        for index, item in enumerate(stack_content[:-1]):
            p = p.findAll(stack_content[index + 1][0], recursive=False)[item[2]]
        result = self._fetch_result_from_child(p, stack['wanted_attr'], stack['is_full_url'])
        return result

    def get_result_similar(self, url=None, html=None, soup=None, request_args=None):
        if url:
            self.url = url
        if not soup:
            soup = self._get_soup(url=url, html=html, request_args=request_args)
        result = []
        for stack in self.stack_list:
            result += self._get_result_with_stack(stack, soup)
        return self.unique(result)

    def get_result_exact(self, url=None, html=None, soup=None, request_args=None):
        if url:
            self.url = url
        if not soup:
            soup = self._get_soup(url=url, html=html, request_args=request_args)
        result = []
        for stack in self.stack_list:
            try:
                result.append(self._get_result_with_stack_index_based(stack, soup))
            except IndexError:
                continue
        return self.unique(result)

    def get_result(self, url=None, html=None, request_args=None):
        soup = self._get_soup(url=url, html=html, request_args=request_args)
        similar = self.get_result_similar(soup=soup)
        exact = self.get_result_exact(soup=soup)
        return similar, exact
