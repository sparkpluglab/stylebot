from PIL import Image
import scipy
import scipy.cluster
import scipy.misc
from pprint import pprint
from StringIO import StringIO
from urllib2 import urlopen

def get_colors(image, NUM_CLUSTERS):
    # Convert image into array of values for each point
    ar = scipy.misc.fromimage(image)
    shape = ar.shape
    print shape
    # Reshape array of values to merge color bands.
    if len(shape) > 2:
        ar = ar.reshape(scipy.product(shape[:2]), shape[2])
    print ar
    print ar.shape
    # Get NUM_CLUSTERS worth of centroids.
    codes, _ = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    # Pare centroids, removing blacks and whites and shades of really 
    # dark and really light.
    original_codes = codes
    for low, hi in [(60, 200), (35, 230), (10, 250)]:
        codes = scipy.array([code for code in codes 
                             if not ((code[0] < low and code[1] < low and code[2] < low) or
                                     (code[0] > hi and code[1] > hi and code[2] > hi))])
        if not len(codes): codes = original_codes
        else: break

    # Assign codes (vector quantization). Each vector is compared to the centroids
    # and assigned the nearest one.
    vecs, _ = scipy.cluster.vq.vq(ar, codes)

    # Count occurences of each clustered vector.
    counts, bins = scipy.histogram(vecs, len(codes))

    # Show colors for each code in its hex value.
    for code in codes:
        print code
    colors = [''.join(chr(c) for c in code).encode('hex') for code in codes]
    #colors = [ list(code / 255.0) for code in codes]
    print colors
    total = scipy.sum(counts)
    color_dist = (zip(colors, [count / float(total) for count in counts]))
    pprint(color_dist)

    # Find the most frequent color, based on the counts.
    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    color = ''.join(chr(c) for c in peak).encode('hex')
    pprint(color)


# test the module
url = 'http://ak1.polyvoreimg.com/cgi/img-thing/size/l/tid/92872867.jpg'
image = Image.open(StringIO(urlopen(url).read()))
NUM_CLUSTERS = 5
get_colors(image, NUM_CLUSTERS)
