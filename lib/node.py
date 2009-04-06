from point import Point
from util import interpolate, intersect

class Node:
	def __init__(self, id):
		self.id = id
		self.movements = []
		self.first_activity = None

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

	def active_at(self, time):
		return self.first_activity != None and time >= self.first_activity

	def receive_packet(self, packet):
		if self.first_activity == None and packet.type == 'VirtualSign':
			self.first_activity = packet.time

	def send_packet(self, packet):
		if self.first_activity == None and packet.type == 'VirtualSign':
			self.first_activity = packet.time

	def intersect(self, region):
		for m in self.movements:
			intersection = intersect(m, region)
			if intersection != None:
				enter = m.time_for(intersection[0])
				exit = m.time_for(intersection[1])

				return (enter, exit)

		return (None, None)

class Movement:
	def __init__(self, line=None):
		self.src        = Point()
		self.dest       = Point()
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
		self.src.x      = float(l[3][1:-1])
		self.src.y      = float(l[4][:-1])
		self.src.z      = float(l[5][:-2])
		self.dest.x     = float(l[6][1:-1])
		self.dest.y     = float(l[7][:-2])
		self.speed      = float(l[8])

		self.distance   = self.src.distance_to(self.dest)
		self.total_time = self.distance / self.speed
		self.dx         = self.dest.x - self.src.x
		self.dy         = self.dest.y - self.src.y

	def position_at(self, time):
		dt = time - self.src_time

		if dt > 0.0 and self.total_time > 0.0:
			ratio = dt / self.total_time 
			return interpolate(self.src, self.dest, ratio)
		else:
			return self.src

	def time_for(self, p):
		distance = self.src.distance_to(p)
		return self.src_time + (distance / self.speed)
