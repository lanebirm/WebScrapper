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

    def __init__(self, df_column_names):

        # init defaults
        self.supported_sites = ["Gumtree"]
        self.df_column_names = df_column_names

    def generate_items_gumtree(self, site_object, key_description_words=[]):

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
                post_time = time_convertor.TimeClass()
                post_time.gen_AEST(mins_ago)
                sale_item['Post Time'] = post_time.local_time
            else:
                # post more then an hour old. Don't save. Assume already on file
                continue

            item_detail_string = a.get('aria-label')

            split_string = item_detail_string.split("\n")
            sale_item['Description'] = split_string[0]

            # if key words given then check if in description. If not dont add item
            if len(key_description_words) > 0:
                key_found = False
                for key_word in key_description_words:
                    if key_word.lower() in sale_item['Description'].lower():
                        key_found = True
                        break
                
                if key_found == False:
                    # no key found in the description. Dont add item
                    continue

            sale_item['Site Title'] = site_title

            split_string = item_detail_string.split("Location: ")
            sale_item['Location'] = split_string[1].split(" Ad")[0]

            split_string = item_detail_string.split("Price: ")
            sale_item['Price']= split_string[1].split("\n")[0]

            item_link = a.get('href')
            sale_item['Link'] = "https://www.gumtree.com.au" + item_link

            sale_items.append(sale_item)

        return sale_items


class ItemProcessor():
    """ class for processing items scrapped from web sites """


if __name__ == "__main__":
    main()
