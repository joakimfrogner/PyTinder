import cv2, os

def load_keys():
    if not os.path.exists("utils/keys.txt"):
        img = cv2.imread("utils/tmp.png", 0)
        cv2.imshow("tmp", img)

        print("Configuring keys...")

        print("Press LEFT:")
        left = str(cv2.waitKey(0) & 0xff)

        print("Press RIGHT:")
        right = str(cv2.waitKey(0) & 0xff)

        print("Press UP:")
        up = str(cv2.waitKey(0) & 0xff)

        print("Press DOWN:")
        down = str(cv2.waitKey(0) & 0xff)

        cv2.destroyAllWindows()

        with open("utils/keys.txt", "w") as f:
            f.write(left+","+right+","+up+","+down)

        return int(left), int(right), int(up), int(down)

    else:
        with open("utils/keys.txt", "r") as f:
            contents = f.read().split(",")

        if len(contents) != 4:
            os.remove("utils/keys.txt")
            contents = load_keys()[:]

        return int(contents[0]), int(contents[1]), int(contents[2]), int(contents[3])

if __name__ == '__main__':
    left, right, up, down = load_keys()
    print(left, right, up, down)
