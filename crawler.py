import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import sys
import collections
import re


class URLValidator:
    def __init__(self):
        self.url_validation_re = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def validate_url(self, url):
        if url is None:
            raise ValueError("Must define url to crawl: ./crawler.py http://www.rescale.com ")

        if re.match(self.url_validation_re, url) is None:
            raise ValueError("Invalid URL: ", args.url, " (ex: python crawler.py http://www.rescale.com )")


def get_website(url):
    try:
        response = requests.request('GET', url, timeout=5.0)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all("a")
        results = [str(link.get('href')) for link in results]  # get href value from html element
        results = [link for link in results if link[:4] == "http"]  # keeps links that begin with http

        ## Log WebCrawl  ###
        buff_output = ""
        buff_output += url + "\n"
        for result_url in results:
            buff_output+= " "+result_url+"\n"
        print(buff_output)

        results = list(set(results))  # Removes duplicates
        website_data = {
            "url": url,
            "html": str(response.text),
            "created_at": datetime.now().isoformat(),
            "links": results,
            "success": True,
        }
        return website_data
    except:
        return {
            "url": url,
            "html": None,
            "created_at": datetime.now(),
            "links": [],
            "success": False}
        pass

class Crawler:

    def __init__(self):
        os.environ["no_proxy"] = "*"
        pass

    @staticmethod
    def multi_process(urls):
        data= []
        with Pool(20) as pool:
            data = pool.map(get_website, urls)
        return data


    @staticmethod
    def save_data(listofDicts):
        with open('data.csv', 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=listofDicts[0].keys(), )
            fc.writeheader()
            fc.writerows(listofDicts)

    @staticmethod
    def crawl(url, max_crawl=100):
        visited = []
        to_visit = [url]
        total_data = []

        while (len(to_visit)) > 0:

            if len(total_data) >= max_crawl:
                break
            visit_limit = max_crawl - len(total_data)
            to_visit = to_visit[:visit_limit]
            data = Crawler.multi_process(to_visit)
            total_data.extend(data)
            to_visit = []

            for i in data:
                visited.append(i["url"])
            new_links = [i for i in data if i["success"]]
            new_links = [i for i in new_links if i["links"] is not None]
            new_links = [links for i in new_links for links in i["links"]]
            to_visit.extend([i for i in new_links if i not in visited])

        return total_data


if __name__ == '__main__':

    arg_names = ['crawler', 'url', 'max_crawl']
    args = dict(zip(arg_names, sys.argv))
    Arg_list = collections.namedtuple('Arg_list', arg_names)
    args = Arg_list(*(args.get(arg, None) for arg in arg_names))

    url_validator = URLValidator()
    url_validator.validate_url(args.url)

    if args.max_crawl is not None:
        try:
            max_crawl = int(args.max_crawl)
        except ValueError:
            raise ValueError("Invalid max_crawl limit: ", args.max_crawl, " ( please enter an int )")

    crawler = Crawler()

    if args.max_crawl:

        data = crawler.crawl(args.url, max_crawl)

    else:
        data = crawler.crawl(args.url)

    Crawler.save_data(data)
    print("Crawl completed: Data outputted as data.csv")
