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
from simulatedbrowser import *
#from constant import *


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
        # Run autonomous web-browsing through the autopilot class.
        while True:
            self.main_runtime_loop()
        
    def main_runtime_loop(self):
        # Iterate through all the websites in random order and then
        # use the autopilot to autonomously browse through the websites
        # and all the associated sites.
        random.shuffle(self.urls)
        for url in self.urls:
            self.autonomously_surf_site(url)

    def autonomously_surf_site(self, url):
        browser = SimulatedBrowser(url, self.bad_words)
        root_page_info = browser.visit_page(url)
        
        # Iterate through all the page images and go through them.
        # Dept order (1) browsing
        for page_url in root_page_info['pages']:
            page_info = browser.randomized_visit_page(page_url)

            # Dept order (2) browsing
            for page_url2 in page_info['pages']:
                page_info2 = browser.randomized_visit_page(page_url2)

                # Dept order (3) browsing
                for page_url3 in page_info['pages']:
                    page_info3 = browser.randomized_visit_page(page_url3)

# Entry point into the application
if __name__ == "__main__":
    """
        To run this application, simply run the following in your console:
        - - - - - - - - - - - - - -
        python autobrowserbot.py
        - - - - - - - - - - - - - -
    """
    os.system('clear;')  # Clear the console text.
    bot = AutoBrowserBot()
    bot.run()