# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020

# TODO: Make a config file to load values from instead of hard codding


class SettingsClass():
    """ class for all varibles of the main that have hardcoded defaults """

    def __init__(self):
        # init defaults

        # flags
        self.pull_html = False

        # input variables
        self.urls = ["https://www.gumtree.com.au/s-brisbane/l3005721?sort=rank&price-type=free"]

def main():
    # should not actually be run from here. import to different script
    print('SettingsClass should not be run directly')


if __name__ == '__main__':
    main()
