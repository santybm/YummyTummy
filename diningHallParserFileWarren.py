#!/usr/bin/env python
#Import Statements
#Using Requests, Beautifulsoup4, and JSON(REST) via Parse_REST
from bs4 import BeautifulSoup
import urllib2
from parse_rest.connection import register
from parse_rest.datatypes import Object as ParseObject
from parse_rest.connection import ParseBatcher
from datetime import datetime
import json,httplib,urllib
import time

#Setup Classes
class BU_All_Items(ParseObject):
    pass

class BU_Weekly_Menu(ParseObject):
    pass

APPLICATION_ID = "OaKii8zZrJDouyJcTe4d6VJuSleCfhWPtYxkjR1O"
REST_API_KEY = "oVHQ4xqopYCvhqvPnvPLknehNG9ctZwWv7OHYKk2"
MASTER_KEY = "M32h6B56OmAb2zq5FB1TOMAdI7TPU4d1JRwGcsrZ"

register(APPLICATION_ID, REST_API_KEY)

def getDiningURLs():

	#Get dining hall menus from each of the dining halls
	#  - Get dining hall name
	#  - Get dates starting on Monday to Sunday
    DHName = "http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/"
	#Get the HTML object from DHName webpage
    #DHURL = {'1':"http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/",'2':"http://www.bu.edu/dining/where-to-eat/residence-dining/marciano-commons/menu/", '3':"http://www.bu.edu/dining/where-to-eat/residence-dining/the-fresh-food-co-at-west-campus/menu/"}
    DHURL = {'1':"http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/"}
    soupObjects = {}
    for key, url in DHURL.iteritems():
            soupObjects[key]=BeautifulSoup(urllib2.urlopen(url))	
    css_soups = {}
    for key, stew in soupObjects.iteritems():
            css_soups[key]=stew.find(class_= "dining-menu-nav")

    #Get the URLs for each date
    dateNURL = {}
    for key, cssSoup in css_soups.iteritems():
            for a in cssSoup.find_all('a', href=True):
                    urlString = a['href']
                    monthDate = urlString[(urlString.find('&dsm=')+5):urlString.find('&dsy')]
                    if (int(monthDate) < 10):
                            monthDate = '0' + monthDate
                    LocDate = (key + ":" + monthDate + " " + urlString[(urlString.find('=')+1):urlString.find('&dsm')])
                    dateNURL[LocDate]= ('http://www.bu.edu' + a['href'])
    #Returns dictionary of [location+Date:URL of dining hall menu for that date]	
    return dateNURL

def getRAWHTML_MealSection(strURL):
	r1 = urllib2.urlopen(strURL)
	menuSoup = BeautifulSoup(r1)
	menuSoup = menuSoup.find(class_="dining-menu-meals")
	#Get menu by meals if available:
	#get Breakfast soup
	breakfastSoup = menuSoup.find(class_="mealgroup breakfast")
	if (breakfastSoup is not None):
		breakfastSoup = breakfastSoup.find(class_="insidecontainer")
	#get Lunch Soup
	lunchSoup = menuSoup.find(class_="mealgroup lunch")
	if (lunchSoup is not None):
		lunchSoup = lunchSoup.find(class_="insidecontainer")
	#get Dinner Soup
	dinnerSoup = menuSoup.find(class_="mealgroup dinner")
	if (dinnerSoup is not None):
		dinnerSoup = dinnerSoup.find(class_="insidecontainer")
	
	#Return meal soups
	mealSoup = {'B':breakfastSoup, 'L':lunchSoup, 'D':dinnerSoup}
	return mealSoup

def specialPropertiesFinder(item):
	specialProps = []
	vegan = item.find(class_='vegan-icon menuitem-icon')
	if (vegan is not None): 
		specialProps.append(1)
	vegetarian = item.find(class_='vegetarian-icon menuitem-icon')
	if (vegetarian is not None): 
		specialProps.append(2)
	glutenFree = item.find(class_='glutenfree-icon menuitem-icon')
	if (glutenFree is not None): 
		specialProps.append(3)
	sargent = item.find(class_='sargent-icon menuitem-icon')
	if (sargent is not None): 
		specialProps.append(4)
	if not specialProps:
		specialProps.append(0)
	return specialProps
