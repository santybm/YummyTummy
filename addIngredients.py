#addIngredients.py

#from bs4 import BeautifulSoup
from parse_rest.connection import register
from parse_rest.datatypes import Object as ParseObject
from parse_rest.connection import ParseBatcher
from datetime import datetime, date
import json,httplib,urllib
import urllib2
from bs4 import BeautifulSoup
import time
import pickle
import csv
import operator
from parse_rest.datatypes import Object as ParseObject
class NutritionLabel(ParseObject):
	pass

class Item(ParseObject):
	pass

class BU_All_Items(ParseObject):
	pass

class _User(ParseObject):
	pass

class User(ParseObject):
	pass

class Tummy(ParseObject):
	pass


APPLICATION_ID = "OaKii8zZrJDouyJcTe4d6VJuSleCfhWPtYxkjR1O"
REST_API_KEY = "oVHQ4xqopYCvhqvPnvPLknehNG9ctZwWv7OHYKk2"
MASTER_KEY = "M32h6B56OmAb2zq5FB1TOMAdI7TPU4d1JRwGcsrZ"
#register(APPLICATION_ID, REST_API_KEY)
register("ab2PDO430oZeLB4cI4GAUFjdWcgKGtJcQUe291UW", "7mjGlKBqovrJxgZY6osHZMkET4AlXlgpyiroNCYl")

