import cv2
import pyautogui
import time
import os
import numpy as np

current_directory = os.getcwd() + "/"
ingame = f"{current_directory}bloons_match.jpg"
ref = f"{current_directory}refrence.png"



def template_cv2(img, needle):
    start_time = time.time()

    # "heat map över img och template"
    imageObject = cv2.imread(img, cv2.COLOR_BGR2GRAY)
    templateObject = cv2.imread(needle, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(imageObject, templateObject, cv2.TM_CCOEFF_NORMED)

    # Vad används detta till
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result) # Bara nödvändigt vid endast en match
    # w = imageObject.shape[0]
    # h = imageObject.shape[1]
    locations = np.where(result >= 0.66) 

    # print("Opencv2 took", time.time()-start_time, "s")

    return (time.time()-start_time, locations)
    # for x, y in zip(*locations[::-1]):
    #     cv2.rectangle(imageObject, (x, y), (x + w, y + h), (0, 0, 255), 1)

    # cv2.imshow("asd", imageObject)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


summa = 0
n = 0
matches = 0
for i in range(100):
    t, res = template_cv2(ingame, ref)
    
    if len(res) >= 1:
        matches += 1

    summa += t
    n += 1

print("Average time:", summa / n)
print("total finds", matches)

