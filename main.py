#!/usr/bin/env python3

import sys
from os import urandom
from image import png

def encrypt():
	if len(sys.argv) != 5:
		print("USAGE: python3 main.py encrypt <input_image> <output_image> <pad_output>")
		sys.exit(1)

	image = png.parse(sys.argv[2])

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



	image.write_to_file(sys.argv[3])

	f = open(sys.argv[4], 'wb')
	f.write(pad)
	f.close()

def decrypt():
	if len(sys.argv) != 5:
		print("USAGE: python3 main.py decrypt <input_image> <output_image> <pad_input>")
		sys.exit(1)

	image = png.parse(sys.argv[2])

	print(image)

	pad = bytearray(open(sys.argv[4], 'rb').read())

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



	image.write_to_file(sys.argv[3])

if __name__ == "__main__":
	if sys.argv[1] == 'encrypt':
		encrypt()
	elif sys.argv[1] == 'decrypt':
		decrypt()
	else:
		print("USAGE: python3 main.py <encrypt/decrypt> <additional arguments....>")