def getItemAddIngredient():
	#Get all items in a day
	datetime = ()
	BUItems = {}
	BUItemsList = []

	all_day_items = BU_All_Items.Query.filter(ingridentsList=None)

	page1k = all_day_items.limit(1000)
	page2k = all_day_items.skip(1000).limit(2000)

	for item in page1k:
		complexDate = item.createdAt
		simpleDate = date(int(complexDate.year), int(complexDate.month), int(complexDate.day))

		if simpleDate in BUItems:
			BUItems[simpleDate].append(item)
		else:
			BUItems[simpleDate] = [item]

	for item in page2k:
		complexDate = item.createdAt
		simpleDate = date(int(complexDate.year), int(complexDate.month), int(complexDate.day))

		if simpleDate in BUItems:
			BUItems[simpleDate].append(item)
		else:
			BUItems[simpleDate] = [item]


	for eachDay in BUItems:
		print eachDay
		month = str(eachDay.month)
		day = str(eachDay.day)
		year = str(eachDay.year)
		

		DHURL = {'war':"http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year,'bay':"http://www.bu.edu/dining/where-to-eat/residence-dining/marciano-commons/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year, 'wes':"http://www.bu.edu/dining/where-to-eat/residence-dining/the-fresh-food-co-at-west-campus/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year}

		for item in BUItems[eachDay]:
				ingrString = "ingredients-" + str(item.NutID)

				soupObjects = {}
				for key, url in DHURL.iteritems():
					bsObject = BeautifulSoup(urllib2.urlopen(url))

					ingredientItem = bsObject.find(class_="hidden ingredients").find(id=ingrString)
					if ingredientItem != None:
						ingridentsString = ingredientItem.find(class_="ingredients").get_text()[13:]
						item.ingridentsList = ingridentsString
						item.save()
						print item.ItemName + " - Saved"
						break
					


def getItemAddIngredient2():
	#Get all items in a day
	datetime = ()
	BUItemsList = []	

	all_day_items = BU_All_Items.Query.all()

	page1k = all_day_items.limit(1000)
	page2k = all_day_items.skip(1000).limit(2000)

	for item in page1k:
		BUItemsList.append(item)

	for item in page2k:
		BUItemsList.append(item)

	for m in range(1,13):
		for d in range(1,32):
		 	removedItems = []
			print str(m) + "/" + str(d)
			month = str(m)
			day = str(d)
			year = "2014"

			DHURL = {'war':"http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year,'bay':"http://www.bu.edu/dining/where-to-eat/residence-dining/marciano-commons/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year, 'wes':"http://www.bu.edu/dining/where-to-eat/residence-dining/the-fresh-food-co-at-west-campus/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year}

			for item in BUItemsList:
				ingrString = "ingredients-" + str(item.NutID)

				soupObjects = {}
				for key, url in DHURL.iteritems():
					bsObject = BeautifulSoup(urllib2.urlopen(url))

					ingredientItem = bsObject.find(class_="hidden ingredients").find(id=ingrString)
					if ingredientItem != None:
						ingridentsString = ingredientItem.find(class_="ingredients").get_text()[13:]
						item.ingridentsList = ingridentsString
						item.save()
						print item.ItemName + " - Saved"
						removedItems.append(item)
						break
		#remove item
		for itemToRemove in removedItems:
			BUItemsList.remove(itemToRemove)
			print "Items Remaining:" + len(BUItemsList)
		
		

def getItemAddIngredient3():
	#Get all items in a day
	datetime = ()
	BUItemsList = []	

	all_day_items = BU_All_Items.Query.filter(ingridentsList=None)

	page1k = all_day_items.limit(1000)
	page2k = all_day_items.skip(1000).limit(2000)

	for item in page1k:
		BUItemsList.append(item)

	for item in page2k:
		BUItemsList.append(item)

	
	print("\n" + str(len(BUItemsList)))



	nameToItem = {}
	for item in BUItemsList:
		ingrString = "ingredients-" + str(item.NutID)
		print ingrString	
		nameToItem[ingrString] = item

	for m in range(2,13):
		for d in range(1,32):
		 	removedItems = []
			print str(m) + "/" + str(d)
			month = str(m)
			day = str(d)
			year = "2013"

			DHURL = {'war':"http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year,'bay':"http://www.bu.edu/dining/where-to-eat/residence-dining/marciano-commons/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year, 'wes':"http://www.bu.edu/dining/where-to-eat/residence-dining/the-fresh-food-co-at-west-campus/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year}
			idToIngridents = {}
			for key, url in DHURL.iteritems():
				bsObject = BeautifulSoup(urllib2.urlopen(url))
				ingredientItem = bsObject.find(class_="hidden ingredients").find_all(class_="hidden")
				for ingObj in ingredientItem:
					idToIngridents[ingObj.get("id")] = ingObj.find(class_="ingredients").get_text()[13:]


			for ingridID in idToIngridents:
				if ingridID in nameToItem:
					nameToItem[ingridID].ingridentsList = idToIngridents[ingridID]
					nameToItem[ingridID].save()
					print nameToItem[ingridID].ItemName + " - Saved"
					nameToItem.pop(ingridID)


def testWebQuery():
	month = "9"
	day = "22"
	year = "2014"

	DHURL = {'war':"http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year,'bay':"http://www.bu.edu/dining/where-to-eat/residence-dining/marciano-commons/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year, 'wes':"http://www.bu.edu/dining/where-to-eat/residence-dining/the-fresh-food-co-at-west-campus/menu/?dsd=" + day + "&dsm=" + month + "&dsy=" + year}

	soupObjects = {}
	for key, url in DHURL.iteritems():
		bsObject = BeautifulSoup(urllib2.urlopen(url))
		ingredientItem = bsObject.find(class_="hidden ingredients").find(id="ingredients-2071227472")
		if ingredientItem != None:
			ingridentsString = ingredientItem.find(class_="ingredients").get_text()[13:]
			print ingridentsString
			break

		
		#print ingredientItem


def csvToParse():

	BUItemsList = []	

	all_day_items = BU_All_Items.Query.filter(ingridentsList=None)

	page1k = all_day_items.limit(1000)
	page2k = all_day_items.skip(1000).limit(2000)

	for item in page1k:
		BUItemsList.append(item)

	for item in page2k:
		BUItemsList.append(item)

	idToIngridents = {}
	with open('recipes2.csv', 'rU') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			idToIngridents[row[1]] = row[3]

	f.close()

	nameToItem = {}
	for item in BUItemsList:
		ingrString = str(item.NutID)
		print ingrString	
		nameToItem[ingrString] = item

	for ingridID in idToIngridents:
		if ingridID in nameToItem:
			nameToItem[ingridID].ingridentsList = idToIngridents[ingridID]
			nameToItem[ingridID].save()
			print nameToItem[ingridID].ItemName + " - Saved"
			nameToItem.pop(ingridID)


def getAllItemIds():
	BUItemsList = []	

	all_day_items = BU_All_Items.Query.all()

	page1k = all_day_items.limit(1000)
	page2k = all_day_items.skip(1000).limit(2000)

	for item in page1k:
		BUItemsList.append(str(item.NutID))

	for item in page2k:
		BUItemsList.append(str(item.NutID))

	writer = csv.writer(open("jsonFiles/input.csv", 'w'))
	for i in BUItemsList:
		writer.writerow(["http://www.bu.edu/nisprod/dining/data/menus/labels/" + i + ".gif"])



def csvNutritionToParse():
	BUItemsList = []	

	all_day_items = Item.Query.all()

	page1k = all_day_items.limit(1000)
	page2k = all_day_items.skip(1000).limit(2000)

	for item in page1k:
		BUItemsList.append(item)

	for item in page2k:
		BUItemsList.append(item)


	print (BUItemsList)

	NameToNutritionList = {}
	with open('jsonFiles/nutritionFiles.csv', 'rU') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			NameToNutritionList[row[0]] = [row[1], row[2], row[3]]
			#fat sodium sugar

	f.close()

	nameToItem = {}
	for item in BUItemsList:
		itemName = str(item.name)
		nameToItem[itemName] = item
	print nameToItem

	for name in NameToNutritionList:
		if name in nameToItem:
			nameToItem[name].fat = NameToNutritionList[name][0]
			nameToItem[name].sodium = NameToNutritionList[name][1]
			nameToItem[name].sugar = NameToNutritionList[name][2]
			nameToItem[name].save()
			print nameToItem[name].name + " - Saved"
			nameToItem.pop(name)

def exportUserTummy():
	user = _User.Query.get(email="agonchar@bu.edu")
	tummy = Tummy.Query.filter(User=user)
	tummy1 = tummy.limit(1000)
	tummyList = []
	for t in tummy1:
		tummyList.append(t.Item.ItemName)

	print tummyList

def addToTummy():

	tummyItems = [u'Sweet and Sour Chicken', u'Corn Muffin', u'Roasted Maine Potatoes', u'Seasoned Greens', u'Portabella Basil Pizza', u'Homestyle Mashed Potatoes', u'Baked Fish & Chips']


	user = User.Query.get(email="agonchar@bu.edu")

	itemListIDs = []
	for ti in tummyItems:
		itemId = Item.Query.filter(name=ti)
		if itemId[0] is not None:
			itemListIDs.append(itemId[0])

	for i in itemListIDs:
		tummyItem = Tummy(Active=True, Item=i, User=user, Date=datetime.now())
		tummyItem.save()



def getMyTummyItems():
	user = User.Query.get(FBName="bQbTxdNsVb")
	tummy = Tummy.Query.filter(User=user)

	uniqItems = {}
	for t in tummy:
		if t.Item.name in uniqItems:
			uniqItems[t.Item.name][0] += 1
		else:
			uniqItems[t.Item.name] = [1, t.Item.objectId]


	sortedx = sorted(uniqItems.items(), key=operator.itemgetter(1), reverse=False)
	
	for x in sortedx:
		print x
	#print uniqItems

addToTummy()