from pynput import mouse
import pyautogui
import time
from PIL import Image
import math



coords = []
def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.middle:
        print(x,y)
        coords.append((x,y))
        if(len(coords)==2):
            return False


mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

region = None
while True:
    if len(coords) == 2:
        c1 = coords[0]
        c2 = coords[1]
        region = (c1[0], c1[1], c2[0]-c1[0], 2)
        break

max_adren = region[2]
min_adren = 1
while True:
    time.sleep(0.25)
    st=time.time()
    abar = pyautogui.screenshot(region=region)
    pixels = abar.load()
    adren_pixels = 0
    for i in range(abar.size[0]):
            r,g,b = pixels[i,0]
            if r > 180 and g > 90:
                adren_pixels += 1
    st = time.time() - st       
    print(st, math.ceil((adren_pixels)*100/(max_adren - min_adren)),'%')
