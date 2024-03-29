import argparse
from skimage import io
import numpy as np
from skimage import io, img_as_ubyte
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray, rgba2rgb
from skimage.measure import label, regionprops

## BBOX of points from all_dots_yellow.png
ALL_BBOX = [
  [0.025, 0.076, 0.0583, 0.1094],
  [0.025, 0.1271, 0.0583, 0.1604],
  [0.025, 0.1781, 0.0583, 0.2115],
  [0.025, 0.2292, 0.0583, 0.2625],
  [0.025, 0.2802, 0.0583, 0.3135],
  [0.025, 0.3302, 0.0583, 0.3635],
  [0.025, 0.3812, 0.0583, 0.4146],
  [0.025, 0.4323, 0.0583, 0.4656],
  [0.025, 0.4833, 0.0583, 0.5167],
  [0.025, 0.5344, 0.0583, 0.5677],
  [0.025, 0.5854, 0.0583, 0.6188],
  [0.025, 0.6365, 0.0583, 0.6698],
  [0.025, 0.6865, 0.0583, 0.7198],
  [0.025, 0.7375, 0.0583, 0.7708],
  [0.025, 0.7885, 0.0583, 0.8219],
  [0.025, 0.8396, 0.0583, 0.8729],
  [0.025, 0.8906, 0.0583, 0.924],
  [0.076, 0.025, 0.1094, 0.0583],
  [0.076, 0.076, 0.1094, 0.1094],
  [0.076, 0.1271, 0.1094, 0.1604],
  [0.076, 0.1781, 0.1094, 0.2115],
  [0.076, 0.2292, 0.1094, 0.2625],
  [0.076, 0.2802, 0.1094, 0.3135],
  [0.076, 0.3302, 0.1094, 0.3635],
  [0.076, 0.3812, 0.1094, 0.4146],
  [0.076, 0.4323, 0.1094, 0.4656],
  [0.076, 0.4833, 0.1094, 0.5167],
  [0.076, 0.5344, 0.1094, 0.5677],
  [0.076, 0.5854, 0.1094, 0.6188],
  [0.076, 0.6365, 0.1094, 0.6698],
  [0.076, 0.6865, 0.1094, 0.7198],
  [0.076, 0.7375, 0.1094, 0.7708],
  [0.076, 0.7885, 0.1094, 0.8219],
  [0.076, 0.8396, 0.1094, 0.8729],
  [0.076, 0.8906, 0.1094, 0.924],
  [0.076, 0.9417, 0.1094, 0.975],
  [0.1271, 0.025, 0.1604, 0.0583],
  [0.1271, 0.076, 0.1604, 0.1094],
  [0.1271, 0.1271, 0.1604, 0.1604],
  [0.1271, 0.1781, 0.1604, 0.2115],
  [0.1271, 0.2292, 0.1604, 0.2625],
  [0.1271, 0.2802, 0.1604, 0.3135],
  [0.1271, 0.3312, 0.1604, 0.3635],
  [0.1271, 0.3812, 0.1604, 0.4146],
  [0.1271, 0.4323, 0.1604, 0.4656],
  [0.1271, 0.4833, 0.1604, 0.5167],
  [0.1271, 0.5344, 0.1604, 0.5677],
  [0.1271, 0.5854, 0.1604, 0.6188],
  [0.1271, 0.6365, 0.1604, 0.6698],
  [0.1271, 0.6865, 0.1604, 0.7198],
  [0.1271, 0.7375, 0.1604, 0.7708],
  [0.1271, 0.7885, 0.1604, 0.8219],
  [0.1271, 0.8396, 0.1604, 0.8729],
  [0.1271, 0.8906, 0.1604, 0.924],
  [0.1271, 0.9417, 0.1604, 0.975],
  [0.1781, 0.025, 0.2115, 0.0583],
  [0.1781, 0.076, 0.2115, 0.1094],
  [0.1781, 0.1271, 0.2115, 0.1604],
  [0.1781, 0.1781, 0.2115, 0.2115],
  [0.1781, 0.2292, 0.2115, 0.2625],
  [0.1781, 0.2802, 0.2115, 0.3135],
  [0.1781, 0.6865, 0.2115, 0.7198],
  [0.1781, 0.7375, 0.2115, 0.7708],
  [0.1781, 0.7885, 0.2115, 0.8219],
  [0.1781, 0.8396, 0.2115, 0.8729],
  [0.1781, 0.8906, 0.2115, 0.924],
  [0.1781, 0.9417, 0.2115, 0.975],
  [0.2292, 0.025, 0.2625, 0.0583],
  [0.2292, 0.076, 0.2625, 0.1094],
  [0.2292, 0.1271, 0.2625, 0.1604],
  [0.2292, 0.1781, 0.2625, 0.2115],
  [0.2292, 0.2292, 0.2625, 0.2625],
  [0.2292, 0.7375, 0.2625, 0.7708],
  [0.2292, 0.7885, 0.2625, 0.8219],
  [0.2292, 0.8396, 0.2625, 0.8729],
  [0.2292, 0.8906, 0.2625, 0.924],
  [0.2292, 0.9417, 0.2625, 0.975],
  [0.2802, 0.025, 0.3135, 0.0583],
  [0.2802, 0.076, 0.3135, 0.1094],
  [0.2802, 0.1271, 0.3135, 0.1604],
  [0.2802, 0.1781, 0.3135, 0.2115],
  [0.2802, 0.7885, 0.3135, 0.8219],
  [0.2802, 0.8396, 0.3135, 0.8729],
  [0.2802, 0.8906, 0.3135, 0.924],
  [0.2802, 0.9417, 0.3135, 0.975],
  [0.3302, 0.025, 0.3635, 0.0583],
  [0.3302, 0.076, 0.3635, 0.1094],
  [0.3302, 0.1271, 0.3635, 0.1604],
  [0.3302, 0.8396, 0.3635, 0.8729],
  [0.3302, 0.8906, 0.3635, 0.924],
  [0.3302, 0.9417, 0.3635, 0.975],
  [0.3812, 0.025, 0.4146, 0.0583],
  [0.3812, 0.076, 0.4146, 0.1094],
  [0.3812, 0.1271, 0.4146, 0.1604],
  [0.3812, 0.8396, 0.4146, 0.8729],
  [0.3812, 0.8906, 0.4146, 0.924],
  [0.3812, 0.9417, 0.4146, 0.975],
  [0.4323, 0.025, 0.4656, 0.0583],
  [0.4323, 0.076, 0.4656, 0.1094],
  [0.4323, 0.1271, 0.4656, 0.1604],
  [0.4323, 0.8396, 0.4656, 0.8729],
  [0.4323, 0.8906, 0.4656, 0.924],
  [0.4323, 0.9417, 0.4656, 0.975],
  [0.4833, 0.025, 0.5167, 0.0583],
  [0.4833, 0.076, 0.5167, 0.1094],
  [0.4833, 0.1271, 0.5167, 0.1604],
  [0.4833, 0.8396, 0.5167, 0.8729],
  [0.4833, 0.8906, 0.5167, 0.924],
  [0.4833, 0.9417, 0.5167, 0.975],
  [0.5344, 0.025, 0.5677, 0.0583],
  [0.5344, 0.076, 0.5677, 0.1094],
  [0.5344, 0.1271, 0.5677, 0.1604],
  [0.5344, 0.8396, 0.5677, 0.8729],
  [0.5344, 0.8906, 0.5677, 0.924],
  [0.5344, 0.9417, 0.5677, 0.975],
  [0.5854, 0.025, 0.6188, 0.0583],
  [0.5854, 0.076, 0.6188, 0.1094],
  [0.5854, 0.1271, 0.6188, 0.1604],
  [0.5854, 0.8396, 0.6188, 0.8729],
  [0.5854, 0.8906, 0.6188, 0.924],
  [0.5854, 0.9417, 0.6188, 0.975],
  [0.6365, 0.025, 0.6698, 0.0583],
  [0.6365, 0.076, 0.6698, 0.1094],
  [0.6365, 0.1271, 0.6698, 0.1604],
  [0.6365, 0.8396, 0.6698, 0.8729],
  [0.6365, 0.8906, 0.6698, 0.924],
  [0.6365, 0.9417, 0.6698, 0.975],
  [0.6865, 0.025, 0.7198, 0.0583],
  [0.6865, 0.076, 0.7198, 0.1094],
  [0.6865, 0.1271, 0.7198, 0.1604],
  [0.6865, 0.1781, 0.7198, 0.2115],
  [0.6865, 0.7885, 0.7198, 0.8219],
  [0.6865, 0.8396, 0.7198, 0.8729],
  [0.6865, 0.8906, 0.7198, 0.924],
  [0.6865, 0.9417, 0.7198, 0.975],
  [0.7375, 0.025, 0.7708, 0.0583],
  [0.7375, 0.076, 0.7708, 0.1094],
  [0.7375, 0.1271, 0.7708, 0.1604],
  [0.7375, 0.1781, 0.7708, 0.2115],
  [0.7375, 0.2292, 0.7708, 0.2625],
  [0.7375, 0.7375, 0.7708, 0.7708],
  [0.7375, 0.7885, 0.7708, 0.8219],
  [0.7375, 0.8396, 0.7708, 0.8729],
  [0.7375, 0.8906, 0.7708, 0.924],
  [0.7375, 0.9417, 0.7708, 0.975],
  [0.7885, 0.025, 0.8219, 0.0583],
  [0.7885, 0.076, 0.8219, 0.1094],
  [0.7885, 0.1271, 0.8219, 0.1604],
  [0.7885, 0.1781, 0.8219, 0.2115],
  [0.7885, 0.2292, 0.8219, 0.2625],
  [0.7885, 0.2802, 0.8219, 0.3135],
  [0.7885, 0.6865, 0.8219, 0.7198],
  [0.7885, 0.7375, 0.8219, 0.7708],
  [0.7885, 0.7885, 0.8219, 0.8219],
  [0.7885, 0.8396, 0.8219, 0.8729],
  [0.7885, 0.8906, 0.8219, 0.924],
  [0.7885, 0.9417, 0.8219, 0.975],
  [0.8396, 0.025, 0.8729, 0.0583],
  [0.8396, 0.076, 0.8729, 0.1094],
  [0.8396, 0.1271, 0.8729, 0.1604],
  [0.8396, 0.1781, 0.8729, 0.2115],
  [0.8396, 0.2292, 0.8729, 0.2625],
  [0.8396, 0.2802, 0.8729, 0.3135],
  [0.8396, 0.3312, 0.8729, 0.3635],
  [0.8396, 0.3812, 0.8729, 0.4146],
  [0.8396, 0.4323, 0.8729, 0.4656],
  [0.8396, 0.4833, 0.8729, 0.5167],
  [0.8396, 0.5344, 0.8729, 0.5677],
  [0.8396, 0.5854, 0.8729, 0.6188],
  [0.8396, 0.6365, 0.8729, 0.6698],
  [0.8396, 0.6865, 0.8729, 0.7198],
  [0.8396, 0.7375, 0.8729, 0.7708],
  [0.8396, 0.7885, 0.8729, 0.8219],
  [0.8396, 0.8396, 0.8729, 0.8729],
  [0.8396, 0.8906, 0.8729, 0.924],
  [0.8396, 0.9417, 0.8729, 0.975],
  [0.8906, 0.025, 0.924, 0.0583],
  [0.8906, 0.076, 0.924, 0.1094],
  [0.8906, 0.1271, 0.924, 0.1604],
  [0.8906, 0.1781, 0.924, 0.2115],
  [0.8906, 0.2292, 0.924, 0.2625],
  [0.8906, 0.2802, 0.924, 0.3135],
  [0.8906, 0.3302, 0.924, 0.3635],
  [0.8906, 0.3812, 0.924, 0.4146],
  [0.8906, 0.4323, 0.924, 0.4656],
  [0.8906, 0.4833, 0.924, 0.5167],
  [0.8906, 0.5344, 0.924, 0.5677],
  [0.8906, 0.5854, 0.924, 0.6188],
  [0.8906, 0.6365, 0.924, 0.6698],
  [0.8906, 0.6865, 0.924, 0.7198],
  [0.8906, 0.7375, 0.924, 0.7708],
  [0.8906, 0.7885, 0.924, 0.8219],
  [0.8906, 0.8396, 0.924, 0.8729],
  [0.8906, 0.8906, 0.924, 0.924],
  [0.8906, 0.9417, 0.924, 0.975],
  [0.9417, 0.076, 0.975, 0.1094],
  [0.9417, 0.1271, 0.975, 0.1604],
  [0.9417, 0.1781, 0.975, 0.2115],
  [0.9417, 0.2292, 0.975, 0.2625],
  [0.9417, 0.2802, 0.975, 0.3135],
  [0.9417, 0.3302, 0.975, 0.3635],
  [0.9417, 0.3812, 0.975, 0.4146],
  [0.9417, 0.4323, 0.975, 0.4656],
  [0.9417, 0.4833, 0.975, 0.5167],
  [0.9417, 0.5344, 0.975, 0.5677],
  [0.9417, 0.5854, 0.975, 0.6188],
  [0.9417, 0.6365, 0.975, 0.6698],
  [0.9417, 0.6865, 0.975, 0.7198],
  [0.9417, 0.7375, 0.975, 0.7708],
  [0.9417, 0.7885, 0.975, 0.8219],
  [0.9417, 0.8396, 0.975, 0.8729],
  [0.9417, 0.8906, 0.975, 0.924],
]

