#!/usr/bin/python3

from PIL import Image
from collections import Counter

def frequent_shape(image_paths):
    """
    Determines the most frequent width and height from a list of image file paths.

    Parameters:
    -----------
    image_paths : list of str
        A list of file paths pointing to image files.

    Returns:
    --------
    tuple (int, int)
        A tuple containing the most frequent width and the most frequent height across all images.
        - The first element is the most frequent width (in pixels).
        - The second element is the most frequent height (in pixels).

    Description:
    ------------
    The function takes a list of image paths, opens each image using the Pillow library (`PIL.Image`), 
    and retrieves the dimensions (width and height) of each image. It then computes the most frequent 
    width and the most frequent height using the `Counter` class from the `collections` module.

    Example:
    --------
    >>> image_paths = ["image1.jpg", "image2.jpg", "image3.png"]
    >>> frequent_shape(image_paths)
    (1920, 1080)

    In this example, the most frequent width is 1920 pixels and the most frequent height is 1080 pixels.
    """
    heights = []
    widths = []
    
    # Itera sobre a lista de paths de imagens
    for path in image_paths:
        with Image.open(path) as img:
            width, height = img.size
            heights.append(height)
            widths.append(width)
    
    # Encontra as dimensões mais frequentes
    most_common_height = Counter(heights).most_common(1)[0][0]
    most_common_width = Counter(widths).most_common(1)[0][0]
    
    return (most_common_width,most_common_height)
