from api_usage import tinder, calculate_age, get_photos, get_image_cv2
from pprint import pprint
from config import dir_liked, dir_disliked, dir_matched, dir_liked_txt, dir_disliked_txt, dir_matched_txt

import tinder_api as api

import cv2
import os

import numpy as np

matches = tinder()

while True:
    rec = api.get_recommendations()

    try:
        data = rec["results"]
    except:
        print("Could not fetch data ({})".format(rec["message"]))
        break

    for i in range(len(data)):
        card = data[i]
        usr_id = card["_id"]
        name = card["name"]
        age = calculate_age(card["birth_date"])
        gender = card["gender"]
        distance = int(card["distance_mi"]) * 1.60934

        if gender:
            gender = "Female"
        else:
            gender = "Male"

        photos = get_photos(card)

        print("{} :: {}, {} years, {}, {} km away ({} photos).".format(i, name, age, gender, distance, len(photos)))

        i = 0

        while i < len(photos):
            ret, image = get_image_cv2(photos[i])
            if not ret:
                continue

            image_title = "[" + str(i+1) + "/" + str(len(photos)) + "] - " + name + " - " + str(age) + " years - " + str(distance) + " km away"
            cv2.imshow(image_title, image)

            key = cv2.waitKey(0) & 0xFF
            if key == 27:
                cv2.destroyAllWindows()
                exit()
            elif key == 83:
                # next
                if i == len(photos) - 1:
                    i = 0
                else:
                    i += 1
            elif key == 81:
                # prev
                i -= 2
            elif key == 82:
                api.like(usr_id)

                for j in range(len(photos)):
                    ret, img = get_image_cv2(photos[j])
                    if not ret:
                        continue

                    cv2.imwrite(dir_liked+"{}-{}.jpg".format(usr_id, j), img)
                
                with open(dir_liked_txt+"{}.json".format(usr_id), "w") as f:
                    del card["photos"]
                    f.write(str(card))

                cv2.destroyWindow(image_title)
                break
            elif key == 84:
                api.dislike(usr_id)

                for j in range(len(photos)):
                    ret, img = get_image_cv2(photos[j])
                    if not ret:
                        continue
                        
                    cv2.imwrite(dir_disliked+"{}-{}.jpg".format(usr_id, j), img)

                with open(dir_disliked_txt+"{}.json".format(usr_id), "w") as f:
                    del card["photos"]
                    f.write(str(card))

                cv2.destroyWindow(image_title)
                break

            cv2.destroyWindow(image_title)
