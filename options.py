import pyautogui
import mouse
import keyboard

import cv2
import numpy as np

import csv
import re
import time

import os

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Options(object):
    def __init__(self, **options):
        abspath = os.path.abspath(__file__)
        dir_name = os.path.dirname(abspath)
        os.chdir(dir_name)

        self.width, self.height = pyautogui.size()

        self.instruction = self.import_data()

        ## Möjligtvis flytta dessa till där de behövs istället direkt
        self.levelup_path = f"Support_Files\\{str(self.height)}_levelup.png"
        self.victory_path = f"Support_Files\\{str(self.height)}_victory.png"
        self.defeat_path = f"Support_Files\\{str(self.height)}_defeat.png"
        self.menu_path = f"Support_Files\\{str(self.height)}_menu.png"
        self.easter_path = f"Support_Files\\{str(self.height)}_easter.png"
        self.obyn_hero_path = f"Support_Files\\{str(self.height)}_obyn.png"
        self.insta_monkey = f"Support_Files\\{str(self.height)}_instamonkey.png"

        pyautogui.FAILSAFE = True # When mouse is moved to top left, program will exit


        self.upgrade_keybinds = {
            "top" : ",",
            "middle" : ".",
            "bottom" : "/"

        }

        self.reso_16 = [
            { "width": 1280, "height": 720  },
            { "width": 1920, "height": 1080 },
            { "width": 2560, "height": 1440 },
            { "width": 3840, "height": 2160 }
        ]

        self.button_positions = { # Creates a dictionary of all positions needed for monkeys (positions mapped to 2160 x 1440 resolution)
            "HOME_MENU_START" : [1123, 1248],
            "EXPERT_SELECTION" : [1778, 1304],
            "RIGHT_ARROW_SELECTION" : [2193, 582],
            "DARK_CASTLE" : [1420, 350], # changed to (x=1941, y=513) in latest patch
            "HARD_MODE" : [1729, 562],
            "CHIMPS_MODE" : [2139, 980],
            "STANDARD_GAME_MODE" : [847,780],
            "OVERWRITE_SAVE" : [1520, 974],
            "VICTORY_CONTINUE" : [1283, 1215],
            "VICTORY_HOME" : [939, 1124],
            "EASTER_COLLECTION" : [1279, 911],
            "F_LEFT_INSTA" : [868, 722],
            "F_RIGHT_INSTA" : [1680, 722],
            "LEFT_INSTA" : [1074, 725],
            "RIGHT_INSTA" : [1479, 724],
            "MID_INSTA" : [1276, 727],
            "EASTER_CONTINUE" : [1280, 1330],
            "EASTER_EXIT" : [100, 93],
            "QUIT_HOME" : [1126, 1135],
            "HERO_SELECT" : [799, 1272],
            "SELECT_OBYN" : [],
            "CONFIRM_HERO" : [855, 893],
            "TARGET_BUTTON_MORTAR": [1909, 491],
            "ABILLITY_ONE": [253, 1379],
            "ABILLITY_TWO": [369, 1377],
            "FREEPLAY" : [1611, 1112],
            "OK_MIDDLE" : [1280, 1003],
            "RESTART": [1413, 1094],
            "CONFIRM_CHIMPS" : [1481, 980]

        }

        self.monkeys = {
            "DART" : "q",
            "BOOMERANG" : "w",
            "BOMB" : "e",
            "TACK" : "r",
            "ICE" : "t",
            "GLUE" : "y",
            "SNIPER" : "z",
            "SUBMARINE" : "x",
            "BUCCANEER" : "c",
            "ACE" : "v",
            "HELI" : "b",
            "MORTAR" : "n",
            "DARTLING" : "m",
            "WIZARD" : "a",
            "SUPER" : "s",
            "NINJA" : "d",
            "ALCHEMIST" : "f",
            "DRUID" : "g",
            "BANANA" : "h",
            "ENGINEER" : "l",
            "SPIKE" : "j",
            "VILLAGE" : "k",
            "HERO" : "u"
        }

    def print_stats(self, stats, start_time):
        os.system("cls")
        print("="*6)
        if round(time.time() - start_time, 2) >= 60.0:
            stats["Uptime"] = "{} minutes".format(round( (time.time() - start_time) / 60, 2)  )
        elif round(time.time() - start_time, 2) / 60 >= 60.0:
            stats["Uptime"] = "{} hours".format(round( (time.time() - start_time) / 60 / 60, 2) )
        else:
            stats["Uptime"] = "{} seconds".format(round(time.time() - start_time, 2))
        
        for key, value in stats.items():
            print(f"{key.replace('_', ' ')}\t{value}")
        print("="*6)

    def padding(self):
        """
            Get's width and height of current resolution
            we iterate through reso_16 for heights, if current resolution height matches one of the entires 
            then it will calulate the difference of the width's between current resolution and 16:9 (reso_16) resolution
            divides by 2 for each side of padding

            Variables Used
              width -- used to referance current resolution width
              height -- used to referance current resolution height
              pad -- used to output how much padding we expect in different resolutions
              reso_16 -- list that      
        """
    
        pad = 0
        for x in self.reso_16: 
            if self.height == x['height']:
                pad = (self.width - x['width'])/2
        #print("I have been padding -- " + str(pad))

        # DEBBUGGING
        return pad

    def scaling(self, pos_list):
        """
            This function will dynamically calculate the differance between current resolution and designed for 2560x1440
            it will also add any padding needed to positions to account for 21:9     
        """

        # do_padding -- this is used during start
        reso_21 = False
        
        for x in self.reso_16: 
            if self.height == x['height']:
                if self.width != x['width']:
                    reso_21 = True
                    x = pos_list[0]
                    break
        if not reso_21:
            x = pos_list[0] / 2560 
            x *= self.width

        y = pos_list[1] / 1440
        y *= self.height
        #print(" Me wihout padding " + str([x]))
        x += self.padding() # Add's the pad to to the curent x position variable
        #print(" Me with padding -- " + str([x]))
        return (x, y)

    # def move_mouse(self, location):
    #     pyautogui.moveTo(location)
    #     time.sleep(0.1)

    def click(self, location=mouse.get_position(), button=None, sleep_time=0.5):
        """
            pass in (x, y) for a specific location to click
            If a specific button should be pressed pass in the button name to button=
        """
        # self.move_mouse(location)
        if button:
            location = self.scaling(self.button_positions[button])
            mouse.move(*location)
        else:
            location = self.scaling(location)
            mouse.move(*location)
            
        time.sleep(sleep_time)
        mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
        time.sleep(sleep_time)

    def press_key(self, key):
        """
            Simulate a keypress
        """
        keyboard.send(key)
        time.sleep(0.1)

    def getRound(self):
        """
            TODO: Refacor this function to try and make it more efficient
        """

        top, left = self.scaling([1850, 35])
        width, height = self.scaling([225, 65])
        img = pyautogui.screenshot(region=(top, left, width, height))
        
        numpy_image = np.array(img)

        # Make image grayscale using opencv
        gray_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2GRAY)

        # Threasholding
        final_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
        # Get current round from image with tesseract
        text = pytesseract.image_to_string(final_image,  config='--psm 7').replace("\n", "")

        # regex to look for format [[:digit:]]/[[:digit:]] if not its not round, return None
        if re.search(r"(\d+/\d+)", text):
            text = text.split("/")
            text = tuple(map(int, text))
            return text
        else:
            return None

    # Fixar om cordinater till sträng
    def fixPositionFormated(self, posString):
        fixed = posString.split(", ")

        return tuple(map(int, fixed))


    def import_data(self):
        formatedInstructions = []
        with open("instructions.csv") as file:
            csvreader = csv.DictReader(file)
            
            for row in csvreader:
                row["POSITION"] = self.fixPositionFormated(row["POSITION"])

                if row["TARGET_POS"] != "-":
                    row["TARGET_POS"] = self.fixPositionFormated(row["TARGET_POS"])
                
                formatedInstructions.append(row)
        return formatedInstructions
        # pprint(formatedInstructions)


