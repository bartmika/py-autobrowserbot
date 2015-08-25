import os
import sys
import json
import random
import urllib3
import certifi
from random import randint
from bs4 import BeautifulSoup
from time import sleep
from crawler import *


# These constants are used by the application to randomily pick a number
# in between on of these ranges.
MIN_PAGE_VIEW_SLEEP = 1
MAX_PAGE_VIEW_SLEEP = 60
AVG_PAGE_VIEW_SLEEP = 30


class AutoBrowserBot:
    def __init__(self):
        # Load up our website URL's from the JSON file.
        urls = []
        with open('safe_websites.json') as data_file:
            json_data = json.load(data_file)
            for website in json_data['websites']:
                url = website['url']
                urls.append(url)
        self.urls = urls
        
        # Load up the bad words we want to avoid in our URL links.
        bad_words = []
        with open('bad_words.json') as data_file:
            bad_words_data = json.load(data_file)
            for website in bad_words_data['keywords']:
                bad_word = website['word']
                bad_words.append(bad_word)
        self.bad_words = bad_words

    def run(self):
        """
            Function runs continuously iterating through all the websites
            we have on file and simulate browsing through them.
        """
        while True:
            # Randomize the URLs so we will be visiting each site in random
            # and unpredictable order.
            random.shuffle(self.urls)
            
            # Browse around all our sites through a random order.
            for url in self.urls:
                self.browse_site_and_click_around(url)

    def browse_site_and_click_around(self, url):
        """
            Function simulates visiting a site randomly clicks around the
            clickable content on the page and loads up the associated pages.
        """
        print("[Root]", url)
        clickable_urls = self.browse_site(url)
    
        # Randomly select how many links we are to "click" through on the
        # current website and then go ahead and click through them. If there
        # where no clickable links selected then exit this site.
        url_counts = len(clickable_urls)
        
        # If no clickable links, do not continue.
        if url_counts == 0:
            return
        
        # Else there are number of links, click through them.
        num_of_sites_to_visit = randint(1, url_counts)
        visit = 0
        while visit < num_of_sites_to_visit:
            clickable_url = clickable_urls[visit]
            self.browse_site(clickable_url)
            visit += 1

    def browse_site(self, url):
        """
            Function simulates visiting a page by fetching the page from the
            website, waiting for a random amount and then return all the 
            clickable URLs there are on the page.
        """
        # Fetch the page URL and get more hyperlinks in the page and reshuffle
        # them so when we fetch them again, they will be random.
        crawler = WebCrawler(url, self.bad_words)
        if crawler.fetch_and_process() is False:
            sleep(AVG_PAGE_VIEW_SLEEP)
            return []
        more_urls = crawler.all_urls()
        
        # Randomize the URLs so we will be visiting each site in random
        # and unpredictable order.
        random.shuffle(more_urls)
        
        # Generate how long we should stay on the particular page
        # before proceeding to our next page.
        random_sleep_interval = randint(MIN_PAGE_VIEW_SLEEP, MAX_PAGE_VIEW_SLEEP)
        
        # Delay visiting another page before our sleep counter finishes
        sleep(random_sleep_interval)
        print("[Visited]", url)
        return more_urls

# Entry point into the application
if __name__ == "__main__":
    os.system('clear;')  # Clear the console text.
    bot = AutoBrowserBot()
    bot.run()