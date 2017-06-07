import fb_auth_token
import os

fb_username = ""
fb_password = ""

fb_access_token = fb_auth_token.get_fb_access_token(fb_username, fb_password)
fb_user_id = fb_auth_token.get_fb_id(fb_access_token)
host = 'https://api.gotinder.com'

img_base_dir = os.environ['HOME'] + "/Pictures/tinder/"
dir_liked = img_base_dir + "liked/"
dir_liked_txt = img_base_dir + "liked/text/"

dir_disliked = img_base_dir + "disliked/"
dir_disliked_txt = img_base_dir + "disliked/text/"

dir_matched = img_base_dir + "matched/"
dir_matched_txt = img_base_dir + "matched/text/"

dirs = [img_base_dir, dir_liked, dir_disliked, dir_matched, dir_liked_txt, dir_disliked_txt, dir_matched_txt]

for path in dirs:
    if not os.path.exists(path):
        os.makedirs(path)