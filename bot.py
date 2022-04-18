from options import Options


class Bot(Options, ):
    def __init__(self, **options):
        super()
        
        self.start_time = time.time()
        self.running = True

        keyboard.add_hotkey("f11", self.print_stats, args=[self.statDict])


    def run(self):
        print("waiting for 5 seconds, please select the btd 6 window")
        time.sleep(5)
        # Check for obyn
        

        while self.running:
            print("selecting map")
            
            # Prevent alt+tab bug from happening
            self.press_key("alt")

            # Choose map
            self.select_map()   

            print("Game start")
            # main game
            self.main_game(self.instructions)
            # statDict["Won_Games"] += won
            # statDict["Lost_Games"] += lost

    def upgrade_tower(self, position, path):
        pass

    def place_tower(self, position, target):
        pass
    
    def change_target(self, position, target):
        pass

    def handleInstruction(self, instruction):
        upgrade_path = instruction["UPGRADE_DIFF"]
        
        monkey_position = instruction["POSITION"]
        target = instruction["TARGET"]
        keybind = instruction["KEYCODE"]


        # OM det inte finns någon upgrade så finns inte tornet placera ut
        if upgrade_path == "-":
            press_key(keybind)

            click(monkey_position)
            statDict["Last_Placement"] = instruction["MONKEY"]
            # press_key("esc")
        else:
            click(monkey_position)
            upgrade_path = upgrade_path.split("-")
            top, middle, bottom = tuple(map(int, upgrade_path))
            
            for _ in range(top):
                press_key(upgrade_keybinds["top"])

            for _ in range(middle):
                press_key(upgrade_keybinds["middle"])

            for _ in range(bottom):
                press_key(upgrade_keybinds["bottom"])
            
            statDict["Last_Upgraded"] = "Upgrading {} to {}; change {}".format(instruction['MONKEY'], instruction['UPGRADE'], instruction['UPGRADE_DIFF'])
            press_key("esc")


        # Om target är - så låt vara
        # Special case för mortar 
        if instruction["TARGET_POS"] != "-":
            pyautogui.moveTo(scaling(monkey_position))
            time.sleep(0.5)
            mouse.click(button="left")

            time.sleep(1)

            pyautogui.moveTo(scaling(button_positions["TARGET_BUTTON_MORTAR"]))
            
            time.sleep(1)
            mouse.press(button='left')
            time.sleep(0.5)
            mouse.release(button='left')

            time.sleep(1)

            pyautogui.moveTo(scaling(instruction["TARGET_POS"]))
            time.sleep(0.5)
            mouse.press(button='left')
            time.sleep(0.5)
            mouse.release(button='left')

            time.sleep(1)

            press_key("esc")

            # Print info
            statDict["Last_Target_Change"] = instruction["MONKEY"]

        if instruction["ROUND_START"] == "TRUE":
            press_key("space")
            press_key("space")


            # Om den har en specifik target
        if target != "-":
            splitTarget = target.split(", ")

            # special cases
            if target == "STRONG":
                click(monkey_position)
                press_key("ctrl+tab")
                press_key("esc")
            elif len(splitTarget) > 1:
                click(monkey_position)
                press_key("tab")
                time.sleep(3)
                press_key("ctrl+tab")
                press_key("ctrl+tab")
                press_key("esc")
            elif target == "CLOSE":
                click(monkey_position)
                press_key("tab")            
                press_key("esc")
            
            # Print info
            statDict["Last_Target_Change"] = instruction["MONKEY"]


    def check_levelup(self):

        found = pyautogui.locateOnScreen(levelup_path, confidence=0.9)

        if found:
            print("level up detected")
            return True
        else:
            return False

    def easter_event_check(self):
        found = pyautogui.locateOnScreen(easter_path, confidence=0.9)
        if found != None:
            print("easter collection detected")
            button_click("EASTER_COLLECTION") #DUE TO EASTER EVENT:
            time.sleep(1)
            button_click("LEFT_INSTA") # unlock insta
            time.sleep(1)
            button_click("LEFT_INSTA") # collect insta
            time.sleep(1)
            button_click("RIGHT_INSTA") # unlock r insta
            time.sleep(1)
            button_click("RIGHT_INSTA") # collect r insta
            time.sleep(1)
            button_click("F_LEFT_INSTA")
            time.sleep(1)
            button_click("F_LEFT_INSTA")
            time.sleep(1)
            button_click("MID_INSTA") # unlock insta
            time.sleep(1)
            button_click("MID_INSTA") # collect insta
            time.sleep(1)
            button_click("F_RIGHT_INSTA")
            time.sleep(1)
            button_click("F_RIGHT_INSTA")
            time.sleep(1)

            time.sleep(1)
            button_click("EASTER_CONTINUE")


            # awe try to click 3 quick times to get out of the easter mode, but also if easter mode not triggered, to open and close profile quick
            button_click("EASTER_EXIT")
            time.sleep(1)
        
    def hero_obyn_check(self):
        found = pyautogui.locateOnScreen(obyn_hero_path, confidence=0.9)
        if not found:
            button_click("HERO_SELECT")
            button_click("SELECT_OBYN")
            button_click("CONFIRM_HERO")
            press_key("esc")

    def victory_check(self):
        found = pyautogui.locateOnScreen(victory_path, confidence=0.9)
        #jprint(victory_path)
        if found:
            return True
        else:
            return False

    def defeat_check(self):     
        #jprint(defeat_path)
        found = pyautogui.locateOnScreen(defeat_path, confidence=0.9)
        if found:
            return True
        else:
            return False

    def exit_level(self):
        button_click("VICTORY_CONTINUE")
        time.sleep(2)
        button_click("VICTORY_HOME")
        time.sleep(4)

        easter_event_check()
        time.sleep(2)

    def select_map(self):
        time.sleep(2)

        button_click("HOME_MENU_START") # Move Mouse and click from Home Menu, Start
        button_click("EXPERT_SELECTION") # Move Mouse to expert and click
        button_click("RIGHT_ARROW_SELECTION") # Move Mouse to arrow and click
        button_click("DARK_CASTLE") # Move Mouse to Dark Castle
        button_click("HARD_MODE") # Move Mouse to select easy mode
        button_click("CHIMPS_MODE") # Move mouse to select Standard mode
        button_click("OVERWRITE_SAVE") # Move mouse to overwrite save if exists
        time.sleep(3)
        button_click("CONFIRM_CHIMPS")

    def menu_check(self):
        #jprint(menu_path)
        found = pyautogui.locateOnScreen(menu_path, confidence=0.9)
        if found:
            return True
        else:
            return False

    def insta_monkey_check(self):
        found = pyautogui.locateOnScreen(insta_monkey, confidence=0.9)
        if found: 
            return True
        else:
            return False

    def abilityAvaliabe(self, last_used, cooldown, fast_forward=True):
        # Möjlighet att välja beroende på ifall fast_forward är på eller ej
        m = 1
        if fast_forward:
            m = 3

        return (time.time() - last_used) >= (cooldown / m)

    def main_game(self, instructions):
        
        current_round = -1
        ability_one_timer = time.time()
        ability_two_timer = time.time()
        
        finished = False

        width, height = pyautogui.size()
        middle_of_screen = width//2, height//2

        inst_idx = 0
        
        # main ingame loop
        while not finished:
            # time.sleep(0.2)
            if inst_idx < len(instructions):
                current_instruction = instructions[inst_idx]
            
            # Check for levelup or insta monkey (level 100)
            if check_levelup() or insta_monkey_check():
                click(middle_of_screen)
                click(middle_of_screen)

            # Check for finished or failed game
            if defeat_check() or victory_check():
                # DEBUG
                if defeat_check():
                    print("Defeat detected on round {}; exiting level".format(current_round))
                elif victory_check():
                    print("Victory detected; exiting level")    
                
                exit_level()
                finished = True
                continue

            if getRound():
                current_round, _ = getRound()
                statDict["Current_Round"] = current_round

            # Saftey net; use abilites
            if current_round >= 39 and abilityAvaliabe(ability_one_timer, 35):
                press_key("1")
                ability_one_timer = time.time()
            
            if current_round >= 51 and abilityAvaliabe(ability_two_timer, 90):
                press_key("2")
                ability_two_timer = time.time()

            # handle current instruction when current round is equal to instruction round
            if int(current_instruction['ROUND']) == current_round and inst_idx < len(instructions):
                handleInstruction(current_instruction)
                inst_idx += 1