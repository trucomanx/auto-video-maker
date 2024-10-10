#!/usr/bin/python3

from PIL import Image
from collections import Counter

def frequent_shape(image_paths):
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
