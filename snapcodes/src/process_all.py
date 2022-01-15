import os

from img_to_svg import img_to_svg


files = os.listdir("./imgs/twitter")
files = [os.path.join("./imgs/twitter", f) for f in files if f.endswith(".jpeg")]

for f in files:
    output_path = f.replace(".jpeg", ".svg")
    try:
        img_to_svg(f, output_path)
    except Exception as e:
        print(f"Error processing {f}")
        print(e)