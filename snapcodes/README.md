# Snapcodes

Using Python 3.10.1

```bash
pip3 install -r requirements.txt
```

Running this command

```bash
python3 img_to_points.py snapcode.png
```

Gets the points from this image:

![](./src/snapcode.png)

Points:

```python
[1, 2, 3, 4, 6, 9, 14, 18, 20, 21, 22, 23, 27, 28, 29, 30, 32, 38, 39, 41, 43, 44, 45, 49, 53, 58, 59, 62, 64, 65, 66, 67, 70, 71, 73, 76, 77, 83, 87, 90, 93, 94, 96, 99, 100, 101, 103, 104, 105, 106, 107, 108, 109, 110, 112, 113, 115, 118, 119, 120, 130, 131, 134, 140, 141, 144, 145, 146, 150, 153, 155, 157, 159, 161, 163, 169, 170, 171, 172, 173, 174, 175, 178, 182, 183, 184, 185, 188, 190, 192, 193, 196, 197, 202, 204, 206, 207, 209]
```

Points are numbered left to right, top to bottom, starting with 0 and ending at 211.

And this command

```bash
python3 img_to_svg.py -i snapcode.png -o output.svg
```

Outputs an SVG file:

![](./src/output.svg)

The svg is useful for checking that the point parsing was correct.
