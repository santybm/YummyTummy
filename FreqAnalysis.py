
from datetime import datetime
import math

def gaussianEquation(difference):
	return .1 ** ((difference * difference)/200.0)

def ingredientsForItem(item):

	if item["name"] == "Tomato":
		return ["Tomato"]
	return ["Tomato", "Onion", "Lettuce", "Wheat"]


def weighItem(item, date):

	itemDate = item["timeStamp"]
	dateDelta = date - itemDate
	dateDifferenceWeight = gaussianEquation(dateDelta.days)

	timeDifferenceWeight = gaussianEquation((dateDelta.total_seconds()/3600.0) % 24.0)

	return dateDifferenceWeight + timeDifferenceWeight


def freqAnaysis(items, date):
	ingredientFreqency = {}

	totalConsumptionWeight = 0.0

	for item in items:
		itemIngredients = ingredientsForItem(item)
		itemWeight = weighItem(item, date)
		totalConsumptionWeight += itemWeight
		for ingredient in itemIngredients:
			if ingredient in ingredientFreqency:
				ingredientFreqency[ingredient] += itemWeight
			else:
				ingredientFreqency[ingredient] = itemWeight

	for key in ingredientFreqency.iterkeys():
		ingredientFreqency[key] /= totalConsumptionWeight

	return ingredientFreqency


print freqAnaysis([{"name": "Tomato Soup", "timeStamp":datetime.now()}, {"name": "Tomato", "timeStamp": datetime(2015, 02, 02, 02, 10)}], datetime.now())






