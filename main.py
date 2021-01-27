# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

from os import set_inheritable
import pickle
import numpy as np
import pandas as pd
import sqlite3 

# python script imports
import settings as settings_file
import web_scrapper
import items_structures
import simple_notifications as SimplyNotify
import time_convertor
import facebook_marketplace_scrapper


def main():

    settings = settings_file.SettingsClass()

    WS = web_scrapper.WebScrapper()

    sale_items = []
    parsed_site_objects = []

    email_notify = settings.email_notify

    # GUMTREE ITEM SCRAPPING
    if settings.scrap_gumtree:
        for i, url in enumerate(settings.gumtree_urls):
            if settings.pull_html:
                # get BeautifulSoup parsed format of web sites. saved to /html_files folder
                parsed_site_object = WS.parse_site_bs(
                    url,  (settings.html_save_location_prefix + str(i) + ".html"))
                parsed_site_objects.append(parsed_site_object)
            else:
                parsed_site_objects.append(WS.parse_local_file_bs(
                    settings.html_save_location_prefix + str(i) + ".html"))

        IC = items_structures.SaleItemConstructor(settings.df_column_names)

        # gumtree items generated
        for soup in parsed_site_objects:
            sale_items.extend(IC.generate_items_gumtree(soup, settings.wanted_items_key_words))

    # FACEBOOK ITEM SCRAPPING
    if settings.scrap_facebook_marketplace:
        FWS = facebook_marketplace_scrapper.App()
        sale_items.extend(FWS.gen_sale_items(settings.wanted_items_key_words, settings.df_column_names))

    # if no new sale items exit script
    if len(sale_items) < 1:
        print("No sale items found. Exiting")
        return True

    sale_items_df = pd.DataFrame(sale_items)

    if settings.save_current_only == True:
        # saves what was just pulled only
        sale_items_df.to_csv("latest_data.csv", index=False)
        return True

    # load currently saved list and compare to what was just scraped
    prev_sale_items_df = pd.DataFrame()
    try:
        prev_sale_items_df = pd.read_csv(settings.csv_save_location)
        prev_sale_items_df["Post Time"] = pd.to_datetime(
            prev_sale_items_df["Post Time"])
    except:
        print("Could not load csv")

    # Check through new items against wanted items list to decide if an email notification is needed
    if email_notify and settings.wanted_items_key_word_check:
        # email notify enabled in settings. Now check through wanted item keyword list
        # set to false then will be set back if key word match is found
        email_notify = False
        if len(settings.wanted_items_key_words) > 0:
            for word in settings.wanted_items_key_words:
                for row in sale_items_df.iterrows():
                    if word.lower() in row[1]["Description"].lower():
                        # keyword match found. 
                        # now check if already found previously
                        if not prev_sale_items_df.isin([row[1]["Link"]]).any().any():
                            # not previously scrapped. New item. Email notify
                            email_notify = True
                            break
    else:
        # check links to find matches
        current_links = sale_items_df["Link"].to_list()
        if prev_sale_items_df.isin([current_links[0]]).any().any():
            # latest post is already saved in prev_links. No update needed
            print('Items list is up to date')
            return True

    # check if links previously found. If so then remove from sale_items_df
    item_links = sale_items_df["Link"].to_list()
    prev_item_links = prev_sale_items_df["Link"].to_list()
    drop_indexes = []
    for i, link in enumerate(item_links):
        if link in prev_item_links:
            drop_indexes.append(i)
    # drop previously found items
    sale_items_df.drop(drop_indexes, inplace=True)

    # Concatenating DataFrames
    prev_sale_items_df = prev_sale_items_df.reset_index(drop=True)
    sale_items_df = sale_items_df.reset_index(drop=True)
    current_sale_items_df = pd.concat(
        [sale_items_df, prev_sale_items_df], axis=0, sort=False)
    current_sale_items_df = current_sale_items_df.reset_index(drop=True)

    # trim to 100 items. Update csv
    current_sale_items_df = current_sale_items_df.head(100)
    current_sale_items_df.to_csv("latest_data.csv", index=False)

    email_df = current_sale_items_df

    if email_notify == True:
        msg = SimplyNotify.MIMEMultipart()

        disclaimer = "NOTE: Post time for facebook items is the time it is first scrapped as can not scrap an accurate time from listing \n"

        # Attach links to pages scrapped
        if settings.scrap_gumtree:
            links_string = "Links Scrapped on Gumtree Are: \n"
            for link in settings.gumtree_urls:
                links_string = links_string + link + "\n"
            msg.attach(SimplyNotify.MIMEText(
                links_string))
        
        # Attach Key phrases checked
        key_phrases_string = "\nKey phrases checked are: \n"
        for link in settings.wanted_items_key_words:
            key_phrases_string = key_phrases_string + link + "\n"
        msg.attach(SimplyNotify.MIMEText(
            key_phrases_string))

        # Gen df in email form
        html = """\
            <html>
            <head></head>
            <body>
                {0}
            </body>
            </html>
            """.format(email_df.to_html())
        table_as_string = SimplyNotify.MIMEText(html, 'html')

        msg.attach(table_as_string)

        for emails in settings.email_list:
            SimplyNotify.email(
                'New Items', emails, input_msg=msg)
    elif settings.email_notify:
        print("No new items. Don't email notify")

    return


def test():

    print("test finished")


if __name__ == "__main__":
    main()
    print("main finished")
    # test()
