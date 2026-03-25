# Pixel Morphing Animation

This Python script creates a captivating visual animation that morphs the pixels of a user-selected image into a target image of President Barack Obama. The animation is built using the `pygame` library for graphics and `tkinter` for the file selection GUI.

## How It Works

The script follows these main steps to create the animation:

1.  **Image Selection**: A file dialog window prompts the user to select a source image from their local files.
2.  **Image Loading and Processing**:
    *   The user's chosen image and a predefined target image (`President_Barack_Obama.jpg`) are loaded.
    *   Both images are scaled down to a consistent, smaller resolution to ensure the animation runs smoothly.
3.  **Pixel Color Bucketing**:
    *   To intelligently map pixels from the source to the target, the script groups pixels into "buckets" based on their color. Similar colors are placed in the same bucket.
    *   This process is done for both the source and target images.
4.  **Pixel Matching**:
    *   The script matches pixels from the source image to pixels in the target image.
    *   It prioritizes matching pixels that fall into the same color bucket, preserving the general color flow.
    *   Any remaining (unmatched) pixels are then randomly assigned to the remaining empty pixel slots in the target image.
5.  **Animation**:
    *   Each matched pair of a source pixel and a target position becomes a "particle."
    *   The script animates each particle, moving it from its original position in the source image to its new position in the target image over a set duration.
    *   An easing function is used to make the motion appear smooth and natural.

## Requirements

To run this script, you need to have the following Python libraries installed:

*   `pygame`: For graphics and animation.
*   `tkinter`: For the graphical user interface (file dialog). It is usually included with standard Python installations.

You can install the necessary library using pip:
```bash
pip install -r requirements.txt
```

## Usage

1.  Run the `main.py` script.
2.  A file dialog will appear. Select an image file (`.jpg`, `.png`, etc.) to use as the source.
3.  A `pygame` window will open, displaying the animation of your image's pixels morphing into the image of Barack Obama.
