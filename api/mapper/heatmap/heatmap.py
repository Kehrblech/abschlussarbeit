import json
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable  # Import make_axes_locatable
import numpy as np
import scipy.ndimage as ndimage
from PIL import Image


# !CODE HAS BEEN COPIED AND MADE FIT FOR MY PURPOSE! 
# HERE IS LINK TO ORIGINAL: https://python.plainenglish.io/creating-click-heatmaps-in-python-visualizing-user-interaction-with-web-pages-810630d83228


save_path_default = 'api/data/images/'

def plotScroll(data, title, image_path, save_path, w, h):
    colors = [(0, 0, 0, 0),       # Transparent
          (0.28, 0.58, 0.94), # #4895ef
          (0.26, 0.38, 0.93), # #4361ee
          (0.24, 0.22, 0.79), # #3f37c9
          (0.23, 0.04, 0.64), # #3a0ca3
          (0.29, 0.04, 0.64), # #480ca8
          (0.33, 0.04, 0.67), # #560bad
          (0.44, 0.04, 0.72), # #7209b7
          (0.71, 0.09, 0.72), # #b5179e
          (0.97, 0.15, 0.52)  # #f72585
         ]



    img = plt.imread(image_path)
    img = np.flipud(img)  # Flip the image vertically

    # Create a figure with subplots
    fig, ax = plt.subplots(figsize=(w/100, h/100))

    # Plot the heatmap on top of the background image
    ax.imshow(img, extent=[0, w, 0, h])
    cm = LinearSegmentedColormap.from_list('sample', colors)
    im = ax.imshow(data, cmap=cm, alpha=0.5)

    plt.title(title)
    if save_path:
        try:
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)  # Save without extra white space
            print("Saved successfully at: " + str(save_path))
            plt.savefig(save_path_default+'heatmap_scroll.png', bbox_inches='tight', pad_inches=0)  # Save without extra white space
            print("Saved successfully at: " + str(save_path_default))
        except Exception as e:
            print("Error: " + str(e))
            
def startMapScroll():
    screenshot_path = 'api/data/images/screenshot.png'
    # screenshot_path = 'api/static/assets/heatmap_click.png'
    image = Image.open(screenshot_path)

    w = image.width
    h = image.height
    # Load scroll data from JSON
    with open('api/data/json/collectedData.json', 'r') as file:
        data = json.load(file)
    scroll_data = data['scrollData']
    scroll_max = data['scrollMax']
    scaleRate = h/scroll_max 
    # Define the maximum scroll value


    # Create an empty numeric array for transformed scroll data
    transformed_scroll = np.zeros((h, w), dtype=float)

    # Populate the transformed_scroll array based on the scroll data
    for key, value in scroll_data.items():
        
        x = int(image.width)-75  # Use the scroll position as the x-coordinate
        y = int(int(key)*scaleRate)  # Scale the y-coordinate based on scroll_max
        if 0 <= x < w and 0 <= y < h:
            transformed_scroll[y, x] += 1

    # Apply a gaussian filter to the transformed_scroll array
    transformed_scroll = ndimage.gaussian_filter(transformed_scroll, sigma=15)

    # Define the save path for the heatmap
    heatmap_save_path = 'api/static/assets/heatmap_scroll.png'

    # Plot and save the heatmap
    plotScroll(transformed_scroll, 'Heatmap Scroll', screenshot_path, heatmap_save_path, w, h)


def plotClick(data, title, image_path, save_path, w, h):
    colors = [(0, 0, 0, 0), (0, 1, 1), (0, 1, 0.75), (0, 1, 0), (0.75, 1, 0),
              (1, 1, 0), (1, 0.8, 0), (1, 0.7, 0), (1, 0, 0)]

    img = plt.imread(image_path)
    img = np.flipud(img)  # Flip the image vertically

    # Create a figure with subplots
    fig, ax = plt.subplots(figsize=(w/100, h/100))

    # Plot the heatmap on top of the background image
    ax.imshow(img, extent=[0, w, 0, h])
    cm = LinearSegmentedColormap.from_list('sample', colors)
    im = ax.imshow(data, cmap=cm, alpha=0.5)
    # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    # plt.imshow(data, cmap=cm, alpha=0.5)
 # Remove axis labels and color bar
    

    # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)  # Remove color bar
    plt.title(title)
    if save_path:
        try:
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)  # Save without extra white space
            print("Saved successfully at: "+str(save_path))
            plt.savefig(save_path_default+'heatmap_click.png', bbox_inches='tight', pad_inches=0)  # Save without extra white space
            print("Saved successfully at: " + str(save_path_default))
        except Exception as e:
            print("Error: "+str(e)) 
