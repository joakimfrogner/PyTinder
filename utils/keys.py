import cv2, os

def load_keys():
    if not os.path.exists("utils/keys.txt"):
        print("Configuring keys...")

        img = cv2.imread("utils/tmp.png", 0)
        cv2.imshow("tmp", img)

        print("Press button for like (arrow buttons not working on Windows):")
        up = str(cv2.waitKey(0) & 0xff)

        print("Press button for dislike (arrow buttons not working on Windows):")
        down = str(cv2.waitKey(0) & 0xff)

        cv2.destroyAllWindows()

        with open("utils/keys.txt", "w") as f:
            f.write(up+","+down)

        return int(up), int(down)
    else:
        with open("utils/keys.txt", "r") as f:
            contents = f.read().split(",")

        if len(contents) != 2:
            os.remove("utils/keys.txt")
            contents = load_keys()[:]

        return int(contents[0]), int(contents[1])

if __name__ == '__main__':
    up, down = load_keys()
    print(up, down)
