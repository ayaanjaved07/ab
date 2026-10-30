# mp
import os
import pyautogui
import pydirectinput
from pywinauto.application import Application
import time
import cv2
import numpy as np
import threading
import configparser
from rich import print
import keyboard
from datetime import date

config  = configparser.ConfigParser()
config.read("settings.ini")

sleep = float(config["settings"]["sleep"])
# cars_list = config["settings"]["cars_list"].split(", ")

iterations = int(config["settings"]["number"])
counter = 1
ticket_refill = config.getboolean("settings", "ticket_refill", fallback=False)
token_refill = config.getboolean("settings", "token_refill", fallback=False) 
play_infinitely = config.getboolean("settings", "play_infinitely", fallback=False)
play_infinitely_sleep = int(config["settings"]["play_infinitely_sleep"])
car_sleep = float(config["settings"]["car_switch_sleep"])
route = int(config["settings"]["route"])
watch_ad = config.getboolean("settings", "watch_ad", fallback=False)
ad_ticket_refill = config.getboolean("settings", "ad_ticket_refill", fallback=False)
car_tlr = config.getfloat("settings", "car_tlr", fallback=0.85)
valour = config.getboolean("settings", "valour", fallback=False)
manual_route_config = config.getboolean("settings", "route_config", fallback=False)
route_set = config.get("settings", "route_set", fallback="").split(", ")
manual_event_selection = config.getboolean("settings", "event_keyboard", fallback=False)
event_number = int(config.get("settings", "event_number", fallback="1"))

league = config.get("settings", "league", fallback="gold")
first_selection = True

if token_refill:
    ticket_refill = True


nitro_thread = False
escape_thread = threading.Event()
pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False


current_dir = f"{os.getcwd()}\\bot.exe"
app2 = Application().connect(title=current_dir)
console = app2[current_dir]
console.set_focus()
console.move_window(0, 720, 1280, 360)
time.sleep(sleep*0.1)

window_title = config["settings"]["window_title"]

while True:
    try:
        app1 = Application().connect(title=window_title)
        window = app1[window_title]
        window.set_focus()
        window.move_window(0, 0, 1280, 720)
        time.sleep(sleep * 1)
        break  
    except:
        print(f"Cannot detect the game window. Open it and press Enter to try again.", end="")
        input("")