def startMapClick():
    screenshot_path = 'api/data/images/screenshot.png'
    image = Image.open(screenshot_path)

    w = image.width
    h = image.height


    # Create a numeric array for transformed_clicks
    transformed_clicks = np.zeros((h, w), dtype=float)

    # Load click data from JSON
    with open('api/data/json/collectedData.json', 'r') as file:
        data = json.load(file)
    clicks = data['clicks']
    # Define your x and y offsets
    x_offset = 0  # Adjust this value based on your needs
    y_offset = 1.075  # Adjust this value based on your needs

    # Apply the offsets and populate the transformed_clicks array
    for click in clicks:
        x = int(click['x'] + x_offset)
        y = int(click['y'] * y_offset)
        if 0 <= x < w and 0 <= y < h:
            transformed_clicks[y, x] += 1  # You may adjust this based on your requirements

    # Apply a gaussian filter to the transformed_clicks array
    transformed_clicks = ndimage.gaussian_filter(transformed_clicks, sigma=15)
    
    

    # Define the save path for the heatmap
    heatmap_save_path = 'api/static/assets/heatmap_click.png'

    # Plot and save the heatmap
    plotClick(transformed_clicks, 'Heatmap Click', screenshot_path, heatmap_save_path, w, h)
    
def plotBoth(data, data2,title, image_path, save_path, w, h):
    colors = [(0, 0, 0, 0), (0, 1, 1), (0, 1, 0.75), (0, 1, 0), (0.75, 1, 0),
              (1, 1, 0), (1, 0.8, 0), (1, 0.7, 0), (1, 0, 0)]
    colors2 = [(0, 0, 0, 0),       # Transparent
          (0.28, 0.58, 0.94), # #4895ef
          (0.26, 0.38, 0.93), # #4361ee
          (0.24, 0.22, 0.79), # #3f37c9
          (0.23, 0.04, 0.64), # #3a0ca3
          (0.29, 0.04, 0.64), # #480ca8
          (0.33, 0.04, 0.67), # #560bad
          (0.44, 0.04, 0.72), # #7209b7
          (0.71, 0.09, 0.72), # #b5179e
          (0.97, 0.15, 0.52)  # #f72585
         ]
    img = plt.imread(image_path)
    img = np.flipud(img)  # Flip the image vertically

    # Create a figure with subplots
    fig, ax = plt.subplots(figsize=(w/100, h/100))

    # Plot the background image
    ax.imshow(img, extent=[0, w, 0, h], alpha=1)

    # Plot the first heatmap with transparency
    cm1 = LinearSegmentedColormap.from_list('sample', colors)
    im1 = ax.imshow(data, cmap=cm1, alpha=0.5)

    # Plot the second heatmap with transparency
    cm2 = LinearSegmentedColormap.from_list('sample', colors2)
    im2 = ax.imshow(data2, cmap=cm2, alpha=0.5)

    # Remove axis labels and color bar
    ax.set_xticks([])
    ax.set_yticks([])

    plt.title(title)
    if save_path:
        try:
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)  # Save without extra white space
            print("Saved successfully at: "+str(save_path))
            plt.savefig(save_path_default+'heatmap_merge.png', bbox_inches='tight', pad_inches=0)  # Save without extra white space
            print("Saved successfully at: " + str(save_path_default))
        except Exception as e:
            print("Error: "+str(e)) 
def startMapBoth():
    screenshot_path = 'api/data/images/screenshot.png'
    image = Image.open(screenshot_path)

    w = image.width
    h = image.height


    # Create a numeric array for transformed_clicks
    transformed_clicks = np.zeros((h, w), dtype=float)

    # Load click data from JSON
    with open('api/data/json/collectedData.json', 'r') as file:
        data = json.load(file)
    webpageHeight = data['scrollMax']
    clicks = data['clicks']
    # Define your x and y offsets
    x_offset = 0  # Adjust this value based on your needs
    y_offset = 1.075  # Adjust this value based on your needs

    # Apply the offsets and populate the transformed_clicks array
    for click in clicks:
        x = int(click['x'] + x_offset)
        y = int(click['y'] * y_offset)
        if 0 <= x < w and 0 <= y < h:
            transformed_clicks[y, x] += 1  # You may adjust this based on your requirements

    # Apply a gaussian filter to the transformed_clicks array
    transformed_clicks = ndimage.gaussian_filter(transformed_clicks, sigma=15)
    
    
    scroll_data = data['scrollData']
    scroll_max = data['scrollMax']
    scaleRate = h/scroll_max 
    # Define the maximum scroll value


    # Create an empty numeric array for transformed scroll data
    transformed_scroll = np.zeros((h, w), dtype=float)

    # Populate the transformed_scroll array based on the scroll data
    for key, value in scroll_data.items():
        
        x = int(image.width)-75  # Use the scroll position as the x-coordinate
        y = int(int(key)*scaleRate)  # Scale the y-coordinate based on scroll_max
        if 0 <= x < w and 0 <= y < h:
            transformed_scroll[y, x] += 1

    # Apply a gaussian filter to the transformed_scroll array
    transformed_scroll = ndimage.gaussian_filter(transformed_scroll, sigma=15)
    # Define the save path for the heatmap
    heatmap_save_path = 'api/static/assets/heatmap_merge.png'

    # Plot and save the heatmap
    plotBoth(transformed_clicks, transformed_scroll,'Heatmap Click & Scroll', screenshot_path, heatmap_save_path, w, h)


startMapClick()
startMapScroll()
startMapBoth()
