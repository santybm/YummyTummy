#addIngredients.py

from bs4 import BeautifulSoup
from parse_rest.connection import register
from parse_rest.datatypes import Object as ParseObject
from parse_rest.connection import ParseBatcher
from datetime import datetime
import json,httplib,urllib
import time


class BU_All_Items(ParseObject):
    pass


APPLICATION_ID = "OaKii8zZrJDouyJcTe4d6VJuSleCfhWPtYxkjR1O"
REST_API_KEY = "oVHQ4xqopYCvhqvPnvPLknehNG9ctZwWv7OHYKk2"
MASTER_KEY = "M32h6B56OmAb2zq5FB1TOMAdI7TPU4d1JRwGcsrZ"


def getItemAddIngredient():
	#Get all items in a day
	


month = 00
day = 00
year = 2014

url = "http://www.bu.edu/dining/where-to-eat/residence-dining/marciano-commons/menu/?dsd=%(day)&dsm=%(month)&dsy=%(year)"