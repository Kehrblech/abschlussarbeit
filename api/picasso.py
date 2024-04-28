import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


# LInien Farbe 
color_green = (0, 128, 0, 255)
color_yellow = (255, 255, 0, 255)
color_orange = (255, 165, 0, 255)
color_red = (255, 0, 0, 255)

#import json
with open('collectedData.json', 'r') as file:
    data = json.load(file)

#get screenshot
screenshot_path = 'screenshot.png'  
image = Image.open(screenshot_path)
# image = image.convert("RGBA")
draw = ImageDraw.Draw(image, "RGBA")
#TODO Verbessern des Y wertes 
webpage_height =data['scrollMax'] #max(int(pos) for pos in data['scrollData'].keys())  # Maximale Y-Koordinate aus den Scroll-Daten
screenshot_height = image.height
scale_ratio = screenshot_height/webpage_height
print(scale_ratio)
x_offest =  150
y_offset = 1.066

#mark all clicks red 


#draw lines with scrolldata 
#threshold color steps 
red = 1.5
orange = .06
yellow = .03
green = .02


for position, scroll_value in data['scrollData'].items():
    scale_y = int(position)*scale_ratio
    if scroll_value > green and scroll_value < yellow:
        draw.line((0, scale_y, image.width, scale_y), fill=color_green, width=1)
    elif scroll_value > yellow and scroll_value < orange:
        draw.line((0, scale_y, image.width, scale_y), fill=color_yellow, width=2)
    elif scroll_value > orange and scroll_value < red:
        draw.line((0, scale_y, image.width, scale_y), fill=color_orange, width=5)
    elif scroll_value > red:
        draw.line((0, scale_y, image.width, scale_y), fill=color_red, width=30, )
        
for click in data['clicks']:
    x, y = click['x'] + x_offest, int(click['y']*y_offset)
    draw.ellipse((x-10, y-10, x+10, y+10), fill='red', outline='white')
        
    

#save image 
image.save('annotated_screenshot.png')
image.show()


