import struct
import sys
import zlib

PNG_MAGIC = bytearray.fromhex("89 50 4E 47 0D 0A 1A 0A")

class PNGImage:
	def __init__(self):
		self.name = ""
		self.chunks = []
		self.width = 0
		self.height = 0
		self.bitdepth = 0
		self.colortype = 0
		self.compression = 0
		self.filtering = 0
		self.interlacing = 0

	def resolution(self):
		return str(self.width) + "x" + str(self.height)

	def __str__(self):
		s  = "{\n"
		s += "\tResolution: " + self.resolution() + ",\n"
		s += "\tBit Depth: " + str(self.bitdepth) + ",\n"
		s += "\tColor Type: " + str(self.colortype) + ",\n"
		s += "\tCompression: " + str(self.compression) + ",\n"
		s += "\tFilter: " + str(self.filtering) + ",\n"
		s += "\tInterlace: " + str(self.interlacing) + "\n"
		s += "}"
		return s

	def _compress(self):
		for i in self.chunks:
			if i.type() == "IDAT":
				print('BEFORE:\t' + str(len(i.data)))
				i.data = zlib.compress(i.data, 9)
				print('AFTER:\t' + str(len(i.data)))
				i.length = struct.pack("!I", len(i.data))
				i.crc = zlib.crc32(i.chunk_type + i.data)
				i.crc = struct.pack("!I", i.crc)

	def _decompress(self):
		for i in self.chunks:
			if i.type() == "IDAT":
				i.data = bytearray(zlib.decompress(i.data))

	def write_to_file(self, filename):
		self._compress()
		with open(filename, "wb") as f:
			f.write(PNG_MAGIC)
			for i in self.chunks:
				f.write(i.length)
				f.write(i.chunk_type)
				f.write(i.data)
				f.write(i.crc)

class Chunk:
	def __init__(self):
		self.length = bytearray()
		self.chunk_type = bytearray()
		self.data = bytearray()
		self.crc = bytearray()

	def __str__(self):
		return "{Type: " + self.type() + ", Length: " + str(self.size()) + "}"

	def size(self):
		return int.from_bytes(self.length, byteorder="big")

	def checksum(self):
		return int.from_bytes(self.crc, byteorder="big")

	def type(self):
		return self.chunk_type.decode()

def parse(filename):
	with open(filename, "rb") as f:
		header = f.read(len(PNG_MAGIC))
		if header != PNG_MAGIC:
			print("ERROR: File is not a PNG file: " + filename)
			sys.exit(1)

		image = PNGImage()
		image.name = filename

		while True:
			chunk = Chunk()
			chunk.length = f.read(4)
			chunk.chunk_type = f.read(4)
			chunk.data = f.read(int.from_bytes(chunk.length, byteorder="big"))
			chunk.crc = f.read(4)
			image.chunks.append(chunk)
			if chunk.type() == "IHDR":
				_parse_ihdr(image, chunk)
			if chunk.type() == "IEND":
				image._decompress()
				return image

def _parse_ihdr(image, chunk):
	image.width = int.from_bytes(chunk.data[0:4], byteorder="big")
	image.height = int.from_bytes(chunk.data[4:8], byteorder="big")
	image.bitdepth = int.from_bytes(chunk.data[8:9], byteorder="big")
	image.colortype = int.from_bytes(chunk.data[9:10], byteorder="big")
	image.compression = int.from_bytes(chunk.data[10:11], byteorder="big")
	image.filtering = int.from_bytes(chunk.data[11:12], byteorder="big")
	image.interlacing = int.from_bytes(chunk.data[12:13], byteorder="big")
