# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

# TODO: Make a config file to load values from instead of hard codding


class SettingsClass():
    """ class for all varibles of the main that have hardcoded defaults """

    def __init__(self):
        # init defaults

        # flags
        self.pull_html = True
        self.email_notify = True       # flag to push notify to email
        self.wanted_items_key_word_check = True
        self.scrap_gumtree = True
        self.scrap_facebook_marketplace = False

        # email notify list
        self.email_list = ['lanebirmbetnotify@gmail.com']

        # general input variables
        self.df_column_names = ['Site Title', 'Post Time','Description', 'Location', 'Price', 'Link']

        #gumtree specific
        self.gumtree_urls = [
            "https://www.gumtree.com.au/s-bicycles/brisbane/c18560l3005721"]

        # facebook specific
        self.facebook_marketplace_urls = []  # to be generated from wanted items keywords

        # constants
        self.html_save_location_prefix = "html_files/html_"
        self.csv_save_location = "latest_data.csv"
        self.wanted_items_key_words = ["bike"]

        self.save_current_only = False


def main():
    # should not actually be run from here. import to different script
    print('SettingsClass should not be run directly')


if __name__ == '__main__':
    main()
