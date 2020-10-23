# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

from datetime import datetime

# python script imports
import time_convertor


def main():
    print("This file should not be run directly")


class SaleItemConstructor():
    """ class for a sale item """

    def __init__(self):

        # init defaults
        self.supported_sites = ["Gumtree"]
        self.df_column_names = ['Site Title', 'Post Time','Description', 'Location', 'Price', 'Link']

    def generate_items_gumtree(self, site_object):

        sale_items = []

        class_string_of_items = 'user-ad-collection-new-design__wrapper--row'
        class_string_of_post_age = 'user-ad-row-new-design__age'

        site_title = self.supported_sites[0]

        # sanity check is for supported site
        for site in self.supported_sites:
            if site not in site_title:
                print("Web page parsed is not from a supported site")
                return False

        ad_sections = site_object.find_all(
            lambda tag: tag.name == 'div' and tag.get('class') == [class_string_of_items])

        main_section = ""

        for section in ad_sections:
            item_sample = section.find_all('a')[0]
            item_sample_describedby = item_sample.get('aria-describedby')
            if not item_sample_describedby == None:
                if "MAIN" in item_sample_describedby:
                    main_section = section
                    break

        for a in main_section.find_all('a'):
            # iterate through each item and collect info. Only get is posted in the last hour.

            # init sale item
            sale_item = {}

            # init defaults
            for name in self.df_column_names:
                sale_item[name] = ""

            post_age_div = a.find_all(
                lambda tag: tag.name == 'p' and tag.get('class') == [class_string_of_post_age])
            post_age_div_text = post_age_div[0].get_text()

            if 'minute' in post_age_div_text:
                mins_ago = float(post_age_div_text.split(" minute")[0])
                sale_item['Post Time'] = time_convertor.TimeClass()
                sale_item['Post Time'].gen_AEST(mins_ago)
            else:
                # post more then an hour old. Don't save. Assume already on file
                continue

            item_detail_string = a.get('aria-label')
            item_link = a.get('href')

            sale_item['Site Title'] = site_title

            split_string = item_detail_string.split("\n")
            sale_item['Description'] = split_string[0]

            split_string = item_detail_string.split("Location: ")
            sale_item['Location'] = split_string[1].split("\n")[0]

            split_string = item_detail_string.split("Price: ")
            sale_item['Price']= split_string[1].split("\n")[0]

            sale_item['Link'] = "https://www.gumtree.com.au" + item_link

            sale_items.append(sale_item)

        return sale_items


class ItemProcessor():
    """ class for processing items scrapped from web sites """


if __name__ == "__main__":
    main()
