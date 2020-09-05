# AutoScraper: A Smart, Automatic, Fast and Lightweight Web Scraper for Python

![img](https://user-images.githubusercontent.com/17881612/91968083-5ee92080-ed29-11ea-82ec-d99ec85367a5.png)

This project is made for automatic web scraping to make scraping easy. 
It gets a url or the html content of a web page and a list of sample data which we want to scrape from that page. **This data can be text, url or any html tag value of that page.** It learns the scraping rules and returns the similar elements. Then you can use this learned object with new urls to get similar content or the exact same element of those new pages.

## Installation

It's compatible with python3.

Install from source:
```bash
$ python setup.py install
```
    
Install latest version from git repository using pip:
```bash
$ pip install git+https://github.com/alirezamika/autoscraper.git
```

## How to use

### Getting similar results

Say we want to fetch all related post titles in a stackoverflow page:

```python
from autoscraper import AutoScraper

url = 'https://stackoverflow.com/questions/2081586/web-scraping-with-python'

# We can add one or multiple candidates here.
# You can also put urls here to retrieve urls.
wanted_list = ["How to call an external command?"]

scraper = AutoScraper()
result = scraper.build(url, wanted_list)
print(result)
```

Here's the output:
```python
[
    'How do I merge two dictionaries in a single expression in Python (taking union of dictionaries)?', 
    'How to call an external command?', 
    'What are metaclasses in Python?', 
    'Does Python have a ternary conditional operator?', 
    'How do you remove duplicates from a list whilst preserving order?', 
    'Convert bytes to a string', 
    'How to get line count of a large file cheaply in Python?', 
    "Does Python have a string 'contains' substring method?", 
    'Why is “1000000000000000 in range(1000000000000001)” so fast in Python 3?'
]
```
Now you can use the `scraper` object to get related topics of any stackoverflow page:
```python
scraper.get_result_similar('https://stackoverflow.com/questions/606191/convert-bytes-to-a-string')
```

### Getting exact result

Say we want to scrape live stock prices from yahoo finance:

```python
from autoscraper import AutoScraper

url = 'https://finance.yahoo.com/quote/AAPL/'

wanted_list = ["124.81"]

scraper = AutoScraper()

# Here we can also pass html content via the html parameter instead of the url (html=html_content)
result = scraper.build(url, wanted_list)
print(result)
```

You can also pass any custom `requests` module parameter. for example you may want to use proxies or custom headers:

```python
proxies = {
    "http": 'http://127.0.0.1:8001',
    "https": 'https://127.0.0.1:8001',
}

result = scraper.build(url, wanted_list, request_args=dict(proxies=proxies))
```

Now we can get the price of any symbol:

```python
scraper.get_result_exact('https://finance.yahoo.com/quote/MSFT/')
```

**You may want to get other info as well.** For example if you want to get market cap too, you can just append it to the wanted list. By using the `get_result_exact` method, it will retrieve the data as the same exact order in the wanted list.

**Another example:** Say we want to scrape the about text, number of stars and the link to pull requests of Github repo pages:

```python
url = 'https://github.com/alirezamika/autoscraper'

wanted_list = ['A Smart, Automatic, Fast and Lightweight Web Scraper for Python', '662', 'https://github.com/alirezamika/autoscraper/issues']

scraper.build(url, wanted_list)
```

Simple, right?


### Saving the model

We can now save the built model to use it later. To save:

```python
# Give it a file path
scraper.save('yahoo-finance')
```

And to load:

```python
scraper.load('yahoo-finance')
```

#### Happy Coding  ♥️
