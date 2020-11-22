from skimage import io
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray


def get_heights(filename: str) -> list:
    """Open an image and return a list of the bar heights.
    """
    # convert to grayscale, then binary
    image = io.imread(filename)
    im = rgb2gray(image)
    binary_im = im > threshold_otsu(im)

    # label connected regions as objects
    labeled = label(binary_im)

    # get the dimensions and positions of bounding box around objects
    bar_dimensions = [r.bbox for r in regionprops(labeled)]

    # sort by X
    bar_dimensions.sort(key=lambda x: x[1], reverse=False)

    # the first object (spotify logo) is the max height of the bars
    logo = bar_dimensions[0]
    max_height = logo[2] - logo[0]
    sequence = []
    for bar in bar_dimensions[1:]:
        height = bar[2] - bar[0]
        ratio = height / max_height
        # multiply by 8 to get an octal integer
        ratio *= 8
        ratio //= 1
        # convert to integer (and make 0 based)
        sequence.append(int(ratio - 1))
    return sequence