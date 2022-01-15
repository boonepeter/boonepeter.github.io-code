import argparse

positions = [
     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
  [0, 1, 2, 3, 4, 5,                         13, 14, 15, 16, 17, 18],
  [0, 1, 2, 3, 4,                                14, 15, 16, 17, 18],
  [0, 1, 2, 3,                                       15, 16, 17, 18],
  [0, 1, 2,                                              16, 17, 18],
  [0, 1, 2,                                              16, 17, 18],
  [0, 1, 2,                                              16, 17, 18],
  [0, 1, 2,                                              16, 17, 18],
  [0, 1, 2,                                              16, 17, 18],
  [0, 1, 2,                                              16, 17, 18],
  [0, 1, 2,                                              16, 17, 18],
  [0, 1, 2, 3,                                       15, 16, 17, 18],
  [0, 1, 2, 3, 4,                                14, 15, 16, 17, 18],
  [0, 1, 2, 3, 4, 5,                         13, 14, 15, 16, 17, 18],
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
]

BORDER = 56.42
BORDER_C = 72.42
MULT = 48.8425
DIAMETER = 32
SVG = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:xlink="http://www.w3.org/1999/xlink" height="1024" version="1.1" viewBox="0 0 1024 1024" width="1024" xmlns="http://www.w3.org/2000/svg">
  <path d=" M749.88,641.75 C763.31,649.46,754.85,644.24,749.88,641.75 M0,860.16 C0,950.64,73.36,1024,163.84,1024 L860.16,1024 C950.64,1024,1024,950.64,1024,860.16 L1024,163.84 C1024,73.36,950.64,0,860.16,0 L163.84,0 C73.36,0,0,73.36,0,163.84 L0,860.16" fill="#000" fill-rule="evenodd"/>
     <path d="M32,163.84 C32,91.03,91.03,32,163.84,32 L860.16,32 C932.97,32,992,91.03,992,163.84 L992,860.16 C992,932.97,932.97,992,860.16,992 L163.84,992 C91.03,992,32,932.97,32,860.16 L32,163.84
    {path}" fill="#FFFC00"/>
</svg>
'''

def points_to_svg(points):
    counter = 0
    path = ""
    points.sort()
    for r in range(len(positions)):
        for c in range(len(positions[r])):
            col = positions[r][c]
            if len(points) == 0:
                break
            if points[0] == counter:
                path += f"""M{col * MULT + BORDER_C},{r * MULT + BORDER}
    A16,16,0,0,0,{col * MULT + BORDER_C},{r * MULT + BORDER + DIAMETER}
    A16,16,0,0,0,{col * MULT + BORDER_C},{r * MULT + BORDER}
    """
                points.pop(0)
            counter += 1
    return SVG.format(path=path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--points", type=str, help="Points to draw")
    parser.add_argument("--output", type=str, help="Output file")
    parser.add_argument("--show", action="store_true", help="Show SVG")
    parser.set_defaults(points=",".join([str(i) for i in range(212)]))
    args = parser.parse_args()
    points = args.points.split(",")
    points = [int(i) for i in points]
    svg = points_to_svg(points)
    if args.output:
        with open(args.output, "w") as f:
            f.write(svg)
        if args.show:
            import subprocess, os, platform
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', args.output))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(args.output)
            else:                                   # linux variants
                subprocess.call(('xdg-open', args.output))
    if not args.show or not args.output:
        print(svg)
