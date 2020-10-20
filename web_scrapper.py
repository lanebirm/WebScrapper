# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

from bs4 import BeautifulSoup
import urllib.request

import pickle


def main():
 
    print("This file should not be run directly")


class WebScrapper():

    def parse_site(self, url):

        if url == "":
            print("no url given")
            return False

        page = urllib.request.urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup
    
    def parse_local_file(self, filename):
        
        soup = BeautifulSoup(open(filename, 'rb'), "html.parser")
        return soup


if __name__ == "__main__":
    main()
