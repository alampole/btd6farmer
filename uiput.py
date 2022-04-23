import pyautogui
import mouse
import keyboard
import time
import static

from utils import Utils


class UIput(Utils):
    """
        Input and UI stuff combined hence UIput :)
    """
    
    def __init__(self):
        self.width, self.height = self.get_resolution()
        Utils.__init__(self, self.width, self.height)

    def get_resolution(self):
        """
            Returns the current resolution of the screen
        """
        w, h = pyautogui.size()
        return  pyautogui.size()

    def move_mouse(self, location):
        pyautogui.moveTo(location)
        time.sleep(0.1)

    def click(self, location): #pass in x and y, and it will click for you
        #print(location)
        # mouse.move(*scaling(button_positions[location]))
        # x, y = location
        # mouse.move(*location)
        self.move_mouse(self.scaling(location))
        mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
        time.sleep(0.5)

    def button_click(self, btn):
        #print(location)
        # x, y = location
        # mouse.move(*location)
        self.move_mouse(self.scaling(static.button_positions[btn]))
        mouse.click(button="left") # performs the pyautogui click function while passing in the variable from button_positions that matches button
        time.sleep(0.5)

    def press_key(self, key, timeout=0.1):
        keyboard.send(key)
        time.sleep(timeout)
