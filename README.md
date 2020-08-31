# AutoScraper: A Smart Automatic Scraper for Python


This project is made for automatic web scraping to make scraping easy. 
It gets an url or the html content of a web page and a list of sample data which we want to scrape from that page. It learns the scraping rules and returns the similar elements. Then you can use this learned object with new urls to get similar content of those new pages.

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
# You can also put urls here to retrive urls.
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

### Getting exact results

Say we want to scrape stock live prices from Nasdaq:

```python
from autoscraper import AutoScraper

url = 'https://www.google.com/finance?oq=aapl'

wanted_list = ["124.81"]

scraper = AutoScraper()

# Here we can also pass html content via the html parameter instead of the url (html=html_content)
result = scraper.build(url, wanted_list)
print(result)
```

You can also pass any custom `requests` module attribute. for example you may want to use proxies:

```python
proxies = {
    "http": 'http://127.0.0.1:8001',
    "https": 'https://127.0.0.1:8001',
}

result = scraper.build(url, wanted_list, request_args=dict(proxies=proxies))
```

Now we can get the price of any nasdaq symbol:

```python
scraper.get_result_exact('https://www.google.com/finance?oq=msft')
```

### Generating the scraper python code

We can generate a code for the built scraper to use it later:

```python
scraper.generate_python_code()
```

It will print the generated code. There's a class named `GeneratedAutoScraper` which has the methods `get_result_similar` and 
`get_result_exact` which you can use. You can also use `get_result` method to get both.
