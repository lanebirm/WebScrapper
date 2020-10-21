# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

import pickle

# python script imports
import settings as settings_file
import web_scrapper
import items_structures


def main():

    settings = settings_file.SettingsClass()

    WS = web_scrapper.WebScrapper()

    parsed_site_objects = []

    for i, url in enumerate(settings.urls):
        if settings.pull_html:
            # get BeautifulSoup parsed format of web sites. saved to /html_files folder
            parsed_site_object = WS.parse_site_bs(
                settings.urls[i],  ("html_files/html_" + str(i) + ".html"))
            parsed_site_objects.append(parsed_site_object)
        else:
            parsed_site_objects.append(WS.parse_local_file_bs(
                "html_files/html_" + str(i) + ".html"))

    IC = items_structures.SaleItemConstructor()

    IC.generate_items_gumtree(parsed_site_objects[0])

    print("main finished")

    return


def test():

    print("test finished")


if __name__ == "__main__":
    main()
    # test()
