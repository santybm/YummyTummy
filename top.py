#!venv/bin/env python

import settings_local
from item import Item, Menu, NutritionLabel
from parse_rest.connection import register
from datetime import datetime



def recommends(dateTime,user, location):
	getMenu(dateTime,location)
	freqTuple = freqAnalysis(user)
	itemWithScore(items)

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

	for nutrition in item.nutrition:

	tumScore += abs(len(ingredientFreq)-len(item.ingredients))

	yumScore += abs(nutritionFreq['fat']-nutritionLabel.fat)
	yumScore += abs(nutritionFreq['sodium']-nutritionLabel.sodium)
	yumScore += abs(nutritionFreq['sugars']-nutritionLabel.sugars)

	return (item,tumScore,yumScore)

def getMenu(dateTime,location):
	register(settings_local.APPLICATION_ID,settings_local.REST_API_KEY)
	