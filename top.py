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

register(settings_local.APPLICATION_ID,settings_local.REST_API_KEY)

def recommends(dateTime,user, location):
#def recommend(user,time):
	itemScores = []
	nutriSorted = []
	ingredSorted = []
	menu = getMenu(dateTime,location)

	tummy = getUserItems(user)

	freqTuple = freqAnaysis(tummy,dateTime)

	for item in menu:
		itemScores.append(itemWithScore(item.NutritionItem,freqTuple))

	#print(itemScores)

	itemScores.sort(key=operator.itemgetter(1))
	ingredSorted = itemScores
	#nutriSorted.sort(key=operator.itemgetter(2))
	#nutriSorted = itemScores

	print(ingredSorted[:20])

	print("\n")

	s = sorted(freqTuple[0].values())
	print(sorted(freqTuple[0].items(), key=lambda x:x[1]))

	return ingredSorted[:5]

	#return (ingredSorted[:5],nutriSorted[:5])

	

#def itemWithScore(item,nutritionLabel,freqTuple):
def itemWithScore(item,freqTuple):
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

def getMenu(timeStamp,location):
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

	return Menu.Query.filter(DateAvailable=date,MealTimeAvailable=meal,hallID=output_location)

def getUserItems(userName):
	user = User.Query.get(fullName=userName)
	tummy = Tummy.Query.filter(User=user)

	return tummy

t = datetime(2015,02,06,13,00)
recommends(t,'Santiago Beltran','Baystate')
#recommend('Erin Dail',t)