def locate(image, x = 1290, y = 730, tolerance = 0.8, a = 0, b = 0):
    small = cv2.imread(image)
    small_h, small_w, _ = small.shape
    region_width = x - a
    region_height = y - b
    big = pyautogui.screenshot(region=(a, b, region_width, region_height))
    big = np.array(big)  
    big = big[:, :, ::-1].copy()
    
    result = cv2.matchTemplate(big, small, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= tolerance:
        center_x = max_loc[0] + small_w // 2 + a
        center_y = max_loc[1] + small_h // 2 + b
        return (center_x, center_y)
    
    else:
        return None
        
def click_if_found(image, n = 1, x = 1290, y = 730, tolerance = 0.85, a = 0, b = 0):
    coord = locate(image, x, y, tolerance, a, b)
    if coord is not None:
        pyautogui.moveTo(coord[0], coord[1], 0.3, pyautogui.easeOutQuad)
        pyautogui.click(clicks=n)
        return True
    return False

def ceoq(x, y, s = 0.1, z = 0.3):
    pyautogui.moveTo(x, y, z, pyautogui.easeOutQuad)
    pyautogui.click()
    time.sleep(s)


def initialize():
    print("[bold red]Waiting[/bold red]")
    while True:
        if locate(r"images\coins.png") is not None:
            break
        else:
            pydirectinput.press("escape")
            time.sleep(sleep*1)
    print("[bold green]Running[/bold green]")

    while True:
        time.sleep(sleep*1.5)
        if click_if_found(r"images\cross.png"):
            time.sleep(sleep*1)

        if click_if_found(r"images\home.png", 1):
            print("Go to Home")
            time.sleep(sleep*1)
            
        elif click_if_found(r"images\mp\mp_b.png", 2):
            time.sleep(sleep*2)
            if click_if_found(r"images\claim.png", 2):
                print("Claim")
                initialize()
            print("Multiplayer")
            break
        elif click_if_found(r"images\mp\mp_w.png", 2):
            time.sleep(sleep*2)
            if click_if_found(r"images\claim.png", 2):
                print("Claim")
                initialize()
            print("Multiplayer")
            break

    time.sleep(sleep*0.5)

    # for i in range(3):
    #     if click_if_found(r"images\rtc.png", 1) is True:
    #         for i in range(20):
    #             pydirectinput.press("left")
    #         break
    #     else:
    #         time.sleep(sleep*1)
    # pydirectinput.press("left")

    # if manual_event_selection:
    #     for i in range(event_number):
    #         pydirectinput.press("right")
    #         time.sleep(sleep*0.1)
    #     pydirectinput.press("enter")
    # else:
    #     while True:
    #         if click_if_found(r"images\loot\hunt.png", 2):
    #             print("Hunt Lobby")
    #             break
    #         else:
    #             pydirectinput.press("right")


           
    return True





def find_car():
    global escape_thread
    global first_selection
    time.sleep(sleep*2)
    escape_thread.set()
    
    while True:
        # if click_if_found(r"images\loot\auto.png"):
        #     time.sleep(sleep*15)
        #     pydirectinput.press("escape")
        #     time.sleep(sleep*10)

        if locate(r"images\mp\play1.png", 1290, 730, 0.8, 986, 563) is not None:
            time.sleep(sleep*1)
            
            if click_if_found(r"images\mp\play1.png", 1, 1290, 730, 0.8, 986, 563):
                print("Car Lobby")
                time.sleep(sleep*1)
            # while locate(r"images\loot\car_selection.png") is None:
            #     time.sleep(sleep*0.5)
            time.sleep(sleep*2)
            print("[wheat4]Selecting Car[/wheat4]")
            if first_selection:
                first_selection = False
                ceoq(1132, 144, 1.5)
                ceoq(390, 275, 1.5)
                ceoq(384, 380, 1.5)
                ceoq(387, 486, 1.5)
                ceoq(284, 570, 5)
                
                img_path = f"images\\mp\\{league}.png"
                tmp = 0
                while click_if_found(img_path, 1, 957, 185, 0.8, 641, 98) is False and tmp != 10:
                    tmp += 1
                    time.sleep(sleep*1)
            break 
        # selection system, may change later

    
    time.sleep(sleep*2.5)
    pydirectinput.press("enter")
    time.sleep(sleep*1)
    pydirectinput.press("enter")
    time.sleep(sleep*2)
    while True:
        # for i in range(len(cars_list)):
        #     image_path = f"images\\cars\\{cars_list[i]}.png"
            # if locate(image_path, 620, 180, car_tlr) != None:
                
            # if locate(image_path, 428, 216, 0.85) != None:
            #     print(f"[wheat4]Found Car: {cars_list[i]}[/wheat4]")
            #     click_if_found(r"images\td.png")
            #     time.sleep(sleep*1)
                
                # for i in range(3):
                #     if click_if_found(r"images\play2.png", 1, 1290, 730, 0.8):   
                #         time.sleep(sleep*1)
                #         return True
        
        if click_if_found(r"images\td.png"):
            time.sleep(sleep*2)
        for i in range(3):
            if click_if_found(r"images\mp\play2.png", 1, 1290, 730, 0.8): 
                escape_thread.clear()
                time.sleep(sleep*3)
                return True
                

        else:
            pyautogui.moveTo(488, 353, 0.3, pyautogui.easeOutQuad)
            pyautogui.click()
            time.sleep(car_sleep)


def escape():
    global escape_thread
    escape_counter = 0
    while True:
        time.sleep(1)
        if escape_thread.is_set():
            for i in range(150):
                if escape_thread.is_set() is False:
                    break
                time.sleep(1)
            if escape_thread.is_set():
                pydirectinput.press("escape")
                escape_counter += 1
                if escape_counter == 5:
                    print("Seems like bot is stuck")
                    print("Starting from the beginning")
                    play()


def prep():
    time.sleep(sleep*1.5)
    if locate(r"images\refill.png") != None:
        print("[red]Out of Tickets[/red]")
        if ticket_refill:
            
            if click_if_found(r"images\ticket_refill.png"):
                time.sleep(sleep*1)
                while locate(r"images\play2.png") is None:
                    pydirectinput.press("escape")
                    time.sleep(10) 
                   
            elif token_refill:    
                time.sleep(sleep*1)
                for i in range(3):
                    click_if_found(r"images\token_refill.png")
                    time.sleep(sleep*1)
                print("token refill")
                    
                while locate(r"images\play2.png") is None:
                    pydirectinput.press("escape")
                    time.sleep(10) 

            elif ad_ticket_refill is True and locate(r"images\watch_ad.png") is not None:
                watch_ad_c = 0
                while True:
                    if locate(r"images\full_tickets.png") is not None:
                        initialize()
                        find_car()
                        break
                    elif watch_ad_c == 24:
                        print("Sleeping for 10 minutes")
                        time.sleep(10*60)
                        initialize()
                        find_car()
                        break

                    time.sleep(5)
                    if click_if_found(r"images\watch_ad.png"):
                        print("Watching Ad")
                        watch_ad_c = 0
                    else:
                        watch_ad_c += 1

            else:
                print("[red]Out of Refills[/red]")
                if play_infinitely == False:
                    print("[wheat4]Out of tickets[/wheat4]")
                    input("Press enter to exit")
                    os._exit(0)
                elif play_infinitely == True:
                    print(f"Sleeping for {play_infinitely_sleep} minutes")
                    pydirectinput.press("escape")
                    time.sleep(sleep*1)
                    click_if_found(r"images\home.png", 1)
                    for i in range(play_infinitely_sleep):
                        time.sleep(60)
                        pyautogui.moveTo(100, 100, 0.3, pyautogui.easeOutQuad)
                        pyautogui.moveTo(200, 200, 0.3, pyautogui.easeOutQuad)
                    if click_if_found(r"images\cross.png"):
                        time.sleep(sleep*1)
                    initialize()
                    find_car()
                   
                    
            
            time.sleep(sleep*1)
            click_if_found(r"images\play2.png", 1, 1290, 730, 0.8)

        elif ticket_refill == False:

            if ad_ticket_refill is True and locate(r"images\watch_ad.png") is not None:
                watch_ad_c = 0
                while True:
                    if locate(r"images\full_tickets.png") is not None:
                        initialize()
                        find_car()
                        break
                    elif watch_ad_c == 24:
                        print("Sleeping for 10 minutes")
                        time.sleep(10*60)
                        initialize()
                        find_car()
                        break

                    time.sleep(5)
                    if click_if_found(r"images\watch_ad.png"):
                        print("Watching Ad")
                        watch_ad_c = 0
                    else:
                        watch_ad_c += 1

            elif play_infinitely ==  True:
                print(f"Sleeping for {play_infinitely_sleep} minutes")
                pydirectinput.press("escape")
                time.sleep(sleep*1)
                click_if_found(r"images\home.png", 1)
                for i in range(play_infinitely_sleep):
                    time.sleep(60)
                    pyautogui.moveTo(100, 100, 0.3, pyautogui.easeOutQuad)
                    pyautogui.moveTo(200, 200, 0.3, pyautogui.easeOutQuad)
                if click_if_found(r"images\cross.png"):
                    time.sleep(sleep*1)
                initialize()
                find_car()
            elif play_infinitely == False:
                input("Press enter to exit")
                os._exit(1)

    print("[grey66]Waiting for Race to start[/grey66]")
    while True:
        time.sleep(0.05)
        if locate(r"images\signs\race_started.png") != None:
            print("[grey66]Race Started[/grey66]")
            return True
        
        # if locate(r"images\loot\completed.png") is not None:
            
        #     time.sleep(1)
        #     pyautogui.moveTo(230, 559, 0.3, pyautogui.easeOutQuad)
        #     pyautogui.click()
        #     print("Never show again")
        #     time.sleep(1)
        #     while click_if_found(r"images\loot\anyway.png") is False:
        #         time.sleep(1)


def nitro():
    while nitro_thread:
        pyautogui.press("space")
        time.sleep(1)
    return

def in_race():
    global nitro_thread
    global escape_thread
    global first_selection
    nitro_thread = True
    escape_thread.clear()
    while True:

        while True:
            if locate(r"images\signs\next.png") is not None:
                break

            if manual_route_config:
                routes_number = len(route_set)
                while True:
                    if locate(r"images\signs\next.png") is not None:
                        break

                    for i in range(routes_number):
                        if locate(f"images\\signs\\{route_set[i]}_s.png", 783, 203, 0.7) != None:
                            break
                        click_if_found(f"images\\signs\\{route_set[i]}.png", 1, 770, 190) 
                    
            elif manual_route_config is False:
                if route == 1:
                    while True:
                        if locate(r"images\signs\ramp1_s.png", 783, 203, 0.7) != None or locate(r"images\signs\ramp2_s.png", 783, 203, 0.7) != None or locate(r"images\signs\flat_ramp_s.png", 783, 203, 0.7) != None or locate(r"images\signs\bottle2_s.png", 783, 203, 0.7) != None:
                            pass
                        else:
                            break

                    click_if_found(r"images\signs\ramp1.png", 1, 770, 190) or click_if_found(r"images\signs\ramp2.png", 1, 783, 203) or click_if_found(r"images\signs\bottle2.png", 1, 783, 203) or click_if_found(r"images\signs\bottle1.png", 1, 783, 203) or click_if_found(r"images\signs\flat_ramp.png", 1, 783, 203)

                elif route == 2:
                    while True:
                        if locate(r"images\signs\bottle2_s.png", 783, 203, 0.7) != None:
                            pass
                        else:
                            break
                    click_if_found(r"images\signs\bottle2.png", 1, 783, 203) or click_if_found(r"images\signs\bottle1.png", 1, 783, 203)




        if locate(r"images\signs\next.png") is not None:
            nitro_thread = False
            time.sleep(sleep*0.5)
            escape_thread.set()

            while True:
                time.sleep(sleep*0.01)
                if click_if_found(r"images\signs\next.png"):
                    print("Next")
                    time.sleep(sleep*1)

                if locate(r"images\signs\watch_ad.png") is not None and watch_ad is True:
                    click_if_found(r"images\signs\watch_ad.png")
                    print("Watch Ad")
                    time.sleep(sleep*1)
                elif click_if_found(r"images\signs\miss_out.png"):
                    print("Ad Skip")
                    time.sleep(sleep*1)
                if click_if_found(r"images\signs\next_w.png"):
                    time.sleep(sleep*0.5)
                

                # maybe change this later
                if locate(r"images\mp\demoted.png", 1290, 730) is not None:
                    first_selection = True
                    pydirectinput.press("escape")
                    time.sleep(sleep*5)
                    LEAGUES = ["bronze", "silver", "gold", "plat", "champion", "legend"]
                    idx = LEAGUES.index(league)
                    league = LEAGUES[max(0, idx - 1)]

                if locate(r"images\mp\play1.png", 1290, 730) is not None:
                    time.sleep(sleep*1)
                    if locate(r"images\mp\play1.png") is not None:
                        escape_thread.clear()
                        return True






def race():
    global escape_thread
    t1 = threading.Timer(1, nitro)
    t1.start()
    in_race()

def exit_program():
    print("Exiting program...")
    os._exit(2)


#--------------------------------------------------------------------------------------------------------------------------------------------

def play():
    global escape_thread
    global counter



    initialize()
    if play_infinitely == True:
        while True:
            escape_thread.clear()
            print(f"[bold blue3]-----{counter}-----[/bold blue3]")
            time.sleep(sleep*1)
            find_car()
            prep()
            race()    
            counter += 1
            time.sleep(sleep*3)
    elif play_infinitely == False:
        escape_thread.clear()
        for i in range(iterations):
            print(f"[bold blue3]-----{counter}/{iterations}-----[/bold blue3]")
            time.sleep(sleep*1)
            find_car()
            prep()
            race()    
            counter += 1
            time.sleep(sleep*3)


    input("Press Enter to Exit:")

x = date.today()
y = date(2027, 1, 1)
if(x > y):
    os._exit(3)

keyboard.add_hotkey('ctrl+shift+q', exit_program)
print("Press CTRL + SHIFT + Q to exit in between")

t2 = threading.Timer(1, escape)
t2.start()
escape_thread.clear()
play()