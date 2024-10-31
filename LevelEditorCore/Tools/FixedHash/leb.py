from LevelEditorCore.Tools.FixedHash.fixed_hash import *
import numpy as np
import struct


class Actor:
	def __init__(self, data, names):
		# self.names = names
		self.visible = True # for the UI
		self.key = readBytes(data, 0x0, 8)
		# self.name = readString(names, readBytes(data, 0x8, 4))
		self.type = readBytes(data, 0xC, 2)
		# self.xE = readBytes(data, 0xE, 2) # print this out to view it, we might not need to read it
		self.roomID = readBytes(data, 0x10, 4)

		self.position = readVector3(data, 0x14)
		self.rotation = readVector3(data, 0x20)
		self.scale = readVector3(data, 0x2C)

		self.parameters = []
		for i in range(8):
			param_type = readBytes(data, 0x38 + (0x8 * i) + 0x4, 4)

			if param_type == 0x2:
				param = readFloat(data, 0x38 + (0x8 * i))
			else:
				param = readBytes(data, 0x38 + (0x8 * i), 4)
			
			if param_type == 0x4:
				self.parameters.append(readString(names, param))
			else:
				self.parameters.append(param)

		self.switches = [
			(readBytes(data, 0x78, 1), readBytes(data, 0x7C, 2)),
			(readBytes(data, 0x79, 1), readBytes(data, 0x7E, 2)),
			(readBytes(data, 0x7A, 1), readBytes(data, 0x80, 2)),
			(readBytes(data, 0x7B, 1), readBytes(data, 0x82, 2))
		]

		self.relationships = Relationship(data, names)

	def pack(self, name_offset):
		packed = b''

		# only the hex part of the name matters, so we can change the first half to a basic "Actor" to trim down file size a little
		id_hex = hex(self.key).split('0x')[1].upper()
		while len(id_hex) != 16:
			id_hex = "0" + id_hex
		self.name = bytes(f"Actor-{id_hex}", 'utf-8')
		name_repr = self.name + b'\x00'

		packed += self.key.to_bytes(8, 'little')
		packed += name_offset.to_bytes(4, 'little')
		packed += self.type.to_bytes(2, 'little')
		packed += (0).to_bytes(2, 'little') # 0xE padding
		packed += self.roomID.to_bytes(4, 'little')
		packed += struct.pack('<f', self.position.x)
		packed += struct.pack('<f', self.position.y)
		packed += struct.pack('<f', self.position.z)
		packed += struct.pack('<f', self.rotation.x)
		packed += struct.pack('<f', self.rotation.y)
		packed += struct.pack('<f', self.rotation.z)
		packed += struct.pack('<f', self.scale.x)
		packed += struct.pack('<f', self.scale.y)
		packed += struct.pack('<f', self.scale.z)

		for i in range(8):
			param = self.parameters[i]
			if isinstance(param, bytes):
				packed += (len(name_repr) + name_offset).to_bytes(4, 'little')
				packed += (4).to_bytes(4, 'little')
				name_repr += param + b'\x00'
			elif isinstance(param, np.float32):
				packed += struct.pack('<f', param)
				packed += (2).to_bytes(4, 'little')
			else:
				packed += param.to_bytes(4, 'little')
				packed += (3).to_bytes(4, 'little')

		switches = b''
		for i in range(4):
			packed += self.switches[i][0].to_bytes(1, 'little')
			switches += self.switches[i][1].to_bytes(2, 'little')
		packed += switches
		
		packed += self.relationships.pack(name_repr, name_offset, self.name)

		return packed



