from PIL import Image
from StringIO import StringIO
from urllib2 import urlopen
import color_convertor
from math import sqrt
from scipy import misc
from scipy import ndimage

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

def get_mask(image): #this gets True for picel poistions which are foreground
    image_mc = image.convert('L') # convert to grayscale
    ar = misc.fromimage(image_mc) # get array
    shape = ar.shape
    ar = ar.reshape(shape[0]*shape[1]) #reshape the array to be 1 dim
    ar = ndimage.gaussian_filter(ar, sigma=256/(4.*10)) #apply gaussian smoothing filter
    mask = list((ar < ar.mean())) # boolean list of pixels that matter 
    return  mask

def get_colors(image):
    image = image.convert('RGB') #convert to RGB as rest of code needs RGB
    image.thumbnail((image.size[0]/2,image.size[1]/2)) #reduce the size to realy small to speed up thinga
    rgb_pixels = list(image.getdata()) # Convert image into array of values for each point
    mask = get_mask(image) # get mask, list of boolean  of pixels that matter
    best_groups = [best_group(pixel) for i, pixel in enumerate(rgb_pixels) if mask[i]]     # get the best group or each pixel
    color_histogram = {x:best_groups.count(x) for x in set(best_groups)}     #generate the histogram of the groups
    if not color_histogram: return False
    from operator import itemgetter     #return a sorted list
    color_histogram = sorted(color_histogram.items(), key=itemgetter(1), reverse=True)
    top_color_count = color_histogram[0][1]
    top_colors = [color[0] for color in color_histogram if color[1] > 0.8 * top_color_count]
    return color_histogram, top_colors    

# test the module
url = 'https://www.polyvore.com/cgi/img-thing/size/orig/tid/15307823.jpg'
#url = 'http://ak1.polyvoreimg.com/cgi/img-thing/size/orig/tid/64279101.jpg'
#url = 'http://ak2.polyvoreimg.com/cgi/img-thing/size/l/tid/92202643.jpg'
image = Image.open(StringIO(urlopen(url).read()))
print image
print get_colors(image)
