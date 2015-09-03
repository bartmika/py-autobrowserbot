import os
import sys
import json
from multiprocessing import Pool
from simulatedbrowser import *


# This constant controls how many seperate individual bots are to be
# running for this application
NUMBER_OF_RUNNING_BOT_INSTANCES = 6


class AutoBrowserBot:
    def __init__(self, id):
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

def run_bot(bot_id):
    """
        Run a single bot instance.
    """
    print("Starting Bot #", bot_id)
    bot = AutoBrowserBot(bot_id)
    bot.run()

# Entry point into the application
if __name__ == "__main__":
    """
        To run this application, simply run the following in your console:
        - - - - - - - - - - - - - -
        python autobrowserbot.py
        - - - - - - - - - - - - - -
    """
    os.system('clear;')  # Clear the console text.
    with Pool(NUMBER_OF_RUNNING_BOT_INSTANCES) as p:
        p.map(run_bot, [1, 2, 3, 4, 5, 6])
