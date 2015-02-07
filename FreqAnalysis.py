
from datetime import datetime
import math


def ingredientsForItem(item):
	return item["item"]["ingredients"]
	# if item["name"] == "Tomato":
	# 	return ["Tomato"]
	# return ["Tomato", "Onion", "Lettuce", "Wheat"]

def nutritionForItem(item):
	return {"sodium": item["item"]["nutritionID"]["sodium"], "sugar": item["item"]["nutritionID"]["sugar"], "fat": item["item"]["nutritionID"]["fat"]}
	# if item["name"] == "Tomato":
	# 	return {"fat": 140.0, "sugar": 20, "sodium": 43}
	# return {"fat": 120.0, "sugar": 20, "sodium": 43}


def gaussianEquation(difference):
	return .1 ** ((difference * difference)/200.0)

def weighItem(item, date):

	itemDate = item["timeStamp"]
	dateDelta = date - itemDate
	dateDifferenceWeight = gaussianEquation(dateDelta.days)

	timeDifferenceWeight = gaussianEquation((dateDelta.total_seconds()/3600.0) % 24.0)

	return dateDifferenceWeight + timeDifferenceWeight


def freqAnaysis(items, date):
	ingredientFreqency = {}
	nutritionFreqency = {}

	totalConsumptionWeight = 0.0

	for item in items:
		itemIngredients = ingredientsForItem(item)
		itemNutrition = nutritionForItem(item)

		itemWeight = weighItem(item, date)
		totalConsumptionWeight += itemWeight

		for ingredient in itemIngredients:
			if ingredient in ingredientFreqency:
				ingredientFreqency[ingredient] += itemWeight
			else:
				ingredientFreqency[ingredient] = itemWeight

		for key in nutritionForItem(item):
			if key in nutritionFreqency:
				nutritionFreqency[key] += itemWeight * itemNutrition[key]
			else:
				nutritionFreqency[key] = itemWeight * itemNutrition[key]

	for key in ingredientFreqency.iterkeys():
		ingredientFreqency[key] /= totalConsumptionWeight

	for key in nutritionFreqency.iterkeys():
		nutritionFreqency[key] /= totalConsumptionWeight

	return (ingredientFreqency, nutritionFreqency)


# print freqAnaysis([{"name": "Tomato Soup", "timeStamp":datetime.now()}, {"name": "Tomato", "timeStamp": datetime(2015, 02, 02, 02, 10)}], datetime.now())






