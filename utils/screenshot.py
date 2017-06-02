import numpy as np
import cv2
from mss import mss
from PIL import Image

def screenshot(mon=0, top=0, left=0, width=200, height=200):
    sct = mss()
    monitors = sct.enum_display_monitors()

    for num, monitor in enumerate(monitors[1:], 1):
        if num == mon+1:
            sct.get_pixels(monitor)
            break
    
    img = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    try:
        img = img[top:top+height, left:left+width]
    except:
        img = None

    return img

if __name__ == "__main__":
    screenshot(mon=0, width=1000)