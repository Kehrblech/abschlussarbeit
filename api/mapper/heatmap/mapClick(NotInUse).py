import json
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import scipy.ndimage as ndimage
from PIL import Image

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
    # plt.imshow(data, cmap=cm, alpha=0.5)
 # Remove axis labels and color bar
    

    # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)  # Remove color bar
    plt.title(title)
    if save_path:
        try:
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)  # Save without extra white space
            print("Saved successfully at: "+str(save_path))
        except Exception as e:
            print("Error: "+str(e)) 
def startMapClick():
    screenshot_path = 'screenshot.png'
    image = Image.open(screenshot_path)

    w = image.width
    h = image.height


    # Create a numeric array for transformed_clicks
    transformed_clicks = np.zeros((h, w), dtype=float)

    # Load click data from JSON
    with open('collectedData.json', 'r') as file:
        data = json.load(file)
    webpageHeight = data['ScrollMax']
    scaleRate = h/webpageHeight
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
    heatmap_save_path = 'heatmap_click.png'

    # Plot and save the heatmap
    plotClick(transformed_clicks, 'Heatmap Click', screenshot_path, heatmap_save_path, w, h)


