
# Generated by Qodo Gen
from autoscraper.auto_scraper import AutoScraper


# Dependencies:
# pip install pytest-mock
import pytest

class TestAutoScraper:

    # Build scraping rules from URL by providing wanted_list and successfully extract data
    def test_build_with_wanted_list(self, mocker):
        # Arrange
        url = "http://test.com"
        wanted_list = ["item1", "item2"]
        html = "<html><body><div>item1</div><span>item2</span></body></html>"
    
        mock_soup = mocker.patch('autoscraper.auto_scraper.BeautifulSoup')
        mock_soup.return_value.findChildren.return_value = []
    
        mock_get = mocker.patch('requests.get')
        mock_get.return_value.text = html
        mock_get.return_value.encoding = "utf-8"
    
        scraper = AutoScraper()
    
        # Act
        results = scraper.build(url=url, wanted_list=wanted_list)
    
        # Assert
        assert len(scraper.stack_list) == 0
        assert results == []
        mock_get.assert_called_once()
        mock_soup.assert_called_once()

    # Build rules with empty wanted_list or wanted_dict
    def test_build_with_empty_wanted(self, mocker):
        # Arrange
        url = "http://test.com"
        html = "<html><body></body></html>"
    
        mock_soup = mocker.patch('autoscraper.auto_scraper.BeautifulSoup')
        mock_get = mocker.patch('requests.get')
        mock_get.return_value.text = html
        mock_get.return_value.encoding = "utf-8"
    
        scraper = AutoScraper()
    
        # Act
        results = scraper.build(url=url)
    
        # Assert
        assert len(scraper.stack_list) == 0
        assert results == []
        mock_get.assert_not_called()
        mock_soup.assert_not_called()