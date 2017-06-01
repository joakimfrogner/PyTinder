import cv2
import numpy as np

def match(img, template_path):
    template = cv2.imread(template_path, 0)
    #img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    
    threshold = 0.9
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0,255,255), 2)

    return img

if __name__ == "__main__":
    img = cv2.imread("img/opencv-template-matching-python-tutorial.jpg")

    img = match(img, "img/opencv-template-for-matching.jpg")
    cv2.imshow("detected", img)
    cv2.waitKey(0)