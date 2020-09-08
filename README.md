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

### Grouping results and removing unwanted ones

Here we want to scrape product name, price and rating from ebay product pages:

```python
url = 'https://www.ebay.com/itm/Sony-PlayStation-4-PS4-Pro-1TB-4K-Console-Black/203084236670' 

wanted_list = ['Sony PlayStation 4 PS4 Pro 1TB 4K Console - Black', 'US $349.99', '4.8'] 

scraper.build(url, wanted_list)
```
The items which we wanted have been on multiple sections of the page and the scraper tries to catch them all. So it may retrieve some extra information compared to what we have in mind.
Let's run it on a different page:
```python
scraper.get_result_exact('https://www.ebay.com/itm/Acer-Predator-Helios-300-15-6-144Hz-FHD-Laptop-i7-9750H-16GB-512GB-GTX-1660-Ti/114183725523') 
```
The result:
```python
[
    "Acer Predator Helios 300 15.6'' 144Hz FHD Laptop i7-9750H 16GB 512GB GTX 1660 Ti",
    'ACER Predator Helios 300 i7-9750H 15.6" 144Hz FHD GTX 1660Ti 16GB 512GB SSD⚡RGB',
    'US $1,229.49',
    '5.0'
]
```
As we can see we have one extra item here. We can run the `get_result_exact` or `get_result_similar` method with `grouped=True` parameter. It will group all results per its scraping rule:
 
Output:
```python
{
    'rule_sks3': ["Acer Predator Helios 300 15.6'' 144Hz FHD Laptop i7-9750H 16GB 512GB GTX 1660 Ti"],
    'rule_d4n5': ['ACER Predator Helios 300 i7-9750H 15.6" 144Hz FHD GTX 1660Ti 16GB 512GB SSD⚡RGB'],
    'rule_fmrm': ['ACER Predator Helios 300 i7-9750H 15.6" 144Hz FHD GTX 1660Ti 16GB 512GB SSD⚡RGB'],
    'rule_2ydq': ['US $1,229.49'],
    'rule_buhw': ['5.0'],
    'rule_vpfp': ['5.0']
}
```
 
Now we can use `keep_rules` or `remove_rules` methods to prune unwanted rules:
 
```python
scraper.keep_rules(['rule_sks3', 'rule_2ydq', 'rule_buhw'])
 
scraper.get_result_exact('https://www.ebay.com/itm/Acer-Predator-Helios-300-15-6-144Hz-FHD-Laptop-i7-9750H-16GB-512GB-GTX-1660-Ti/114183725523') 
```

And now the result only contains the ones which we want:
```python
[
    "Acer Predator Helios 300 15.6'' 144Hz FHD Laptop i7-9750H 16GB 512GB GTX 1660 Ti",
    'US $1,229.49',
    '5.0'
]
 ```
#### Happy Coding  ♥️