#Input Parameters: Item Nutrition ID
#Output Parameters: ObjectID if exists; None if does not exist
def getItemObjectID(itemNutriID):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"where":json.dumps({"NutID": itemNutriID})})
	connection.connect()
	connection.request('GET', '/1/classes/BU_All_Items?%s' % params, '', {
       	"X-Parse-Application-Id": APPLICATION_ID,
       	"X-Parse-REST-API-Key": REST_API_KEY})
	result = json.loads(connection.getresponse().read())
	#print result
	#Check if result is null // aka Item doesn't exist
	if not result['results']:
		#print 'No Results Found'
		return None
	else:
		tempList = result['results']
		tempDict = tempList[0]
		return tempDict['objectId']
#Separate the Menu Items.
#INPUTS: HTML Code as BS4 Objects, diningID(1,2,3), and the mealTimeID (B,L,D)
#OUTPUTS parseAllItems: A list of dictionary objects containing {url, BU_All_Items(object)}
def getEachItem(rawSoup, diningID, mealTimeID):
	for station in rawSoup.find_all(class_="station"):
		#print station.get('id')
		stationName = station.get('id')
		stationName = stationName[:stationName.find("-")]
		itemSoup = station.find(class_="items")
		TimeID = diningID[2:]
		TimeID = datetime.strptime(str(datetime.now().year) + " " + TimeID,'%Y %m %d')
		#print itemSoup.find('item-menu-name')		
		for item in itemSoup.find_all('a'):
			#itemParse = {}
			#menuItemList = {}
			calories = item.find(class_='item-calories').get_text()
			calories = calories[:(calories.find(" C"))]
			if calories == 'n/a':
				calories = 0
			satFat = item.find(class_='item-satfat').get_text()
			satFat = satFat[:(satFat.find(" S"))]
			name = item.find(class_='item-menu-name').get_text()
			specProps = specialPropertiesFinder(item)
			url = item.get('href')
			url = url[(url.find("-")+1):]
			#print ("FOR YOUR REFERENCE:  DiningID: " + diningID[:1] + ", and mealTimeID: " + mealTimeID) 
			#FORMAT: itemProps[url] = [diningID, mealTimeID, stationName,name, url, specProps, calories, satFat]
			itemParse = BU_All_Items(ItemName=name,NutID=url,SpecialProperties=specProps,Calories=float(calories),SatFat=float(satFat), UserRating=0)
			#Save the items to All list
			try:
				itemQuery = getItemObjectID(itemParse.NutID)
			except:
				try:
					itemQuery = getItemObjectID(itemParse.NutID)
				except:
					itemQuery = getItemObjectID(itemParse.NutID)
			print (name)			
			print ("****************")
			print itemQuery
			if itemQuery is None:
				print ("!!!!!!!!!!!!!!!!!!!!!! NOT FOUND !!!!!!")
				try:
					itemParse.save()
				except:
					try:
						itemParse.save()
					except:
						itemParse.save()
				menuItemList = BU_Weekly_Menu(DateAvailable=TimeID, MealTimeAvailable=mealTimeID, hallID=int(diningID[:1]), station=stationName, NutritionItem=itemParse)
				allMenuItems.append(menuItemList)
				print (url + "Added to list and menu")
			else:
				print ("!!!!!!!!!!!!!!!!!!!!!! FOUND !!!!!!")
				try:
					allItemsObject = BU_All_Items.Query.get(objectId=itemQuery)
				except:
					try:
						allItemsObject = BU_All_Items.Query.get(objectId=itemQuery)
					except: 
						allItemsObject = BU_All_Items.Query.get(objectId=itemQuery)
				print allItemsObject
				menuItemList = BU_Weekly_Menu(DateAvailable=TimeID, MealTimeAvailable=mealTimeID, hallID=int(diningID[:1]), station=stationName, NutritionItem=allItemsObject)
				allMenuItems.append(menuItemList)
				#menuItemList.save()
				print (url + "Added to Menu")
			#list containing dictionary of parseAllItems[{url:BU_All_Items Object}]
			#parseAllItems.append(itemParse)
			#allMenuItems.append(menuItemList)

