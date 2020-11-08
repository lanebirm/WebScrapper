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


def main():

    settings = settings_file.SettingsClass()

    WS = web_scrapper.WebScrapper()

    sale_items = []
    parsed_site_objects = []

    email_notify = settings.email_notify

    # database connection # TODO
    # conn = sqlite3.connect('sale_items.db')

    for i, url in enumerate(settings.urls):
        if settings.pull_html:
            # get BeautifulSoup parsed format of web sites. saved to /html_files folder
            parsed_site_object = WS.parse_site_bs(
                url,  (settings.html_save_location_prefix + str(i) + ".html"))
            parsed_site_objects.append(parsed_site_object)
        else:
            parsed_site_objects.append(WS.parse_local_file_bs(
                settings.html_save_location_prefix + str(i) + ".html"))

    IC = items_structures.SaleItemConstructor()

    # gumtree items generated
    for soup in parsed_site_objects:
        sale_items.extend(IC.generate_items_gumtree(soup, settings.wanted_items_key_words))

    # if no new sale items exit script
    if len(sale_items) < 1:
        print("No sale items found. Exiting")
        return True

    sale_items_df = pd.DataFrame(sale_items)

    if settings.save_current_only == True:
        # saves what was just pulled only
        sale_items_df.to_csv("latest_data.csv", index=False)
        return True

    # load currently saved list and compare to what was jsut scraped
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
                    if word in row[1]["Description"]:
                        # keyword match found. 
                        # now check if already found previously
                        if not prev_sale_items_df.isin([row[1]["Link"]]).any().any():
                            # not previously scrapped. New item. Email notify
                            email_notify = True
                            break
    else:
        # check links to find matches
        current_links = sale_items_df["Link"]
        if prev_sale_items_df.isin([current_links[0]]).any().any():
            # latest post is already saved in prev_links. No update needed
            print('Items list is up to date')
            return True

    # new item avaliable. Replace all last hour items and
    time_one_hour_ago = time_convertor.TimeClass()
    time_one_hour_ago.gen_AEST(60.0)

    cut_index = -1
    for index, row in prev_sale_items_df.iterrows():
        if row["Post Time"] < time_one_hour_ago.local_time:
            # row post time is older than an hour
            cut_index = index
            break

    current_sale_items_df = ""
    if cut_index == -1:
        # no old posts found. Just use new list
        current_sale_items_df = sale_items_df
    else:
        if cut_index != 0:
            # trim prev_sale_items_df to only items over an hour old
            prev_sale_items_df = prev_sale_items_df.tail(-cut_index)

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

        # Attach links to pages scrapped
        links_string = "Links Scrapped Are: \n"
        for link in settings.urls:
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

    return


def test():

    print("test finished")


if __name__ == "__main__":
    main()
    print("main finished")
    # test()
