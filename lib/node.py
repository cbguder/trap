from util import distance, interpolate, intersect

class Node:
	def __init__(self, id):
		self.id = id
		self.movements = []
		self.packet_times = {}
		self.type_times = []

	def position_at(self, time):
		movement = None
		for m in self.movements:
			if m.src_time > time:
				break
			movement = m

		if movement == None:
			return None
		else:
			return movement.position_at(time)

	def active_at(self, time, vs_type):
		return self.has_trust_at(time, vs_type, 1)

	def has_trust_at(self, time, vs_type, trust):
		if self.packet_times.has_key(vs_type) and len(self.packet_times[vs_type]) >= trust:
			return self.packet_times[vs_type][trust - 1] <= time
		else:
			return False

	def unique_types_at(self, time):
		return len([t for t in self.type_times if t <= time])

	def unique_types_when(self, types):
		if types == 0:
			return float('-inf')
		elif len(self.type_times) >= types:
			return self.type_times[types - 1]
		else:
			return float('inf')

	def receive_packet(self, packet):
		if packet.type == 'VirtualSign':
			if packet.region.contains((packet.node_x, packet.node_y)):
				if not self.packet_times.has_key(packet.vs_type):
					self.packet_times[packet.vs_type] = []
					self.type_times.append(packet.time)
				self.packet_times[packet.vs_type].append(packet.time)

	def send_packet(self, packet):
		self.receive_packet(packet)

	def intersect(self, region):
		enter, exit = None, None

		for m in self.movements:
			intersection = intersect(m, region)
			if intersection != None:
				_enter = m.time_for(intersection[0])
				_exit = m.time_for(intersection[1])

				if enter == None or _enter < enter:
					enter = _enter
				if exit == None or _exit > exit:
					exit = _exit

		return (enter, exit)

class Movement:
	def __init__(self, line=None):
		self.src        = (None,None)
		self.dest       = (None,None)
		self.src_time   = 0.0
		self.speed      = 0.0
		self.distance   = 0.0
		self.total_time = 0.0
		self.dx         = 0.0
		self.dy         = 0.0

		if line != None:
			self.parse(line)

	def parse(self, line):
		l = line.split()
		self.src_time   = float(l[1])
		self.node_id    = int(l[2])
		self.src        = (float(l[3][1:-1]), float(l[4][:-1]))
		self.dest       = (float(l[6][1:-1]), float(l[7][:-2]))
		self.speed      = float(l[8])

		self.distance   = distance(self.src, self.dest)
		self.total_time = self.distance / self.speed
		self.dx         = self.dest[0] - self.src[0]
		self.dy         = self.dest[1] - self.src[1]

	def position_at(self, time):
		dt = time - self.src_time

		if dt > 0.0 and self.total_time > 0.0:
			ratio = dt / self.total_time 
			return interpolate(self.src, self.dest, ratio)
		else:
			return self.src

	def time_for(self, p):
		dist = distance(self.src, p)
		return self.src_time + (dist / self.speed)