def processDateMenus():
	#Gets the URL for every date and dining hall to read the menus
	dateURLDict = getDiningURLs()
	#print Date
	for key,url in dateURLDict.iteritems():
		print key + ":" + url
		#Call item getter. Gets every item on the menu
		mealTimeCode = getRAWHTML_MealSection(url)
		for mealKey, mealTime in mealTimeCode.iteritems():
			if (mealTime is not None):
				#Send the mealTime Soup object, the Date and location ID, and the meal (b,l,d)				
				getEachItem(mealTime,key,mealKey)
		#Filter duplicated to store in the all items class in Parse -- Returns a list of item objects		
		#filteredSet = getAllUniqueItems(parseAllItems)
		#print(filteredSet)
		#Save to Parse
		#parseList = list(filteredSet)
		#print(parseList)
		#saveToParse(parseList)
		batcher = ParseBatcher()
		#batcher.batch_save(parseList)
		#batcher.batch_save(allMenuItems)
		tempList = []
		for i in range(len(allMenuItems)):
			if ( i%50 is not 0):
				tempList.append(allMenuItems[i])
			else:
				allMenuItems[i].save()
				if (len(tempList) is not 0):
					try:
                                            time.sleep(2)
                                            batcher.batch_save(tempList)
					except:
                                            time.sleep(2)
                                            batcher.batch_save(tempList)
				tempList = []
				print ("Save batch")
		if (len(tempList) is not 0):
			try:
                                time.sleep(2)
				batcher.batch_save(tempList)
			except:
                                time.sleep(2)
				batcher.batch_save(tempList)
			tempList = []
			print ("Save batch")
			
		print("Done")
		


# key = BU_Food_Items() object
def getAllUniqueItems(menuToFilter):
	#This gets all the unique keys into on set [{url:object},{url:object}] where every url is unique 
	uniqueItems = set(val for dic in menuToFilter for val in dic.values())
	return uniqueItems

#store all items in list
def saveToParse(listOfObjects):
	#Get all unique items, saved to global variable uniqueItems
	#getAllUniqueItems()
	#Configure Parse API
	APPLICATION_ID = "OaKii8zZrJDouyJcTe4d6VJuSleCfhWPtYxkjR1O"
	REST_API_KEY = "oVHQ4xqopYCvhqvPnvPLknehNG9ctZwWv7OHYKk2"
	MASTER_KEY = "M32h6B56OmAb2zq5FB1TOMAdI7TPU4d1JRwGcsrZ"

	register(APPLICATION_ID, REST_API_KEY)
	#list containing lists of 50 BU_All_Items objects
	#objList = []
	#FORMAT: uniqueItems = [{url:Object},{url:Object}]
	#counter = 1
	#for itemDict in uniqueItems:	
	#	for key, itemObject in itemDict.iteritems():
	#		#Create Batch of 50 objects per list
	#		if (counter % 50 == 0):
	#			print("I'm Here")
	#			objList.append(itemObject)			
	#			batcher = ParseBatcher()
	#			batcher.batch_save(objList)
	#			objList = []
	#		else:
	#			#Store to list	
	#			objList.append(itemObject)
	#			counter += 1
	batcher = ParseBatcher()
	batcher.batch_save(listOfObjects)
	print ("Done")
	

#allItems = []
parseAllItems = []
allMenuItems = []
uniqueItems = set()
processDateMenus()
#saveToParse()
