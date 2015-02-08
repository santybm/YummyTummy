import json
from parse_rest.connection import register
from parse_rest.datatypes import Object
import operator

#Register Parse with Keys
register("ab2PDO430oZeLB4cI4GAUFjdWcgKGtJcQUe291UW", "7mjGlKBqovrJxgZY6osHZMkET4AlXlgpyiroNCYl")


#Setup User Class
class User(Object):
    pass

class Item(Object):
	pass

class NutritionLabel(Object):
	pass


def getUserData(userID, save=False):
	#Read JSON jsonFiles/_User.json file and get the FBName, email, and email
	json_data=open('jsonFiles/_User.json')
	
	data = json.load(json_data)
	users = data['results']

	if (save==True):
		for userObject in users:	
			if userObject['objectId'] == userID:
				user= User(username = userObject['username'], fullName=userObject.get('FBName'), email = userObject['email'])
				user.save()

def getTummyByDate(userID):
	# Get all items added to tummy by date. (Date: [item1,item2])
	# Return Day object with Date (mmddyy, user, [item_ids])
	return None

def getTummyData():
	#read jsonFiles/Tummy.json file and 1) Find most frequently appearing User.

	#Get most frequently appearing user.
	json_data=open('jsonFiles/Tummy.json')

	items = json.load(json_data)
	json_data.close()

	allUsers = {}
	for item in items['results']:
		userID = item['User']['objectId']
		if userID in allUsers:
			allUsers[userID] += 1
		else:
			allUsers[userID] = 1

	sorted_x = sorted(allUsers.items(), key=operator.itemgetter(1), reverse=True)

	for i in range(0,10):
		getUserData (sorted_x[i][0])

def getAllItems():
	#Get all items.
	json_data=open('jsonFiles/BU_All_Items.json')
	items = json.load(json_data)
	json_data.close()

	for item in items['results']:
		nutLabel = NutritionLabel(calories=item['Calories'])
		nutLabel.save()
		parseItem = Item(name=item['ItemName'], nutritionID=nutLabel, oldObjectID=item['objectId'])
		parseItem.save()


getAllItems()


