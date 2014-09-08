from scipy import ndimage
import numpy as np
from PIL import Image
from StringIO import StringIO
from urllib2 import urlopen
import scipy
from pprint import pprint


url = 'http://ak1.polyvoreimg.com/cgi/img-thing/size/l/tid/91442647.jpg'
image = Image.open(StringIO(urlopen(url).read()))
ar = scipy.misc.fromimage(image)
shape = ar.shape
ar = ar.reshape(scipy.product(shape[:2]), shape[2])
ar = ndimage.gaussian_filter(ar, sigma=256/(4.*10))
mask = (ar > ar.mean()).astype(np.float)
print mask
binary_img = mask > 0.5

scipy.misc.imsave('outfile.png', binary_img.reshape(shape))