def color_crop(im, color=[(250, 255), (245, 255), (0, 10)]):
    """Crop an image to the min and max occurances of a color range.
    Accepts an image and list of colors (channels and colors must match).
    """
    assert len(color) == im.shape[-1]
    binary = np.ones(im.shape[:-1], dtype=bool)
    for i in range(3):
        binary &= (im[:,:,i] >= color[i][0]) & (im[:,:,i] <= color[i][1])
    labeled = label(binary, background=0)
    rp = regionprops(labeled)
    bbox = max(rp, key=lambda x: x.bbox_area).bbox
    return im[bbox[0]:bbox[2], bbox[1]:bbox[3], :]

def _get_points(image):
    im = rgb2gray(image)
    t = threshold_otsu(im)
    return im > t


def get_bbox_and_centers(im, color=[(250, 255), (245, 255), (0, 10)]):
    im = color_crop(im, color=color)
    p = _get_points(im)
    l = label(p, background=1)
    rp = regionprops(l)
    (maxx, maxy) = l.shape
    max_size = l.shape[0] * l.shape[1] // 500
    min_size = l.shape[0] * l.shape[1] // 2000

    bbs = []
    centers = []
    for props in rp:
        minr, minc, maxr, maxc = props.bbox
        if props.bbox_area < max_size and props.bbox_area > min_size:
            bbs.append((props.bbox[0] / maxx, props.bbox[1] / maxx, props.bbox[2] / maxx, props.bbox[3] / maxx))
            centers.append(
                (
                    (((minr / maxy) + (maxr / maxy)) / 2), 
                    (((minc / maxx) + (maxc / maxx)) / 2)
                ),
            )
    return bbs, centers

def get_numbers(centers, bbs):
    points = []
    for i, b in enumerate(bbs):
        for x, y in centers:
            if x > b[0] and x < b[2] and y > b[1] and y < b[3]:
                points.append(i)
    return points

def img_to_points(filepath, check_counts=False):
    im = io.imread(filepath)
    color = [(250, 255), (245, 255), (0, 10)]
    # convert to 3 channel
    if im.shape[-1] == 4:
        im = rgba2rgb(im)
    # convert to uint8 (0-255)
    im = img_as_ubyte(im)
    try:
        _, centers = get_bbox_and_centers(im, color)
    except:
        try:
            # for some reason, some of the colors are off
            # when the images are read in
            color = [(250, 255), (245, 255), (75, 90)]
            _, centers = get_bbox_and_centers(im, color)
        except Exception as e:
            raise e
    if check_counts and (len(centers) < 50 or len(centers) > 120):
        raise Exception("Too many or too few points")
    return get_numbers(centers, ALL_BBOX)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str)
    parser.add_argument("--check_counts", action="store_true")
    args = parser.parse_args()
    print(img_to_points(args.filepath, args.check_counts))


