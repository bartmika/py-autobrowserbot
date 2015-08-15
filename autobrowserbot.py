import os
import sys
import json
import random
import urllib3
import certifi
from random import randint
from bs4 import BeautifulSoup
from time import sleep


# These constants are used by the application to randomily pick a number
# in between on of these ranges.
MIN_PAGE_VIEW_SLEEP = 1
MAX_PAGE_VIEW_SLEEP = 60


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
        
        # Object makes HTTP and HTTPS requests.
        # Note: https://urllib3.readthedocs.org/en/latest/security.html#using-certifi-with-urllib3
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED', # Force certificate check.
            ca_certs=certifi.where(),  # Path to the Certifi bundle.
        )

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
        print("Root:", url);
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
        print("Visiting:", url);
        # Generate how long we should stay on the particular page
        # before proceeding to our next page.
        random_sleep_interval = randint(MIN_PAGE_VIEW_SLEEP, MAX_PAGE_VIEW_SLEEP)
                                
        # Fetch the page URL and get more hyperlinks in the page and reshuffle
        # them so when we fetch them again, they will be random.
        more_urls = self.crawl_page(url)
        random.shuffle(more_urls)
        
        # Delay visiting another page before our sleep counter finishes
        print("Wait:", random_sleep_interval, " seconds");
        sleep(random_sleep_interval)
        return more_urls

    def crawl_page(self,url):
        """
            Function fetchs HTML data from the web-server at the URL and 
            returns all the available hyperlinks it parsed.
        """
        try:
            # Lookup the URL and get the HTML data from it and if
            # any errors occured then cancel the crawling with empty
            # array being returned.
            r = self.http.request('GET', url)
        except Exception as e:
            print("Error for", url)
            return []
        
        # Only process if a successful result was returned.
        urls = []
        if r.status == 200:
            soup = BeautifulSoup(r.data, "html.parser")
            html_links = soup.find_all('a')
            for a_element in html_links:
                try:
                    href_url = a_element.get('href')
                    if href_url:
                        if href_url[0] == '/' or href_url[0] == '?':
                            href_url = url + href_url
                            urls.append(href_url)
                        elif href_url[0] == '#':
                            pass
                        else:
                            urls.append(href_url)
                except Exception as e:
                    print('Error at URL:{}.ERROR:{}'.format(url,e))
    
        # Return all the valid urls we can use in our application.
        return self.filter_urls(urls)

    def filter_urls(self, uncertain_urls):
        """
            Function will look through all the urls and remove any
            URLs that have 'bad' words in them, such as 'terrorism'.
        """
        good_urls = []
        bad_words = self.bad_words
        for url in uncertain_urls:
            is_url_ok = True
            
            for bad_word in bad_words:
                if bad_word in url:
                    is_url_ok = False
        
            if is_url_ok:
                good_urls.append(url)
        return good_urls

# Entry point into the application
if __name__ == "__main__":
    os.system('clear;')  # Clear the console text.
    bot = AutoBrowserBot()
    bot.run()