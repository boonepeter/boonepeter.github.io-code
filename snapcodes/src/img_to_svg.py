import argparse
from img_to_points import img_to_points
from points_to_svg import points_to_svg

def img_to_svg(filepath, output_filepath):
    """
    Converts an image to an SVG file.
    """
    points = img_to_points(filepath, True)
    print(points)
    svg = points_to_svg(points)
    with open(output_filepath, "w") as f:
        f.write(svg)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an image to an SVG file.")
    parser.add_argument("-i", "--input", help="Input filepath", required=True)
    parser.add_argument("-o", "--output", help="Output filepath", required=True)
    args = parser.parse_args()
    img_to_svg(args.input, args.output)