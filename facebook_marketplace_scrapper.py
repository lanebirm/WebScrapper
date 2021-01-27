# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

# facebook marketplace
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#from pymongo import MongoClient

import random
import time_convertor

# TODO: for debug code
import pickle


class App:
    def __init__(self, email="yuyan728@yahoo.com", password="889900",
                 path='Q:\Development\WebScrapper\facebook_save'):
        #TODO: Move email and password
        self.email = email
        self.password = password
        self.path = path
        self.df_column_names = []
        self.wanted_items_key_words = []
        self.scrap_time = ""

    def log_in(self):
        try:
            email_input = self.driver.find_element_by_id("email")
            emulate_typing(email_input, self.email, 0.5)
            sleep_random()
            password_input = self.driver.find_element_by_id("pass")
            emulate_typing(password_input, self.password, 0.5)
            sleep_random()
            login_button = self.driver.find_element_by_xpath(
                "//*[@type='submit']")
            login_button.click()
            sleep_random()
        except Exception:
            print(
                'Some exception occurred while trying to find username or password field')

    def marketplace_search(self, search_term):
        try:
            search_input = self.driver.find_element_by_xpath('//input[contains(@placeholder, "Search Marketplace")]')
            emulate_typing(search_input, search_term)
            sleep_random()
            search_input.send_keys(Keys.ENTER)
            sleep_random()
        except Exception:
            print(
                'Some exception occurred while trying to use marketplace search')

    def gen_sale_items(self, wanted_items_key_words, df_column_names):
        sale_items = []
        self.df_column_names = df_column_names
        self.wanted_items_key_words = wanted_items_key_words

        self.driver = webdriver.Firefox()
        self.main_url = "https://www.facebook.com"
        # self.client = MongoClient('mongodb://localhost:27017/')
        self.driver.get(self.main_url)
        self.log_in()
        self.used_item_links = []
        self.scrape_item_links(True, sale_items)
        # self.scrape_item_details_in_links(self.used_item_links)

        self.driver.quit()

        return sale_items

    def scrape_item_links(self, grab_item_details=False, sale_items=[]):
        marketplace_button = self.driver.find_element_by_xpath(
            "//*[@href='https://www.facebook.com/marketplace/?ref=bookmark']")
        marketplace_button.click()
        sleep_random()

        # create a list search items. May expand search structure in the future
        search_terms = self.wanted_items_key_words

        for term in search_terms:
            self.marketplace_search(term)
            # scroll down to get html of more items
            for i in range(6):
                try:
                    self.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    sleep_random()
                except:
                    pass

            full_items_list = self.driver.find_elements_by_xpath(
                "//a[contains(@href, '/marketplace/item/')]")

            # get time to set for all items 
            post_time = time_convertor.TimeClass()
            post_time.gen_AEST(0.0)
            self.scrap_time = post_time.local_time
            if grab_item_details:
                try:
                    title_divs = self.driver.find_elements_by_xpath(
                        '//div[contains(@class, "suyy3zvx")]')
                    for i, div in enumerate(title_divs):
                        
                        # init sale item
                        sale_item = {}

                        # init defaults
                        for name in self.df_column_names:
                            sale_item[name] = ""

                        titles_full_string = div.text
                        titles = titles_full_string.split("\n")

                        sale_item["Title"] = titles[1]
                        key_found = False
                        for key_word in self.wanted_items_key_words:
                            if key_word.lower() in sale_item['Title'].lower():
                                key_found = True
                                break
                        
                        if key_found == False:
                            # no key found in the description. Dont add item
                            continue

                        sale_item["Site Title"] = "Facebook Marketplace"
                        sale_item["Price"] = titles[0][2:]
                        sale_item['Description'] = titles[1] # set same as title for now
                        sale_item['Location'] = titles[2]
                        sale_item['Link'] = full_items_list[i].get_attribute('href')
                        
                        # can not scrap post time so set post time as first time scraped
                        sale_item['Post Time'] = self.scrap_time

                        sale_items.append(sale_item)
                except:
                    print("Failed to grab items on page. Script")
                    return sale_items

            if len(self.used_item_links) == 0:
                self.used_item_links = [item.get_attribute(
                    'href') for item in full_items_list]
            else:
                # append or extend or add?
                for item in full_items_list:
                    try:
                        self.used_item_links = self.used_item_links.extend(
                            [item.get_attribute('href')])
                    except:
                        continue

            # print([item.get_attribute('href') for item in full_items_list])

        # print(self.used_item_links)
        return self.used_item_links

    def scrape_item_details(self, used_item_links):

        for i, url in enumerate(used_item_links):

            # TODO: Debug code to not check all at the moment
            if i > 0:
                break

            images = []
            self.driver.get(url)
            sleep_random()

            url = url
            try:
                image_element = self.driver.find_element_by_xpath(
                    '//img[contains(@class, "x6m")]')
                images = [image_element.get_attribute('src')]
            except:
                images = ""
            try:
                title_div = self.driver.find_element_by_xpath(
                    '//div[contains(@class, "iscj3wi")]')
                titles_full_string = title_div.text
                titles = titles_full_string.split("\n")

                title = titles[0]
                price = titles[1][2:]
                category = titles[3]
                sub_category = titles[5]
                location = titles[6]
            except:
                title = ""
                price = ""
                category = ""
                sub_category = ""
                location = ""
            try:
                date_time = self.driver.find_element_by_xpath(
                    '//a[@class="_r3j"]').text
            except:
                date_time = ""
            try:
                if self.driver.find_element_by_xpath("//a[@title='More']").is_displayed():
                    self.driver.find_element_by_xpath(
                        "//a[@title='More']").click()
                description = self.driver.find_element_by_xpath(
                    '//p[@class="_4etw"]/span').text
            except:
                description = ""

            try:
                previous_and_next_buttons = self.driver.find_elements_by_xpath(
                    "//i[contains(@class, '_3ffr')]")
                next_image_button = previous_and_next_buttons[1]
                while next_image_button.is_displayed():
                    next_image_button.click()
                    image_element = self.driver.find_element_by_xpath(
                        '//img[contains(@class, "_5m")]')
                    sleep_random()
                    if image_element.get_attribute('src') in images:
                        break
                    else:
                        images.append(image_element.get_attribute('src'))
            except:
                pass

            print({'Url': url,
                   'Images': images,
                   'Title': title,
                   'Description': description,
                   'Date_Time': date_time,
                   'Location': location,
                   'Price': price,
                   'Category': category,
                   'Sub Category': sub_category,
                   })


def sleep_random(min_sleep=2, max_sleep=5):
    """
    Function to sleep for a random amount of time to reduce chances of scrapping being flagged as a bot on facebook

    """
    wait_time = random.randint(min_sleep, max_sleep) + random.random()
    if wait_time > max_sleep:
        wait_time = wait_time - 1

    sleep(wait_time)

def emulate_typing(web_element, string_to_type, max_time_per_key=1, min_time_per_key=0.2):
    """
    Function to emulate type keys into element
    """
    for character in string_to_type:
      sleep_time = random.random() * max_time_per_key
      if sleep_time < min_time_per_key:
        sleep_time = sleep_time + min_time_per_key
      sleep(random.random() * max_time_per_key)
      web_element.send_keys([character])


if __name__ == '__main__':
    app = App()
