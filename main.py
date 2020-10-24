# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

import pickle
import numpy as np
import pandas as pd

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
    sale_items.extend(IC.generate_items_gumtree(parsed_site_objects[0]))

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

    # check links to find matches
    prev_links = prev_sale_items_df["Link"]
    current_links = sale_items_df["Link"]

    if current_links[0] in prev_links:
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

    # trim to 50 items. Update csv
    current_sale_items_df = current_sale_items_df.head(50)
    current_sale_items_df.to_csv("latest_data.csv", index=False)

    email_df = current_sale_items_df

    # TODO: filter out "WANTED", etc. Will need to rethink check if new items as will have to skip the items to be filtered

    if settings.email_notify == True:
        msg = SimplyNotify.MIMEMultipart()
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
                'New Free Items', emails, input_msg=msg)

    return


def test():

    print("test finished")


if __name__ == "__main__":
    main()
    print("main finished")
    # test()
