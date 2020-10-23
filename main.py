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

    sale_items_df = pd.DataFrame(sale_items)

    if settings.save_current_only == True:
        # saves what was just pulled only
        sale_items_df.to_csv("latest_data.csv", index=False)
        return True

    # load currently saved list and compare to what was jsut scraped
    prev_sale_items_df = pd.DataFrame()
    try:
        prev_sale_items_df = pd.read_csv(settings.csv_save_location)
    except:
        print("Could not load csv")

    match_index = -1
    for index, row in sale_items_df.iterrows():
        # iterate through each row and compare until up to date with previously found items i.e. first row of saved values
        if row["Link"] == prev_sale_items_df["Link"][0]:
            # add all entries before this row to previous list
            match_index = index
            break

    # if no match found add all items to outgoing sale item df
    items_to_add = pd.DataFrame()
    if match_index == -1:
        # no item match found. Add all to list
        items_to_add = sale_items_df
    elif match_index == 0:
        # match found at first index. List is up to date. Dont update and don't email notify
        print('Items list is up to date')
        return True
    else:
        # only take top entries above match
        items_to_add = sale_items_df.head(match_index)

    # Concatenating DataFrames
    prev_sale_items_df = prev_sale_items_df.reset_index(drop=True)
    items_to_add = items_to_add.reset_index(drop=True)
    current_sale_items_df = pd.concat(
        [items_to_add, prev_sale_items_df], axis=0, sort=False)
    current_sale_items_df = current_sale_items_df.reset_index(drop=True)

    # update csv
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


    print("main finished")

    return


def test():

    print("test finished")


if __name__ == "__main__":
    main()
    # test()
