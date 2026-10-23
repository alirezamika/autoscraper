import autoscraper.auto_scraper as auto_scraper_module
from autoscraper import AutoScraper


class _SyntheticResponse:
    encoding = "utf-8"
    headers = {}
    text = "<p>fixture</p>"


def test_fetch_uses_default_timeout_without_mutating_request_args(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, **request_args):
        captured["url"] = url
        captured["headers"] = headers
        captured["request_args"] = request_args
        return _SyntheticResponse()

    monkeypatch.setattr(auto_scraper_module.requests, "get", fake_get)
    request_args = {
        "params": {"q": "synthetic"},
        "headers": {"X-Test": "synthetic"},
    }

    result = AutoScraper._fetch_html("https://example.invalid/page", request_args)

    assert result == "<p>fixture</p>"
    assert captured["request_args"]["timeout"] == 10
    assert captured["headers"]["X-Test"] == "synthetic"
    assert request_args == {
        "params": {"q": "synthetic"},
        "headers": {"X-Test": "synthetic"},
    }


def test_fetch_preserves_explicit_timeout_override(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, **request_args):
        captured.update(request_args)
        return _SyntheticResponse()

    monkeypatch.setattr(auto_scraper_module.requests, "get", fake_get)
    AutoScraper._fetch_html("https://example.invalid/page", {"timeout": (2, 5)})

    assert captured["timeout"] == (2, 5)
