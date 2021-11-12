from PIL import Image
from math import pi, sqrt
import glob
import time

"""
    Loads the color palette

    Parameter
        palette: The palette file to load.
    
    Return
        A list of 3 element tuples
"""
def load_color_palette (palette):
    pal = {}
    with open("./palettes/" + palette + ".pal") as file:
        for line in file:
            l = line.split()
            pal[l[0]] = (int(l[len(l)-3].strip(',')), int(l[len(l)-2].strip(',')), int(l[len(l)-1].strip(',')))
            # color = (int(l[len(l)-3].strip(',')), int(l[len(l)-2].strip(',')), int(l[len(l)-1].strip(',')))
            # pal.append(color)
    return pal

"""
    Loads all the images in the images folder.

    Parameter
        extension: the file extension for the image. Default parameter is the jpg

    Return
        Returns a list of PIL Images.
"""
def load_images (extension = "jpg"):
    images = []
    for filename in glob.glob('./images/*.*'):
        if filename[-3:] == extension:
            img = Image.open(filename)
            images.append(img)
    return images

"""
    Gets the color distance between color1 and color2.
    Uses the formula from: https://en.wikipedia.org/wiki/Color_difference

    Parameter
        color1: A 3 element tuple where each element is a value representing a r, g, b value.
        color2: A 3 element tuple where each element is a value representing a r, g, b value.
    
    Return
        The distance between the colors.
"""
def get_color_distance_rgb (color1, color2):
    dR = color1[0] - color2[0]
    dG = color1[1] - color2[1]
    dB = color1[2] - color2[2]
    avg_red = (color1[0] + color2[0]) / 2

    distance = sqrt (dR ** 2 + dG ** 2 + dB ** 2)

    return distance

"""
    Gets the distance between the color in the lab format.

    Parameters
        color1: a 3 element tuple in the lab color format.
        color2: a 3 element tuple in the lab color format.
    
    Return
        Returns the distance between the color.
"""
def get_color_distance_lab (color1, color2):
    da = color2[1] - color1[1]
    db = color2[2] - color1[2]
    dL = color2[0] - color1[0]
    return sqrt(da ** 2 + db ** 2) + abs(dL)

"""
    Converts the color from an color in the palette.

    Parameter
        color: the color to convert to the closet color in the palette.
        palette: the list of colors in the palette.

    Return
        A image in the palette that is the closet color in the palette.
"""
def convert_color (color, palette):
    res = (-1, -1, -1)
    dist = 999999999999

    # threshold Testing
    dRG = abs(color[0] - color[1])
    dGB = abs(color[1] - color[2])
    dRB = abs(color[0] - color[2])
    threshold = 5

    greys = []
    nongreys = []
    pal = []
    
    for c in palette.keys():
        if "grey" in c.lower():
            greys.append(palette[c])
        else:
            nongreys.append(palette[c])
        pal.append(palette[c])

    for c in pal:
        c1 = rgb2lab(color)
        c2 = rgb2lab(c)
        d = get_color_distance_lab(c1, c2)
            
        if d < dist:
            res = c
            dist = d

    # if dRG < threshold and dGB < threshold and dRB < threshold:
    #     for c in greys:
    #         c1 = rgb2lab(color)
    #         c2 = rgb2lab(c)
    #         d = get_color_distance_lab(c1, c2)

    #         if d < dist:
    #             res = c
    #             dist = d
    # else:
    #     for c in nongreys:
    #         c1 = rgb2lab(color)
    #         c2 = rgb2lab(c)
    #         d = get_color_distance_lab(c1, c2)
            
    #         if d < dist:
    #             res = c
    #             dist = d

    return res

"""
    Converts a color from the rgb format to the lab format.
    From: https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python

    Parameter
        color: a rgb represented as a 3 element tuple.
    
    Returns
        A color in Lab formats as a 3 element tuple.
"""
def rgb2lab (color):
    num = 0
    RGB = [0, 0, 0]

    for value in color:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505

    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float(XYZ[0]) / 95.047
    XYZ[1] = float(XYZ[1]) / 100.0
    XYZ[2] = float(XYZ[2]) / 108.883

    num = 0
    for value in XYZ:
        if value > 0.008865:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]
    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return (Lab[0], Lab[1], Lab[2])

def get_adjacent_colors (color, range_val):
    colors = []
    colors.append(color)
    
    for r in range(-range_val, range_val):
        colors.append((color[0] + r, color[1], color[2]))
        colors.append((color[0], color[1] + r, color[2]))
        colors.append((color[0], color[1], color[2] + r))

        colors.append((color[0] + r, color[1] + r, color[2]))
        colors.append((color[0], color[1] + r, color[2] + r))
        colors.append((color[0] + r, color[1], color[2] + r))

        colors.append((color[0] + r, color[1] + r, color[2] + r))

    return colors

"""
    Lanch point function.
"""
def main ():
    palette_name = 'c64'
    palette = load_color_palette(palette_name)
    images = load_images()

    saved_pixels = {}

    iteration = 1
    for img in images:
        pixels = img.load()
        st = time.time()

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if pixels[x, y] in saved_pixels:
                    pixels[x, y] = saved_pixels[pixels[x, y]]
                else:
                    colors = get_adjacent_colors(pixels[x, y], 35)
                    color = convert_color(colors[0], palette)
                    for c in colors:
                        saved_pixels[c] = color
                    pixels[x, y] = color

        et = time.time()
        img.save('./results/' + palette_name + '_image' + str(iteration) + '.jpg')
        iteration = iteration + 1
        print(str(et-st) + " seconds")

if __name__ == "__main__":
    main()