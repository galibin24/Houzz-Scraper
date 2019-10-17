# -*- coding: utf-8 -*-
# from __future__ import absolute_import

import scrapy

from scrapy.utils.project import get_project_settings

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
import json
import js2xml
import lxml.etree
from parsel import Selector
from collections import OrderedDict
from ast import literal_eval
from scrapy.selector import Selector
import pandas as pd 
import re
from houzagainv2.items import HouzzAgainItem



item = HouzzAgainItem()

class MainSpider(CrawlSpider):
    name = 'main'
    domain = 'https://www.houzz.com/professionals'

    def __init__(self, *args, **kwargs): 
      global item
      super(MainSpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('start_url')]

    # custom_settings = {
    #             'CLOSESPIDER_ITEMCOUNT': 2000,
    #             }
    domains = ['https://www.houzz.com']
    rules = (
    Rule(LinkExtractor(restrict_xpaths='//*[contains(concat( " ", @class, " " ), concat( " ", "hz-pagination-link--next", " " ))]'), follow=True , callback='parse_item'),
)

    def parse_item(self, response):
        result = re.search('&location=(.*)&distance=', self.start_urls[0])
        city = result.group(1)
        city = city.replace('%2C+', ' ')
        item['City'] = city
        links = response.css('.text-unbold::attr(href)').getall()
        for i in links:
            yield scrapy.Request(i, callback = self.main_parse)

    def main_parse(self, response):
        global item
        data = response.xpath('//*[@id="hz-ctx"]//text()').get()
        data = json.loads(data) 
        json_string = json.dumps(data, indent=4, ensure_ascii= False)
        data2 = json.loads(json_string)
        data3 = data2['data']['stores']['data']['PageStore']['data']['pageDescriptionFooter']
        data3 = data3.replace('<runnable type="application/ld+json">', '')
        data3 = data3.replace('</runnable>', '')
        data4 = json.loads(data3)

        for i in data4:
            
            i = json.dumps(i, indent=4, ensure_ascii= False)
            i = json.loads(i)

            Phone_Number = data2['data']['stores']['data']['UserProfileStore']['data']['user']['professional']['formattedPhone']
            Phone2 = i['telephone']
            print(Phone2)
            Company_Website = i['url']
            Company_name = i['name']
            Services_provided = i['hasOfferCatalog']['name']
            Company_Description = i['description']
            Area_served = i['areaServed']['name']
            Company_link = response.url

            try:
                Number_of_Reviews = response.xpath('//*[contains(concat( " ", @aria-label, " " ), concat( " ", "Average", " " ))][1]/@aria-label').get()
            except:
                Number_of_Reviews = 'Nan'
            try:
                Number_of_stars = response.xpath('//*[contains(concat( " ", @aria-label, " " ), concat( " ", "Average", " " ))][1]//text()').get()
            except:
                Number_of_stars = 'Nan'
            try:
                Awards = response.xpath('//*[contains(text(), "Awards")][1]/../p//text()').get()
            except:
                Awards = "Nan"
            
            Category = response.xpath('//*[contains(text(), "Category")]/../div/a//text()').getall()
            Category = ''.join(Category)
            Category = Category.strip()
         
            try:
                Job_cost = response.xpath('//*[contains(text(), "Typical Job Costs:")]/../div[2]//text()').getall()
            except:
                Job_cost = 'Nan'
            try:
                License_number = response.xpath('//*[contains(text(), "License Number")]/../div[2]//text()').get()
            except:
                License_number = 'Nan'
            try:
                Contact_Info = response.xpath('//*[contains(text(), "Contact Info")]/../div[2]//text()').getall()
            except:
                Contact_Info = 'Nan'
            try:
                Profile_img = response.css('.hz-profile-photo__avatar-img::attr(src)').get()
            except:
                Profile_img = 'Nan'
            try:
                Background_img = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "hz-cover-photo__overlay", " " ))]/..//@style').get()
                Background_img = Background_img[Background_img.find("(")+1:Background_img.find(")")]
            except:
                Background_img = 'Nan'

            item['Company_Name'] = Company_name
            item['Company_Description'] = Company_Description
            item['Phone_Number'] = Phone_Number
            item['Company_Website'] = Company_Website
            item['Services_provided'] = Services_provided
            item['Address'] = Contact_Info
            item['Areas_Served'] = Area_served
            item['Number_of_Reviews'] = Number_of_stars 
            item['Number_of_stars'] = Number_of_Reviews 
            item['Category'] = Category
            item['Job_Cost'] = Job_cost
            item['License_number'] = License_number
            item['Awards'] = Awards
            item['Company_link'] = Company_link
            item['Profile_img'] = Profile_img
            item['Background_img'] =  Background_img
            item['Phone2'] = Phone2
            yield item

     