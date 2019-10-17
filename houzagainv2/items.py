# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field
from collections import OrderedDict

class OrderedItem(Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

class HouzzAgainItem(OrderedItem):
    Company_Name = Field()
    Company_Description = Field()
    Phone_Number = Field()
    Company_Website = Field()
    Services_provided = Field()
    Address = Field()
    Areas_Served = Field()
    Number_of_Reviews = Field()
    Number_of_stars = Field()
    Category = Field()
    Job_Cost = Field()
    License_number = Field()
    Awards = Field()
    Company_link = Field()
    City = Field()
    Profile_img = Field()
    Background_img = Field()
    Phone2 = Field()



    pass
