from utils.tinder.api_usage import tinder, calculate_age, get_photos
from utils.tinder.config import dir_liked, dir_disliked, dir_matched, dir_liked_txt, dir_disliked_txt, dir_matched_txt
from utils.imgutils import combine_imgs, get_image_from_url, scale_img
from utils.tinder import tinder_api as api
from utils import keys

from pprint import pprint
import cv2
import numpy as np
import sys

if len(sys.argv) > 1 and sys.argv[1] == "-v":
    verbose = True
else:
    verbose = False

key_like, key_dislike = keys.load_keys()

matches = tinder()

while True:
    rec = api.get_recommendations()

    try:
        data = rec["results"]
    except:
        print("Could not fetch data ({})".format(rec["message"]))
        break

    profiles = []

    for i in range(len(data)): 
        usr_id = data[i]["_id"]
        name = data[i]["name"]
        age = calculate_age(data[i]["birth_date"])
        distance = int(int(data[i]["distance_mi"]) * 1.60934)

        photo_urls = get_photos(data[i])
        photos = []

        for url in photo_urls:
            ret, img = get_image_from_url(url)

            if ret:
                r, img = scale_img(img, 300)
                photos.append(img)

        profile = {
            "id": usr_id,
            "name":name,
            "age":age,
            "distance":distance,
            "photos":photos
        }

        if verbose:
            print("{} :: {}, {} years, {} km away ({} photos).".format(i, profile["name"], profile["age"], profile["distance"], len(profile["photos"])))
        else:
            print("Loading... {} of {}".format(i+1, len(data)), end="\r")

        if len(photos) == 0:
            if verbose:
                print("^ NO PHOTOS AVAILABLE -- SKIPPING")
        else:   
            profiles.append(profile)

    print("\nDone")

    for i in range(len(profiles)):
        profile = profiles[i]
        combined = profile["photos"][0]

        for photo in profile["photos"][1:]:
            combined = combine_imgs(combined, photo)

        image_title = name + " - " + str(age) + " years - " + str(distance) + " km away"
        cv2.imshow(image_title, combined)

        key = cv2.waitKey(0) & 0xFF

        if key == 27:
            cv2.destroyAllWindows()
            exit()

        elif key == key_like:
            api.like(profile["id"])

            for j in range(len(profile["photos"])):
                cv2.imwrite(dir_liked+"{}-{}.jpg".format(profile["id"], j), profile["photos"][j])

            with open(dir_liked_txt+"{}.json".format(usr_id), "w") as f:
                del data[i]["photos"]
                f.write(str(str(data[i]).encode("utf-8")))

        elif key == key_dislike:
            api.dislike(profile["id"])

            for j in range(len(profile["photos"])):
                cv2.imwrite(dir_disliked+"{}-{}.jpg".format(profile["id"], j), profile["photos"][j])

            with open(dir_disliked_txt+"{}.json".format(profile["id"]), "w") as f:
                del data[i]["photos"]
                f.write(str(str(data[i]).encode("utf-8")))

        cv2.destroyWindow(image_title)
