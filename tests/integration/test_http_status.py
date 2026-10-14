import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import pytest


HTML = ('<html class="page" style="display:block">'
        '<body class="body" style="display:block">'
        '<p class="target" style="color:red">Wanted</p>'
        '<p class="other" style="color:blue">Other</p></body></html>')
SCRAPE = """
import json
import sys
import requests
from autoscraper import AutoScraper

scraper = AutoScraper()
scraper.build(html=sys.argv[3], wanted_list=['Wanted'])
arguments = {'url': sys.argv[1], 'request_args': {'timeout': 2, 'proxies': {'http': '', 'https': ''}}}
if sys.argv[2] == 'build':
    arguments['wanted_list'] = ['Wanted']
try:
    result = getattr(scraper, sys.argv[2])(**arguments)
except requests.HTTPError as error:
    print(json.dumps({'http_error': error.response.status_code}))
else:
    print(json.dumps({'result': result}))
"""


@pytest.fixture
def http_url():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/redirect":
                self.send_response(302)
                self.send_header("Location", "/200")
                self.end_headers()
                return
            self.send_response(int(self.path[1:]))
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:{}".format(server.server_port)
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def scrape(url, method):
    # Isolate the real installed requests/BeautifulSoup from conftest's doubles.
    result = subprocess.run(
        [sys.executable, "-c", SCRAPE, url, method, HTML],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize("method", ["build", "get_result", "get_result_similar", "get_result_exact"])
@pytest.mark.parametrize("status", [404, 500])
def test_http_errors_are_not_scraped(http_url, method, status):
    assert scrape("{}/{}".format(http_url, status), method) == {"http_error": status}


@pytest.mark.parametrize("method", ["build", "get_result", "get_result_similar", "get_result_exact"])
def test_successful_fetch_still_scrapes(http_url, method):
    expected = [["Wanted"], ["Wanted"]] if method == "get_result" else ["Wanted"]
    assert scrape(http_url + "/200", method) == {"result": expected}


def test_successful_redirect_still_scrapes(http_url):
    assert scrape(http_url + "/redirect", "build") == {"result": ["Wanted"]}