class Room:
	def __init__(self, data):
		self.fixed_hash = FixedHash(data)

		self.points = []
		point_entry = [e for e in self.fixed_hash.entries if e.name == b'point'][0]
		for entry in point_entry.data.entries:
			self.points.append(Point(entry.data))
		
		self.rails = []
		rail_entry = [e for e in self.fixed_hash.entries if e.name == b'rail'][0]
		for entry in rail_entry.data.entries:
			self.rails.append(Rail(data=entry.data))

		self.actors = []
		actor_entry = [e for e in self.fixed_hash.entries if e.name == b'actor'][0]
		for entry in actor_entry.data.entries:
			self.actors.append(Actor(entry.data, self.fixed_hash.names_section))

		try:
			grid_entry = [e for e in self.fixed_hash.entries if e.name == b'grid'][0]
			self.grid = Grid(grid_entry)
		except IndexError:
			self.grid = None


	def repack(self):
		new_names = b''

		for entry in self.fixed_hash.entries:
			if entry.name == b'point':
				entry.data.entries = []
				for point in self.points:
					# Create a new point entry for actors to use
					entry.data.entries.append(Entry(0xFFF3, b'', 0xFFFFFFFF, point.pack()))

			if entry.name == b'rail':
				rail = Rail(data=None, len_points=len(self.points))
				entry.data.entries = []
				entry.data.entries.append(Entry(0xFFF2, b'', 0xFFFFFFFF, rail.pack()))
				# for rail in self.rails:
				# 	# Create a new rail entry to reference point indexes per rail
				# 	entry.data.entries.append(Entry(0xFFF2, b'', 0xFFFFFFFF, rail.pack(len(new_names))))

				# 	# for param in rail.xC:
				# 	# 	if isinstance(param, bytes):
				# 	# 		new_names += param + b'\x00'

			if entry.name == b'actor':
				entry.data.entries = []
				for actor in self.actors:
					# Create a new entry for the actor in the actors FixedHash, using a newly packed data block for that actor
					entry.data.entries.append(Entry(0xFFF0, b'', 0xFFFFFFFF, actor.pack(len(new_names))))

					new_names += actor.name + b'\x00'
					
					for param in actor.parameters:
						if isinstance(param, bytes):
							new_names += param + b'\x00'
					
					for s1 in actor.relationships.section_1:
						if isinstance(s1[0][0], bytes):
							new_names += s1[0][0] + b'\x00'
						if isinstance(s1[0][1], bytes):
							new_names += s1[0][1] + b'\x00'
					
					for s2 in actor.relationships.section_2:
						if isinstance(s2[0][0], bytes):
							new_names += s2[0][0] + b'\x00'
						if isinstance(s2[0][1], bytes):
							new_names += s2[0][1] + b'\x00'
			
			if entry.name == b'grid' and self.grid != None:
				entry.data.entries = []
				entry.data.entries.append(Entry(0xFFF0, b'data', 0xFFFFFFFF, self.grid.pack()))
				# new_names += b'data' + b'\x00'

				if self.grid.chain_entry is not None:
					entry.data.entries.append(Entry(0xFFF0, b'chain', 0xFFFFFFFF, self.grid.chain_entry.data))
				
				entry.data.entries.append(Entry(0xFFF0, b'info', 0x0, self.grid.info.pack()))
				# new_names += b'info' + b'\x00'
			
			new_names += entry.name + b'\x00'

		self.fixed_hash.names_section = new_names

		return self.fixed_hash.toBinary()



