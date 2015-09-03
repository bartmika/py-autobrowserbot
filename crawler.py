import os
import sys
import json
import random
import urllib3
from urllib3 import PoolManager, Retry, Timeout
import certifi
from random import randint
from bs4 import BeautifulSoup
from time import sleep


class WebCrawler:
    def __init__(self, url, bad_words):
        self.soup = None
        self.r = None
        self.url = url
        self.bad_words = bad_words
    
        # Object makes HTTP and HTTPS requests.
        # Note: https://urllib3.readthedocs.org/en/latest/security.html#using-certifi-with-urllib3
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED', # Force certificate check.
            ca_certs=certifi.where(),  # Path to the Certifi bundle.
            timeout=10.0, # Manager with 10 seconds combined timeout.
            retries=Retry(3, redirect=False), # 3 Retries and no redirects
        )
        
    def fetch_and_process(self):
        try:
            # Lookup the URL and get the HTML data from it and if
            # any errors occured then cancel the crawling with empty
            # array being returned.
            self.r = self.http.request('GET', self.url)
        except Exception as e:
            print("Failed getting link, reason: ", e)
            return False

        if self.r.status == 200:
            # Load up the HTML parser for the returned data or else
            # if error, return the urls that where currently processed.
            try:
                self.soup = BeautifulSoup(self.r.data, "html.parser")
                return True
            except Exception as e:
                print("Failed loading BeautifulSoup, reason:", e)
                return False

    def fetch_image(self, url):
        """
            Function downloads the image from the site but does nothing.
        """
        urls = []
        if self.soup is None:
            return urls

        try:
            r = self.http.request('GET', url)
        except Exception as e:
            #print("Failed getting link, reason: ", e)
            return False
        
        # Only process if a successful result was returned.
        if r.status == 200:
            return True
        else:
            return False


    def all_images(self):
        urls = []
        if self.soup is None:
            return urls
        try:
            html_imgs = self.soup.find_all('img')
            for img_element in html_imgs:
                src_url = img_element.get('src')
                if src_url:
                    # Cannot support 'gif' file format so skip this file.
                    if ".gif" in src_url:
                        pass
                    elif src_url[0] == '/' or src_url[0] == '?':
                        # Generate the new url by appending the newly
                        # discovered src_url.
                        src_url = self.url + src_url
                        urls.append(src_url)
                    elif src_url[0] == '#':
                        pass
                    else:
                         urls.append(src_url)
        except Exception as e:
            print('Error at URL:{}.ERROR:{}'.format(self.url,e))
                
        # Return all the valid urls we can use in our application.
        return self.filter_urls(urls)
    
    def all_urls(self):
        # Only process if a successful result was returned.
        urls = []
        if self.soup is None:
            return urls
        
        # Find all the links on the page which are link elements
        html_links = self.soup.find_all('a')
        for a_element in html_links:
            try:
                href_url = a_element.get('href')
                if href_url:
                    if href_url[0] == '/' or href_url[0] == '?':
                        # Generate the new url by appending the newly
                        # discovered href_url.
                        href_url = self.url + href_url
                        urls.append(href_url)
                    elif href_url[0] == '#':
                        pass
                    else:
                        urls.append(href_url)
            except Exception as e:
                print('Error at URL:{}.ERROR:{}'.format(self.url,e))
    
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
            url = url.lower()
            is_url_ok = True
            
            for bad_word in bad_words:
                if bad_word in url:
                    is_url_ok = False
                if "javascript" in url or ".ico" in url or "data:image" in url:
                    is_url_ok = False
        
            if is_url_ok:
                good_urls.append(url)
        return good_urls