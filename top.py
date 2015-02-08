#!venv/bin/env python

import settings_local
import calendar
import operator
from item import Item, Menu, NutritionLabel
from parse_rest.connection import register
from datetime import datetime



def recommends(dateTime,user, location):
	itemScores = []
	nutriSorted = []
	ingredSorted = []
	menu = getMenu(dateTime,location)
	freqTuple = freqAnalysis(user)

	for item in menu.items:
		itemScores.append(itemWithScore(item,item.NutritionLabel,freqTuple))

	itemScores.sort(key=operator.itemgetter(1))
	ingredSorted = itemScores
	nutriSorted.sort(key=operator.itemgetter(2))
	nutriSorted = itemScores

	return (ingredSorted[:5],nutriSorted[:5])

	

def itemWithScore(item,nutritionLabel,freqTuple):
	ingredientFreq = freqTuple[0]
	nutritionFreq = freqTuple[1]
	tumScore = 0
	yumScore = 0

	for ingredient in item.ingredients:
		try:
			freqValue = ingredientFreq[ingredient]
			tumScore += abs(1-freqValue)
		except:
			score += 1

	tumScore += abs(len(ingredientFreq)-len(item.ingredients))

	yumScore += abs(nutritionFreq['fat']-nutritionLabel.fat)
	yumScore += abs(nutritionFreq['sodium']-nutritionLabel.sodium)
	yumScore += abs(nutritionFreq['sugars']-nutritionLabel.sugars)

	return (item,tumScore,yumScore)

def getMenu(timeStamp,location):
	register(settings_local.APPLICATION_ID,settings_local.REST_API_KEY)
	date = "{} {},{}".format(calendar.month_abbr[timeStamp.month],timeStamp.day,timeStamp.year)
	output_date = date
	meal = 0

	if(len(date) < 11):
		output_date = date[:4] + '0' + date[4:]

	time = (timeStamp.hour)*60 + timeStamp.minute

	if (time >=420 && time < 660):
		meal = 0
	elif (time >= 660 && time < 1080):
		meal = 1
	elif (time >= 1080 && time < 1260):
		meal = 2
	else:
		return 0

	return Menu.Query.get(Date=output_date,Meal=meal,Location=location)

