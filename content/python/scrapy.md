Title: Crawling and scraping Google Scholar with Scrapy
Date: 2017-02-08
Category: Python
Tags: Web scraping, Python, Scrapy
Slug: crawl-google-cholar
Authors: Longwen Ou
Summary: Introduction to web crawling and scraping with Scrapy


I am learning web crawling and scraping since it is useful when you want to extract data from websites when no API is available. Since I use python, I searched for some good tools for this task. Eventually I decided to go with [`Scrapy`](https://scrapy.org) due to its ease to use and capability of both web crawling and scraping. In this post I show the process of crawling and scraping *Google Scholar* with `Scrapy`.

The purpose of this project is to download information on all publications of an author as well as information on the publications which cited the author's work. The source code is available on [my github](https://github.com/oulongwen/google-scholar-crawler).

### Installing Scrapy
Installing `Scrapy` is pretty straightforward. You can install `Scrapy` with `pip`: `pip install Scrapy`. However, this is not the recommended way of installing `Scrapy`. For web development tools such as `Scrapy`, `pelican`, and `Djaon`, the best practice is to install them in an "isolated" environment becuase your project is going to rely on this particular version of package. A good introduction about virtual environment in python can be found [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/). If you are using python3, creating a virtual environment is pretty simple:
```bash
$ python3 -m venv scrapyvenv
```
Here `scrapyvenv` is just the name of your virtual environment and you can name it whatever you want. Now that the virtual environment is created, we can activate the virtual environment:
```bash
$ source scrapyvenv/bin/activate
```
Now our virtual environment should be ready. You can check whether your virtual environment is already activated by the following command:
```bash
$ which python
```
If your virtual environment is activated, you will see something like this:
```bash
$ path-to-venv/scrapyvenv/bin/python
```
Now that our virtual environment is ready, we can install `Scrapy` with `pip`:
```bash
$ pip install Scrapy
```

### Web scraping with Scrapy
#### Defining spiders
In order to start scrapying, a Scrapy project must be first set up. Here I named my project "scholar":
```bash
$ scrapy start project scholar
```
The above command creates a `scholar` directory together with several sub-directories and files. The most important directory is the `spiders` folder located at `.../scholar/scholar/spiders`. This folder contains the python files where we define our spiders for web crawling. We define each spider as a class, where we also define its name and the url to start crawling. The name of a spider is important because this is how `Scrapy` identifies a spider. Another important component of a *spider* class is the `parse` method which will be called to handle the response downloaded for each request. A `parse` method has two basic functions: 1) to extract data, and 2) to yield another request with a specified `parse` method to handle this request. My `cite_spider.py` file looks like this:
```python
import scrapy
from scholar.items import ScholarItem


class CiteSpider(scrapy.Spider):
    name = "citation"
    page_size = 20
    start = 0
    # urls = 'https://scholar.google.com/citations?user=nbPXtEUAAAAJ&hl=en'
    urls = 'https://scholar.google.com/citations?user=EXATcMAAAAAJ&hl=en'
    start_urls = [urls + '&cstart={}&pagesize={}'.format(start, page_size)]

    def parse(self, response):
        if response.css("td.gsc_a_t").extract_first() is not None:
            for paper in response.css("td.gsc_a_t"):
                paper_title = paper.css("a::text").extract_first()
                paper_authors = paper.css("div.gs_gray::text").extract_first()

                item = ScholarItem()
                item['title'] = paper_title
                item['authors'] = paper_authors
                yield item

            CiteSpider.start += CiteSpider.page_size
            next_page = CiteSpider.start_urls[0] + '&cstart={}&pagesize={}'.format(CiteSpider.start, CiteSpider.page_size)
            yield scrapy.Request(next_page, callback=self.parse)

            for cite in response.css('td.gsc_a_c a::attr(href)').extract():
                if len(cite) > 0:
                    yield scrapy.Request(cite, callback=self.parse2)

    def parse2(self, response):

        for paper in response.css('div.gs_ri'):

            item = ScholarItem()
            item['title'] = paper.css('h3.gs_rt a::text').extract_first()
            item['authors'] = paper.css('div.gs_a::text').extract_first()
            yield item

            next_page = response.xpath('//span[@class="gs_ico gs_ico_nav_next"]/../@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse2)
```
Here I defined two parse functions, because there are two types of web pages I need to handle. Each type of web page has different structures from the other. In other words, our desired content on each type of website is in different html tags. For instance, the first type of web pages to handle is the pages showing the list of publications of a particular author. It looks like this:

<img src='/images/author.png' width=100%/>

The information in this page that we are interested in is the title of the publications and other information such as authors, journal title, year of publication, etc. In order to extract the desired information, we need to identify the html tags that contain these information. It is convenient with chrome. Just right click the information you are interested and click *"Inspect"*, we can inspect the source code that contains the information. Here the title is under a `<td>` tag with `class=gsc_a_t`.

The second type of pages result from clicking the link of the number indicating the number of citations of each publication. These links direct to pages showing a list of publications that the original publication is cited by. The page is shown below. These pages have very different structures as the first type of pages. Therefore we need two `parse` methods, each handling one type of the pages.

<img src='/images/cite.png' width=100%/>

#### Writing *items.py* file
`Scrapy` usually returns extracted data as dictionaries. However, it is not recommened to define the dictionary to return in the same file where spiders are defined. The reason is that if a typo is made when defining the dictionary keys, a completely different dictionary would be created without raising any errors. Hence `Scrapy` allows defining the dictionary keys in the `items.py` file. After importing the items.py file in the spider file, only dictionaries with the acceptable keys (i.e., keys defined in the `items.py` file) can be returned. If the user attempted to write a dictionary with a key not defined in the `items.py` file, an error would be raised. This is good practice for preventing unintentional mistakes. In this project, two fields are needed to store the title and other information for each paper respectively. The *items.py* files looks like this:
```python
import scrapy


class ScholarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
```
Now that we have defined our spider, we can start crawling using the following command:
```bash
$ scrapy crawl citation -o papers.jl
```
Here *"citation"* is the name of the spider, as defined in the `cite_spider.py` file. The `-o` flag specifies the output file storing the extracted data. Scrapy supports several output file format including `JSON`, `JSON lines`, `CSV`, and `XML`. Here I store the extracted data in `JSON line` format. After the spider is successfully run, the specified output file will be created with all the extracted data.

Again the source code can be found on [my github](https://github.com/oulongwen/google-scholar-crawler).
