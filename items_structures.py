# Python 3.8.0

# Author: Lane Birmingham
# Date 20/10/2020


# python script imports


def main():
    print("This file should not be run directly")


class SaleItem():
    """ Class for a sale item found the on scrapped sites or loaded from file """

    def __init__(self):

        # init defaults
        self.site_title = ""
        self.location = ""
        self.description = ""
        self.price = ""
        self.link = ""

    def __repr__(self) -> str:
        # what is printed when SaleItem print call is made
        return "\nSite Title: %r\n Location: %r\n Description: %r\n Price: %r\n Link: %r" % (self.site_title, self.location, self.description, self.price, self.link)


class SaleItemConstructor():
    """ class for a sale item """

    def __init__(self):

        # init defaults
        self.supported_sites = ["Gumtree"]

    def generate_items_gumtree(self, site_object):

        sale_items = []

        class_string_of_items = 'user-ad-collection-new-design__wrapper--row'

        site_title = site_object.title.string

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
            # iterate through each item and collect info

            item_detail_string = a.get('aria-label')
            item_link = a.get('href')

            sale_item = SaleItem()

            sale_item.site_title = site_title

            split_string = item_detail_string.split("\n")
            sale_item.description = split_string[0]

            split_string = item_detail_string.split("Location: ")
            sale_item.location = split_string[1].split("\n")[0]

            split_string = item_detail_string.split("Price: ")
            sale_item.price = split_string[1].split("\n")[0]

            sale_item.link = "https://www.gumtree.com.au" + item_link

            sale_items.append(sale_item)
            print(str(sale_items))

        return True


if __name__ == "__main__":
    main()
