from PIL import Image
from StringIO import StringIO
from urllib2 import urlopen
import color_convertor
from math import sqrt

histogram_groups = ["660000","de6318","d3d100","8c8c00","293206","34e3e5","205260","1c0946","46008c",
                "33151a","e30e5c","3d1f00","5e1800","000000","980000","ff7f00","ffff00","88ba41",
                "006700","65f3c9","318c8c","31318c","5e318c","520f41","ff59ac","8c5e31","8c4600",
                "505050","ff0000","ffa000","eed54f","778c62","00ae00","77f6a7","628c8c","4a73bd",
                "77628c","840e47","ef8cae","8e7032","d1b45b","828283","e32636","ffc549","ffff6d",
                "8c8c62","00ff00","b2ffff","62778c","589ad5","ac59ff","8c6277","ead0cd","8c7762",
                "e2db9a","b5b5b6","fa624d","ffc898","ffffae","96d28a","a9ff00","d8ffb2","bdd6bd",
                "a1c4e9","a297e9","c6a5b6","ffdfef","c69c7b","ffffff","e7e7e7"]
lab_groups = [(value,color_convertor.rgb_to_cielab(*color_convertor.hex_to_rgb(value))) for value in histogram_groups]

def get_distance(a,b):
    return sqrt(sum( (a - b)**2 for a, b in zip(a, b)))

def best_group(pixel):
    lab_pixel = color_convertor.rgb_to_cielab(*pixel)
    best_group = ()
    min_distance = 200
    for group in lab_groups:
        distance = get_distance (group[1], lab_pixel)
        if distance < min_distance:
            min_distance = distance
            best_group = group
    return best_group[0] #hexcode


def get_colors(image):
    # Convert image into array of values for each point
    rgb_pixels = list(image.getdata())
    first_pixel = rgb_pixels[0]
    center_pixel = image.getpixel((image.size[0]/2,image.size[1]/2)) 
    best_group_first_pixel = best_group(first_pixel)
    ignore_first_pixel_group = True if best_group_first_pixel != best_group(center_pixel) else False

    # get the best group or each pixel
    best_groups = [(best_group(pixel), pixel) for pixel in list(image.getdata()) if pixel != first_pixel]
    #generate the histogram of the groups
    color_histogram = {}
    for group in best_groups:
        if group[0] in color_histogram:
            color_histogram[group[0]] = color_histogram[group[0]] + 1
        else:
            color_histogram[group[0]] = 1
    # drop the group of first pixel if that is not the main 
    if ignore_first_pixel_group:
        del color_histogram[best_group_first_pixel]
    return color_histogram
    


# test the module
url = 'http://ak1.polyvoreimg.com/cgi/img-thing/size/l/tid/81914589.jpg'
image = Image.open(StringIO(urlopen(url).read()))
get_colors(image)
