# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

from bs4 import BeautifulSoup
import requests

import pickle


def main():
 
    print("This file should not be run directly")


class WebScrapper():

    def parse_site_bs(self, url, save_location):

        if url == "":
            print("no url given")
            return False

        response = requests.get(url)
        if response.status_code == 200:
            with open(save_location, 'wb') as f:
                f.write(response.content)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    
    def parse_local_file_bs(self, filename):
        
        soup = BeautifulSoup(open(filename, 'rb'), "html.parser")
        return soup



if __name__ == "__main__":
    main()
