import numpy as np
import urllib.request as geturl
import cv2

def combine_imgs(img1, img2):
	h1, w1 = img1.shape[:2]
	h2, w2 = img2.shape[:2]

	combined = np.zeros((max(h1, h2), w1+w2,3), np.uint8)

	combined[:h1, :w1,:3] = img1
	combined[:h2, w1:w1+w2,:3] = img2

	return combined

def get_image_from_url(url):
	try:
		resp = geturl.urlopen(url)
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	except:
		print("Could not get url: {}".format(url))
		return False, None

	return True, image

def scale_img(img, scale):
	if scale < img.shape[1]:
		r = scale / img.shape[1]
		dim = (scale, int(img.shape[0]*r))
		return True, cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
	else:
		return False, img
