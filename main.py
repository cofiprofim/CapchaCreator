from captcha.image import ImageCaptcha
from PIL import Image
import random
import keyboard
import os
import ctypes

WidthCmd = 120
HeightCmd = 20
text = [" ", " ", " ", " "]

if not os.path.exists("captcha"):
    os.mkdir("captcha")

if os.name == "nt":
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("CaptchaSolver")
    except:
        pass

def create_captcha(captcha_path):
    imagee = ImageCaptcha()
    captcha_text = str(random.randint(1000, 9999))
    imagee.write(captcha_text, captcha_path)
    return captcha_text

def print_captcha(captcha_path, text):
    print(" ┌" + "─" * (WidthCmd - 4) + "┐")
    image = Image.open(captcha_path)
    
    WidthPng, HeightPng = image.size

    PixelsX = [round(WidthPng / WidthCmd * i) for i in range(WidthCmd)]
    PixelsY = [round(HeightPng / HeightCmd * i) for i in range(HeightCmd)]
    for y in (PixelsY):
        for index, x in enumerate(PixelsX, 1):
            a, b, c = image.getpixel((x, y))
            if index in [1, len(PixelsX)]:
                print(" ", end="")
            elif index in [2, len(PixelsX) - 1]:
                print("│", end="")
            elif not (a >= 200 and a <= 270 and b >= 200 and b <= 270 and c >= 200 and c <= 270):
                print("█", end="")
            else:
                print(" ", end="")
    print(f""" └──────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────┘ 
                                                            │                                                           
                                                        ┌───┴───┐                                                       
                                                        │{text[0]} {text[1]} {text[2]} {text[3]}│                       
                                                        └───────┘                                                       
""")

def cls_console():
    os.system("cls" if os.name == "nt" else "clear")

def keyb(key):
    global num
    if key.name == "enter" and num == "".join(text):
        cls_console()
        print("Right!")
    elif key.name == "enter" and num != "".join(text):
        cls_console()
        print("Wrong!")
    elif key.name == "r":
        cls_console()
        num = create_captcha("captcha/captcha.png")
        print_captcha("captcha/captcha.png", text)
    elif key.name == "backspace":
        if text.count(" ") != 4:
            for index, word in enumerate(text[::-1]):
                if word != " ":
                    text[(index + 1) * -1] = " "
                    break
            cls_console()
            print_captcha("captcha/captcha.png", text)
    elif key.name in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
        if text.count(" ") != 0:
            for index, word in enumerate(text):
                if word == " ":
                    text[index] = key.name
                    break
            cls_console()
            print_captcha("captcha/captcha.png", text)

cls_console()
num = create_captcha("captcha/captcha.png")
print_captcha("captcha/captcha.png", text)

keyboard.on_press(keyb)
keyboard.wait()