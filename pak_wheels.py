import scrapy
import os
import json

os.system("clear")


def get_attribute_safely(dictionary, attrib):
    """Returns None if attribute not found in dictionary

    Arguments:
        dictionary: dict:
            Dictionary that has values of the attributes
        attrib: string:
            Attribute whose value is required

    Returns:
         Value of attribute if exists, otherwise returns None
    """

    try:
        return dictionary[attrib]
    except KeyError:
        pass
    return None


def get_array_attribute_safely(dictionary, main_attrib, sub_attrib):
    """Returns None if attribute not found in dictionary

        Arguments:
            dictionary: dict:
                Dictionary that has values of the attributes
            main_attrib: string:
                Parent attribute to refer to child
            sub_attrib: string:
                Child attribute whose value is required

        Returns:
             Value of child attribute if exists, otherwise returns None
    """

    try:
        return dictionary[main_attrib][sub_attrib]
    except KeyError:
        pass
    return None


def get_clean_dictionary(dictionary):
    """Creates a clean dictionary with useful attribute

    Arguments:
        dictionary: dict:
            Dictionary from where arguments will be extracted

    Returns:
        dictionary: dict:
            Which contains all the required attributes
    """

    clean_dict = {}
    required_attributes = [
        ["Name", "name"],
        ["Description", "description"],
        ["Condition", "itemCondition"],
        ["Type", "@type"],
        ["Manufacturer", "manufacturer"],
        ["Fuel Type", "fuelType"],
        ["Model Date", "modelDate"],
        ["Image Url", "image"],
        ["Vehicle Transmission", "vehicleTransmission"],
        ["Mileage", "mileageFromOdometer"]
    ]

    for name, attribute in required_attributes:
        value = get_attribute_safely(dictionary, attribute)
        if value is not None:
            clean_dict[name] = value

    required_child_attributes = [
        ["Engine Displacement", "vehicleEngine", "engineDisplacement"],
        ["Url", "offers", "url"]
    ]

    for name, parent_attrib, child_attrib in required_child_attributes:
        value = get_array_attribute_safely(dictionary, parent_attrib,
                                           child_attrib)
        if value is not None:
            clean_dict[name] = value

    price = get_array_attribute_safely(dictionary, "offers", "price")
    currency = get_array_attribute_safely(dictionary, "offers",
                                          "priceCurrency")
    if price is not None and currency is not None:
        clean_dict["Price"] = str(price) + str(currency)
    elif price is not None:
        clean_dict["Price"] = price
    return clean_dict


class PakWheelsCrawler(scrapy.Spider):
    """This class is used to crawl website using
    scrapy
    """

    name = "pak_wheels"

    def __init__(self):
        self.base_url = "https://www.pakwheels.com"
        self.dots = 0
        self.dot_limit = 5
        super().__init__()

    def start_requests(self):
        """This method is called by spider automatically
        to start crawl
        """

        used_cars_url = "https://www.pakwheels.com/used-cars/search/"
        used_cars_url += "-/featured_1/"
        new_cars_url = "https://www.pakwheels.com/new-cars/search/"
        new_cars_url += "make_any/model_any/price_any_any/?page=1&"
        new_cars_url += "sortby=price+ASC"
        yield scrapy.Request(url=used_cars_url,
                             callback=self.parse_used_cars)
        yield scrapy.Request(url=new_cars_url,
                             callback=self.parse_new_cars)

    def parse_used_cars(self, response):
        """Parse used car information

        Arguments:
            Receives a response from scrapy.Request

        Returns:
            Yields dictionaries with clean data
        """

        xpath_to_data = "//div[@class='search-page-new']//"
        xpath_to_data += "div[@class='row']/div[2]/div[2]/ul/li/"
        xpath_to_data += "script/text()"
        complete_data_in_json = response.xpath(xpath_to_data).getall()

        for vehicle_data in complete_data_in_json:
            json_data = json.loads(vehicle_data)
            yield get_clean_dictionary(json_data)

        next_page_link = response.xpath("//li[@class='next_page']/a//@href")\
            .get()

        self.dots = (self.dots % self.dot_limit) + 1
        print("\rWorking" + "." * self.dots + "          ", end='\r')
        if next_page_link is not None:
            next_page_link = self.base_url + next_page_link
            yield scrapy.Request(url=next_page_link,
                                 callback=self.parse_used_cars)

    def parse_new_cars(self, response):
        """Parse used car information

        Arguments:
            Receives a response from scrapy.Request

        Returns:
            Yields dictionaries with clean data
        """

        xpath_to_data = "//div[@class='search-page-new']//"
        xpath_to_data += "div[@class='row']/div[2]/ul[1]/li/"
        xpath_to_data += "script/text()"
        complete_data_in_json = response.xpath(xpath_to_data).getall()
        next_page_link = response.xpath("//li[@class='next_page']/a//@href") \
            .get()

        for vehicle_data in complete_data_in_json:
            json_data = json.loads(vehicle_data)
            yield get_clean_dictionary(json_data)

        self.dots = (self.dots % self.dot_limit) + 1
        print("\rWorking" + "." * self.dots + "          ", end='\r')

        if next_page_link is not None:
            next_page_link = self.base_url + next_page_link
            yield scrapy.Request(url=next_page_link,
                                 callback=self.parse_new_cars)
