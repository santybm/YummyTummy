***REMOVED***

import settings_local
import calendar
import operator
from FreqAnalysis import freqAnaysis
from parse_rest.connection import register
from datetime import datetime
from parse_rest.datatypes import Object as ParseObject

class Item(ParseObject):
	pass

class Menu(ParseObject):
	pass

class NutritionLabel(ParseObject):
	pass

class User(ParseObject):
	pass

class Tummy(ParseObject):
	pass

class recEngine:
	dateTime = 0
	user = ''
	location = ''
	numListings =0
	itemScores = []
	sortedFreq = []
	mostHatedItems = []


	def __init__(self,dateTime,user,location,numListings):
		self.dateTime = dateTime
		self.user = user
		self.location = location
		self.numListings = numListings

	def recommends(self):
		nutriSorted = []
		ingredSorted = []
		menu = self.getMenu(self.dateTime,self.location)

		tummy = self.getUserItems(self.user)

		freqTuple = freqAnaysis(tummy,self.dateTime)

		for item in menu:
			self.itemScores.append(self.itemWithScore(item.NutritionItem,freqTuple))

		#print(itemScores)

		self.itemScores.sort(key=operator.itemgetter(1))
		ingredSorted = self.itemScores
		#nutriSorted.sort(key=operator.itemgetter(2))
		#nutriSorted = itemScores

		#print(ingredSorted[:numListings])

		#print("\n")

		#print(ingredSorted[-numListings:])

		#s = sorted(freqTuple[0].values())
		self.sortedFreq = sorted(freqTuple[0].items(), key=lambda x:x[1])

		self.mostHatedItems = ingredSorted[-self.numListings:]

		return ingredSorted[:self.numListings]

	def itemWithScore(self,item,freqTuple):
		ingredientFreq = freqTuple[0]
		tumScore = 0

		for ingredient in item.ingredients:
			try:
				freqValue = ingredientFreq[ingredient]
				tumScore += abs(1-freqValue)
			except:
				tumScore += 1

		tumScore += abs(len(ingredientFreq)-len(item.ingredients))

		return (item.name,tumScore)

	def getMenu(self,timeStamp,location):
		date = datetime(timeStamp.year,timeStamp.month,timeStamp.day)
		meal = ''
		output_location = 0

		time = (timeStamp.hour)*60 + timeStamp.minute

		if (time >=420 and time < 660):
			meal = 'B'
		elif (time >= 660 and time < 1080):
			meal = 'L'
		elif (time >= 1080 and time < 1260):
			meal = 'D'
		else:
			return 0

		if location == 'Warren':
			output_location = 1
		elif location == 'Baystate':
			output_location = 2
		elif location == 'West':
			output_location = 3

		menu = Menu.Query.filter(DateAvailable=date,MealTimeAvailable=meal,hallID=output_location)
		return menu.limit(2000)

	def getUserItems(self,userName):
		user = User.Query.get(fullName=userName)
		tummy = Tummy.Query.filter(User=user)
		tummy1 = tummy.limit(2000)

		return tummy


register(settings_local.APPLICATION_ID,settings_local.REST_API_KEY)

if __name__ == "__main__":
	t = datetime(2015,02,06,19,00)
	test = recEngine(t, 'Carlos Cheung', 'Baystate',5)
	print(test.recommends())
	#recommends(t,'Carlos Cheung','Baystate',5)
#recommend('Erin Dail',t)