class Relationship:
	def __init__(self, data, names):
		# no need to bother reading these, we will determine these when repacking
		# self.is_enemy = readBytes(data, 0x84, 1)
		# self.check_kills = readBytes(data, 0x85, 1)
		# self.is_chamber_enemy = readBytes(data, 0x86, 1)

		self.num_entries_1 = readBytes(data, 0x87, 1) # this is not a mistake, group sizes are defined in the order 1, 3, 2
		self.num_entries_3 = readBytes(data, 0x88, 1)
		self.num_entries_2 = readBytes(data, 0x89, 1)

		# self.null = data[0x8A:0x90] # always null bytes, no need to read this and will manually add them when repacking

		self.section_1 = []
		self.section_2 = []
		self.section_3 = []

		pos = 0x90
		
		for i in range(self.num_entries_1):
			acts = []
			seq = []

			for b in range(2):
				param_type = readBytes(data, pos + (0x8 * b) + 0x4, 4)

				if param_type == 0x2:
					param = readFloat(data, pos + (0x8 * b))
				else:
					param = readBytes(data, pos + (0x8 * b), 4)
				
				if param_type == 0x4:
					seq.append(readString(names, param))				
				else:
					seq.append(param)
			
			act_index = readBytes(data, pos + 0x10, 4)
			acts.append(seq)
			acts.append(act_index)
			self.section_1.append(acts)
			pos += 20
		
		for i in range(self.num_entries_2):
			acts = []
			seq = []

			for b in range(2):
				param_type = readBytes(data, pos + (0x8 * b) + 0x4, 4)

				if param_type == 0x2:
					param = readFloat(data, pos + (0x8 * b))
				else:
					param = readBytes(data, pos + (0x8 * b), 4)
				
				if param_type == 0x4:
					seq.append(readString(names, param))				
				else:
					seq.append(param)
			
			rail = readBytes(data, pos + 0x10, 4)
			point = readBytes(data, pos + 0x14, 4)
			acts.append(seq)
			acts.append(rail)
			acts.append(point)
			self.section_2.append(acts)
			pos += 24
		
		for i in range(self.num_entries_3):
			id = readBytes(data, pos + (0x4 * i), 4)
			self.section_3.append(id)
	

	def pack(self, name_repr, name_offset, actor_name: str):
		packed = b''
		is_enemy = 1 if actor_name.startswith(b'Enemy') else 0
		check_kills = 1 if actor_name.endswith(b'HolocaustChecker') else 0
		is_chamber_enemy = 0 # cant see any purpose for this, so leave as 0
		packed += is_enemy.to_bytes(1, 'little')
		packed += check_kills.to_bytes(1, 'little')
		packed += is_chamber_enemy.to_bytes(1, 'little')
		packed += self.num_entries_1.to_bytes(1, 'little')
		packed += self.num_entries_3.to_bytes(1, 'little')
		packed += self.num_entries_2.to_bytes(1, 'little')
		for i in range(6):
			packed += b'\x00'

		for i in range(self.num_entries_1):
			param1 = self.section_1[i][0][0]
			param2 = self.section_1[i][0][1]
			act_index = self.section_1[i][1]

			if isinstance(param1, bytes):
				packed += (len(name_repr) + name_offset).to_bytes(4, 'little')
				packed += (4).to_bytes(4, 'little')
				name_repr += param1 + b'\x00'
			elif isinstance(param1, np.float32):
				packed += struct.pack('<f', param1)
				packed += (2).to_bytes(4, 'little')
			else:
				packed += param1.to_bytes(4, 'little')
				packed += (3).to_bytes(4, 'little')
			
			if isinstance(param2, bytes):
				packed += (len(name_repr) + name_offset).to_bytes(4, 'little')
				packed += (4).to_bytes(4, 'little')
				name_repr += param2 + b'\x00'
			elif isinstance(param2, np.float32):
				packed += struct.pack('<f', param2)
				packed += (2).to_bytes(4, 'little')
			else:
				packed += param2.to_bytes(4, 'little')
				packed += (3).to_bytes(4, 'little')
			
			packed += act_index.to_bytes(4, 'little')
		
		for i in range(self.num_entries_2):
			param1 = self.section_2[i][0][0]
			param2 = self.section_2[i][0][1]
			rail = self.section_2[i][1]
			point = self.section_2[i][2]

			if isinstance(param1, bytes):
				packed += (len(name_repr) + name_offset).to_bytes(4, 'little')
				packed += (4).to_bytes(4, 'little')
				name_repr += param1 + b'\x00'
			elif isinstance(param1, np.float32):
				packed += struct.pack('<f', param1)
				packed += (2).to_bytes(4, 'little')
			else:
				packed += param1.to_bytes(4, 'little')
				packed += (3).to_bytes(4, 'little')
			
			if isinstance(param2, bytes):
				packed += (len(name_repr) + name_offset).to_bytes(4, 'little')
				packed += (4).to_bytes(4, 'little')
				name_repr += param2 + b'\x00'
			elif isinstance(param2, np.float32):
				packed += struct.pack('<f', param2)
				packed += (2).to_bytes(4, 'little')
			else:
				packed += param2.to_bytes(4, 'little')
				packed += (3).to_bytes(4, 'little')
			
			packed += rail.to_bytes(4, 'little')
			packed += point.to_bytes(4, 'little')
		
		for i in range(self.num_entries_3):
			packed += self.section_3[i].to_bytes(4, 'little')
		
		return packed



