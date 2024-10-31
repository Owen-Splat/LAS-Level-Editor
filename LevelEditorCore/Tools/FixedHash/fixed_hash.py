import numpy as np
import struct

def readBytes(bytes, start, length, endianness='little'):
	return int.from_bytes(bytes[start : start + length], endianness)

def readFloat(bytes, start):
	return np.float32(struct.unpack('<f', bytes[start : start+4])[0])

def readString(data, start):
	result = b''
	index = start
	while index < len(data) and data[index]:
		result += data[index : index + 1]
		index += 1
	return result

def hash_string(s):
    data = s + b"\x00"
    h = 0
    i = 0
    while data[i]:
        h ^= (data[i] + (h >> 2) + (h << 5)) & 0xFFFFFFFF
        i += 1
    return h

def readVector3(data, start):
	x = readFloat(data, start)
	y = readFloat(data, start+4)
	z = readFloat(data, start+8)
	return Vector3(x, y, z)


class Vector3:
    def __init__(self, x: np.float32, y: np.float32, z: np.float32) -> None:
        self.x = x
        self.y = y
        self.z = z


class Entry:
	def __init__(self, node_index, name, next_offset, data):
		self.node_index = node_index
		self.name = name
		self.next_offset = next_offset
		self.data = data


class FixedHash:
	def __init__(self, data, offset=0):
		self.magic = readBytes(data, offset + 0x0, 1)
		self.version = readBytes(data, offset + 0x1, 1)
		self.num_buckets = readBytes(data, offset + 0x2, 2)
		self.num_nodes = readBytes(data, offset + 0x4, 2)
		self.x6 = readBytes(data, offset + 0x6, 2)

		self.buckets = []
		for i in range(self.num_buckets): # there will be an extra one. I don't really know what this data means but we want to preserve it
			self.buckets.append(readBytes(data, offset + 0x8 + (i * 4), 4))

		entries_offset = ((offset + 0x8 + 4*(self.num_buckets+1) + 3) & -8) + 8
		num_entries = readBytes(data, entries_offset - 8, 8) // 0x10

		entry_offsets_offset = entries_offset + (num_entries * 0x10) + 8

		data_section_offset = ((entry_offsets_offset + (4 * num_entries) + 7) & -8) + 8

		names_section_offset = ((data_section_offset + readBytes(data, data_section_offset - 8, 8) + 3) & -4) + 4
		names_size = readBytes(data, names_section_offset - 4, 4)
		self.names_section = data[names_section_offset : names_section_offset + names_size]

		self.entries = []
		for i in range(num_entries):
			current_offset = entries_offset + (i * 0x10)
			
			node_index = readBytes(data, current_offset, 2)
			
			next_offset = readBytes(data, current_offset + 8, 4)
			
			if names_size:
				name = readString(data, names_section_offset + readBytes(data, current_offset + 2, 2))
			else:
				name = b''

			entry_data_offset = readBytes(data, current_offset + 0xC, 4)
			
			if node_index <= 0xFFED:
				entry_data = FixedHash(data, data_section_offset + entry_data_offset)
				#print(data[dataSectionOffset + entryDataOffset : dataSectionOffset + entryDataOffset + 32])
				pass
			elif node_index >= 0xFFF0:
				data_size = readBytes(data, data_section_offset + entry_data_offset, 8)
				
				entry_data = data[data_section_offset + entry_data_offset + 8 : data_section_offset + entry_data_offset + 8 + data_size]
			else:
				raise ValueError('Invalid node index')

			self.entries.append(Entry(node_index, name, next_offset, entry_data))


	def toBinary(self, offset=0):
		# Returns a bytes object of the fixed hash in binary form
		intro = b''

		intro += self.magic.to_bytes(1, 'little')
		intro += self.version.to_bytes(1, 'little')
		intro += self.num_buckets.to_bytes(2, 'little')
		intro += self.num_nodes.to_bytes(2, 'little')
		intro += self.x6.to_bytes(2, 'little')

		for bucket in self.buckets:
			intro += bucket.to_bytes(4, 'little')

		entries_sect = (len(self.entries) * 0x10).to_bytes(8, 'little')
		entry_offsets_sect = (len(self.entries) * 0x4).to_bytes(8, 'little')
		data_sect = b''
		
		for i in range(len(self.entries)):
			entry = self.entries[i]

			entries_sect += entry.node_index.to_bytes(2, 'little')
			if self.names_section.count(entry.name) and self.names_section != b'':
				entries_sect += self.names_section.index(entry.name + b'\x00').to_bytes(2, 'little')
			else:
				entries_sect += b'\x00\x00'
			entries_sect += hash_string(entry.name).to_bytes(4, 'little')
			entries_sect += entry.next_offset.to_bytes(4, 'little')
			entries_sect += len(data_sect).to_bytes(4, 'little')
			
			entry_offsets_sect += (i * 0x10).to_bytes(4, 'little')

			if entry.node_index <= 0xFFED:
				data_sect += entry.data.toBinary(len(data_sect))
			elif entry.node_index >= 0xFFF0:
				data_sect += len(entry.data).to_bytes(8, 'little') + entry.data

				data_sect += b'\x00\x00\x00\x00\x00\x00\x00'
				data_sect = data_sect[:len(data_sect) & -8]
			else:
				raise ValueError('Invalid node index')

		data_sect = len(data_sect).to_bytes(8, 'little') + data_sect

		result = b''
		result += intro

		while (len(result) + offset) % 8 != 0:
			result += b'\x00'
		result += entries_sect

		while (len(result) + offset) % 8 != 0:
			result += b'\x00'
		result += entry_offsets_sect

		while (len(result) + offset) % 8 != 0:
			result += b'\x00'
		result += data_sect

		while (len(result) + offset) % 4 != 0:
			result += b'\x00'
		result += len(self.names_section).to_bytes(4, 'little')
		result += self.names_section

		return result
