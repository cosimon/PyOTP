#!/usr/bin/env python3

import sys

from image import png

if len(sys.argv) != 2:
    print("ERROR: No filename provided!")
    sys.exit(1)

image = png.parse(sys.argv[1])

print(image)

for i in image.chunks:
    print(i)

image.write_to_file("output.png")
