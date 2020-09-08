# Task1: Scraping results from assigned search engine
from bs4 import BeautifulSoup
import time
import requests
from random import randint
import json
from collections import OrderedDict
from html.parser import HTMLParser

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100Safari/537.36'}

class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep:  # Prevents loading too many pages too soon
            time.sleep(randint(10, 100))
        SEARCHING_URL="https://www.duckduckgo.com/html/?q="
        temp_url = '+'.join(query.split())  # for adding + between words for  the query
        url = SEARCHING_URL + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text,
                             "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all('a', attrs = {'class' : 'result__a'}, href=True)
        results = []
        for result in raw_results:
            link = result['href']
            if(len(results)==10): break
            if(link in results): continue
            else: results.append(link)
        return results


if __name__=="__main__":
    file_name = 'Queries.txt'
    result_dict= {}
    queries = open(file_name,"r")
    itr =1;
    for query in queries:
        res = SearchEngine.search(query,False)
        key = str(query.strip())
        result_dict[key]= res
        itr += 1;
    with open('Ask_Results.json', 'w') as outfile:
        json.dump(result_dict, outfile, indent=4)