# EXPERIMENTAL POINT AND RAIL SECTIONS
class Point(Vector3):
	def __init__(self, data):
		vector = readVector3(data, 0x0)
		self.x = vector.x
		self.y = vector.y
		self.z = vector.z

	def pack(self):
		packed = b''
		packed += struct.pack('<f', self.x)
		packed += struct.pack('<f', self.y)
		packed += struct.pack('<f', self.z)
		for i in range(0xC):
			packed += b'\xFF'
		return packed



class Rail:
	def __init__(self, data=None, len_points=None):
		if data is not None:

			# always blocks of [25, 0xFFFFFF04] for some reason, so we won't bother parsing this
			# self.xC = []
			# for i in range(4):
			# 	paramType = readBytes(data, 0xC + (0x8 * i) + 0x4, 4)

			# 	if paramType == 0x2:
			# 		param = readFloat(data, 0xC + (0x8 * i))
			# 	else:
			# 		param = readBytes(data, 0xC + (0x8 * i), 4)
				
			# 	if paramType == 0xFFFFFF04:
			# 		self.xC.append(readString(names, param))
			# 	else:
			# 		self.xC.append(param)

			self.xC = [25, 25, 25, 25]
			self.num_entries = readBytes(data, 0x2C, 2)
			self.num_indexes = readBytes(data, 0x2E, 2)

			self.points = []
			for i in range(self.num_entries):
				self.points.append(readBytes(data, (0x30 + (0x2 * i)), 2))
		
		else:
			self.xC = [25, 25, 25, 25]
			self.num_entries = len_points
			self.num_indexes = 0x1
			self.points = []
			for i in range(len_points):
				self.points.append(i)


	def pack(self):
		"""Pack all points into a single rail"""

		packed = b''
		for i in range(0xC):
			packed += b'\x00'
		
		# nameRepr = b'' # + b'\x00'

		for i in range(4):
			param = self.xC[i]
			packed += param.to_bytes(4, 'little')
			packed += (0xFFFFFF04).to_bytes(4, 'little')
			# if isinstance(param, bytes):
			# 	packed += (len(nameRepr) + nameOffset).to_bytes(4, 'little')
			# 	packed += (0xFFFFFF04).to_bytes(4, 'little')
			# 	nameRepr += param + b'\x00'
			# elif isinstance(param, np.float32):
			# 	packed += struct.pack('<f', param)
			# 	packed += (2).to_bytes(4, 'little')
			# else:
			# 	packed += param.to_bytes(4, 'little')
			# 	packed += (3).to_bytes(4, 'little')

		packed += self.num_entries.to_bytes(2, 'little')
		packed += self.num_indexes.to_bytes(2, 'little')

		for i in range(self.num_entries):
			packed += self.points[i].to_bytes(2, 'little')
		
		return packed



