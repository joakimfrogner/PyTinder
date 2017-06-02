from datetime import date, datetime
# from threading import Thread
# import time
import utils.tinder.tinder_api as api
import utils.tinder.config as config

import cv2

import urllib.request as geturl
import numpy as np


################################################
################################################
'''
This file collects important data on your matches,
allows you to sort them by last_activity_date, age,
gender, message count, and their average successRate.

The only thing that is not supported on this is 
getting your matches distance as this requires a
different api call [api.get_person(id)] which would
severely slow down the data collection into match_info.

So, since it is not entirely important to have distance,
we will proceed without it. Perhaps further down the road
I will cache this information so that it does not have to 
be re-retrieved every time you refresh your match updates.

'''
################################################
################################################


# Gets all important information on all of your matches
def get_match_info():
	matches = api.get_updates()['matches']
	now = datetime.utcnow()
	match_info = {}
	for match in matches[:len(matches) - 2]:
		try:
			person = match['person']
			name = person['name']
			person_id = person['_id'] # for looking up profile
			match_id = match['id'] # for sending messages
			message_count = match['message_count']
			photos = get_photos(person)
			bio = person['bio']
			gender = person['gender']
			messages = match['messages']
			birthday = match['person']['birth_date']
			avg_successRate = get_avg_successRate(person)
			# last_activity_date = match['last_activity_date']
			# distance = api.get_person(person_id)['results']['distance_mi'] #Takes too long...

			match_info[person_id] = {
				"name": name,
				"match_id": match_id,
				"message_count": message_count,
				"photos": photos,
				"bio": bio,
				"gender": gender,
				"avg_successRate": avg_successRate,
				"messages": messages,
				"age": calculate_age(birthday)
				# "distance": distance,
				# "last_activity_date": last_activity_date,
				# "readable_activity_date": get_last_activity_date(now, last_activity_date)
			}

		except Exception as ex:
		    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		    message = template.format(type(ex).__name__, ex.args)
		    print(message)
	return match_info

# Query by match name 
def get_match_id_by_name(name):
	global match_info
	list_of_ids = []
	for match in match_info:
		match_name = match_info[match]['name']
		if match_name == name:
			list_of_ids = list_of_ids + [match_info[match]['match_id']]
	if len(list_of_ids) > 0:
		return list_of_ids
	return {"error": "No matches by name of %s" % name}

# Returns a list of photo urls
def get_photos(person):
	photos = person['photos']
	photo_urls = []
	for photo in photos:
		photo_urls = photo_urls + [photo['url']]
	return photo_urls

# Converts from '1997-03-25T22:49:41.151Z' to an integer (age)
def calculate_age(birthday_string):
	birthyear = int(birthday_string[:4])
	birthmonth = int(birthday_string[5:7])
	birthday = int(birthday_string[8:10])
	today = date.today()
	return today.year - birthyear - ((today.month, today.day) < (birthmonth, birthday))

# Gets the average successRate of the person
# perhaps an indicator of... something?
def get_avg_successRate(person):
	photos = person['photos']
	avg = 0
	for photo in photos:
		try:
			photo_successRate = photo['successRate']
			avg += photo_successRate
		except:
			return 0
	return avg / len(photos)


def sort_by_successRate():
	global match_info
	return sorted(match_info.items(), key=lambda x: x[1]['avg_successRate'], reverse=True)


# This is the abstract version of sort_by_activity_date and sort_by_successRate
# accepted valueNames are: "age", "message_count", "successRate", "gender"
def sort_by_value(valueName):
	global match_info
	return sorted(match_info.items(), key=lambda x: x[1][valueName], reverse=True)
# This doesn't sort it...Maybe make it a list?
# Can't return a sorted dict.

def see_friends_profiles(name=None):
	friends = api.see_friends()
	if name == None:
		return friends
	else:
		result_dict = {}
		name = name.title()  # this turns fabien bessez-espina into Fabien Bessez-Espina
		for friend in friends:
			if name in friend["name"]:
				result_dict[friend["name"]] = friend
		if result_dict == {}: return "No friends by that name"
		return result_dict

def tinder():
	if api.authverif() == True:
		return get_match_info()
	else:
		print("Something went wrong. You were not authorized.")
		return None
	

def get_image_cv2(url):
	try:
		resp = geturl.urlopen(url)
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	except:
		print("Could not get url: {}".format(url))
		return False, None

	return True, image
