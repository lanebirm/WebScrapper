# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

import pickle
import sys
import urllib.request

# python script imports
import settings as settings_file
import web_scrapper


def main():

    settings = settings_file.SettingsClass()

    WS = web_scrapper.WebScrapper()

    site_soups = []

    test_list = []

    for i, url in enumerate(settings.urls):
        if settings.pull_html:
            # get BeautifulSoup parsed format of we sites. Pickle for reuse
            site_soup = WS.parse_site(settings.urls[0])
            site_soups.append(site_soup)

            urllib.request.urlretrieve(
                url, "html_files/html_" + str(i) + ".html")
        else:
            site_soups.append(WS.parse_local_file("html_files/html_" + str(i) + ".html"))

    test_list = site_soups[0].find_all("a")

    print(test_list)

    print("main finished")

    return


if __name__ == "__main__":
    main()
