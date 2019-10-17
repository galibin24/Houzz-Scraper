#!/usr/bin/env python

import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy
import pandas as pd 

country = input(' Please write country abriviation name (e.g. United Kindom = UK) : ')
city = input ( 'Write the name of the city : '  ) 
process = CrawlerProcess(get_project_settings())

def runspider(link):
    process.crawl('main', start_url=link)    

link = 'https://www.houzz.com/professionals/searchDirectory?topicId=1200&query=All+Professionals&location=' +  city + '%2C+' + country + '&distance=50&sort=4'
runspider(link)
process.start()

import parser.py