# EXPERIMENTAL GRID SECTION
class Grid:
	def __init__(self, entry):
		self.chain_entry = None

		for e in entry.data.entries:
			if e.name == b'data':
				self.data_entry = e
				continue
			if e.name == b'chain':
				self.chain_entry = e
				continue
			if e.name == b'info':
				self.info = self.InfoBlock(e.data)
		
		if self.info.room_height not in (8, 2):
			raise ValueError('Cannot determine room type')
		
		self.tilesdata = []
		
		if self.info.room_type == '3D':
			for i in range(80):
				start_addr = (0x10 * i)
				self.tilesdata.append(self.TileData(self.data_entry.data[start_addr : (start_addr + 0x10)]))
		else:
			for i in range(20):
				start_addr = (0x10 * i)
				self.tilesdata.append(self.TileData(self.data_entry.data[start_addr : (start_addr + 0x10)]))
	

	def pack(self): # this handles packing of just the data entry
		packed = b''
		for tile in self.tilesdata:
			packed += tile.pack()
		
		return packed
	
	

	class TileData:
		def __init__(self, data):
			flags_byte = readBytes(data, 0x0, 1)
			self.flags1 = {
				'southcollision': 1 if flags_byte&128 != 0 else 0,
				'unused6': 1 if flags_byte&64 != 0 else 0,
				'eastcollision': 1 if flags_byte&32 != 0 else 0,
				'unused4': 1 if flags_byte&16 != 0 else 0,
				'northcollision': 1 if flags_byte&8 != 0 else 0,
				'unused2': 1 if flags_byte&4 != 0 else 0,
				'containscollision': 1 if flags_byte&2 != 0 else 0,
				'deepwaterlava': 1 if flags_byte&1 != 0 else 0
			}
			
			flags_byte = readBytes(data, 0x1, 1)
			self.flags2 = {
				'unused7': 1 if flags_byte&128 != 0 else 0,
				'unused6': 1 if flags_byte&64 != 0 else 0,
				'unused5': 1 if flags_byte&32 != 0 else 0,
				'unused4': 1 if flags_byte&16 != 0 else 0,
				'unused3': 1 if flags_byte&8 != 0 else 0,
				'unused2': 1 if flags_byte&4 != 0 else 0,
				'westcollision': 1 if flags_byte&2 != 0 else 0,
				'unused0': 1 if flags_byte&1 != 0 else 0
			}
			
			flags_byte = readBytes(data, 0x2, 1)
			self.flags3 = {
				'unused7': 1 if flags_byte&128 != 0 else 0,
				'unknown6': 1 if flags_byte&64 != 0 else 0,
				'canrefresh': 1 if flags_byte&32 != 0 else 0,
				'respawnload': 1 if flags_byte&16 != 0 else 0,
				'respawnvoid': 1 if flags_byte&8 != 0 else 0,
				'iswaterlava': 1 if flags_byte&4 != 0 else 0,
				'unused1': 1 if flags_byte&2 != 0 else 0,
				'isdigspot': 1 if flags_byte&1 != 0 else 0
			}
			
			flags_byte = readBytes(data, 0x3, 1)
			self.flags4 = {
				'unused7': 1 if flags_byte&128 != 0 else 0,
				'unused6': 1 if flags_byte&64 != 0 else 0,
				'unused5': 1 if flags_byte&32 != 0 else 0,
				'unused4': 1 if flags_byte&16 != 0 else 0,
				'unused3': 1 if flags_byte&8 != 0 else 0,
				'unused2': 1 if flags_byte&4 != 0 else 0,
				'unused1': 1 if flags_byte&2 != 0 else 0,
				'unused0': 1 if flags_byte&1 != 0 else 0
			}
			
			# self.unknown = data[0x4:0x8] # matches the first 4 bytes

			self.chain_index = readBytes(data, 0x8, 4)
			self.elevation = readFloat(data, 0xC)
		

		def pack(self):
			packed = b''

			bin_str1 = ''.join(str(i) for i in list(self.flags1.values()))
			packed += int(bin_str1, 2).to_bytes(1, 'little')

			bin_str2 = ''.join(str(i) for i in list(self.flags2.values()))
			packed += int(bin_str2, 2).to_bytes(1, 'little')

			bin_str3 = ''.join(str(i) for i in list(self.flags3.values()))
			packed += int(bin_str3, 2).to_bytes(1, 'little')

			bin_str4 = ''.join(str(i) for i in list(self.flags4.values()))
			packed += int(bin_str4, 2).to_bytes(1, 'little')

			# packed += self.unknown
			
			# having this match the first 4 bytes is important for the tile properties to work properly
			packed += int(bin_str1, 2).to_bytes(1, 'little')
			packed += int(bin_str2, 2).to_bytes(1, 'little')
			packed += int(bin_str3, 2).to_bytes(1, 'little')
			packed += int(bin_str4, 2).to_bytes(1, 'little')

			packed += self.chain_index.to_bytes(4, 'little')
			packed += struct.pack('<f', self.elevation)

			return packed
	


	class InfoBlock:
		def __init__(self, data):
			self.room_height = readBytes(data, 0x0, 2) # how many tiles on the Z-axis: 8 for 3D rooms, 2 for 2D rooms
			self.room_width = readBytes(data, 0x2, 2) # how many tiles on the X-axis, always 10
			self.room_type = '3D' if self.room_height == 8 else '2D'
			self.tile_size = readFloat(data, 0x4)
			self.x_coord = readFloat(data, 0x8)
			self.z_coord = readFloat(data, 0xC)
		
		def pack(self):
			packed = b''
			packed += self.room_height.to_bytes(2, 'little')
			packed += self.room_width.to_bytes(2, 'little')
			packed += struct.pack('<f', self.tile_size)
			packed += struct.pack('<f', self.x_coord)
			packed += struct.pack('<f', self.z_coord)

			return packed
