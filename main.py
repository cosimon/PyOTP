#!/usr/bin/env python3

import sys
from os import urandom
from image import png

def main():
	if len(sys.argv) != 2:
		print("ERROR: No filename provided!")
		sys.exit(1)

	image = png.parse(sys.argv[1])

	print(image)

	pad = bytearray()

	for i in image.chunks:
		if i.type() == 'IDAT':
			pad += bytearray(urandom(len(i.data)))

	position = 0

	if image.colortype != 2:
		scanlineLength = image.width + 1
	else:
		scanlineLength = image.width * 3 + 1

	for i in image.chunks:
		if i.type() == 'IDAT':
			for j in range(len(i.data)):
				if position % scanlineLength != 0:
					i.data[j] ^= pad[position]
				position += 1



	image.write_to_file("output.png")

	f = open('pad.txt', 'wb')
	f.write(pad)
	f.close()


if __name__ == "__main__":
	main()
