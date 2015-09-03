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
from constant import *


class SimulatedBrowser:
    """
        Class is responsible for automatically browsing through the
        website urls found in the inputted safe_websites.json file.
    """
    def __init__(self, root_url, bad_words):
        self.root_url = root_url
        self.bad_words = bad_words
        self.visited = []

    def visit_page(self, url):
        """
            Function will visit the page and return ALL URLs from the page
            and all image URLs.
        """
        
        # Get the domain URL
        url = url.replace("http://", "")
        url = url.replace("https://", "")
        url = url.replace("www.", "")
        url = url.replace("www2.", "")
        
        # If we already visited this link, then don't visit it again.
        if url in self.visited:
            print("Skipping:",url)
            return {
                'pages': '',
                'images': '',
            }
        else:
            print("Visiting:",url)

        # Keep track of all the visited pages.
        self.visited.append(url)
        
        # Fetch the page URL and get more hyperlinks in the page and reshuffle
        # them so when we fetch them again, they will be random.
        crawler = WebCrawler(url, self.bad_words)
        if crawler.fetch_and_process() is False:
            sleep(AVG_PAGE_VIEW_SLEEP)
            return []
        page_urls = crawler.all_urls()
        random.shuffle(page_urls)
        
        # Fetch and download all the images on the page as a normal browser
        # would do when visiting a page.
        image_urls = crawler.all_images()
        random.shuffle(page_urls)
        for url in image_urls:
            if crawler.fetch_image(url):
                pass
        
        # Add an artifical delay before returning URLs to simulate
        # a user 'browsing' the page.
        self.random_delay_wait()
                       
        # Return all the links & images on this site.
        return {
            'pages': page_urls,
            'images': image_urls,
        }

    def randomized_visit_page(self,url):
        """
            Function will visit the page and return RANDOMLY SELECTED
            URLs from the page and all image URLs.
        """
        # Visit the page
        page_info = self.visit_page(url)
        pages = page_info['pages']
        
        # Randomly select how many links we are to "click" through on the
        # current website and then go ahead and click through them. If there
        # where no clickable links selected then exit this site.
        url_counts = len(pages)
        
        # If no clickable links, do not continue.
        if url_counts == 0:
            return page_info
        
        # Depending on what number we randomized, load up the pages
        # depending on the random number.
        num_of_sites_to_visit = randint(1, url_counts)
        visit = 0
        new_page_urls = []
        while visit < num_of_sites_to_visit:
            new_page_urls.append(pages[visit])
            visit += 1

        page_info['pages'] = new_page_urls
        return page_info

    def random_delay_wait(self):
        # Generate how long we should stay on the particular page.
        value = randint(MIN_PAGE_VIEW_SLEEP, MAX_PAGE_VIEW_SLEEP)
        sleep(value)