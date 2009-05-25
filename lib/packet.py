from region import CircularRegion

class Packet:
	def __init__(self, line=None):
		if line != None:
			self.parse(line)

	def parse(self, line):
		packet = {}
		parts  = line.split()

		for i in range(1, len(parts), 2):
			packet[parts[i][1:]] = parts[i+1]

		self.time = float(packet['t'])
		self.type = packet['It']

		self.node_id = int(packet['Ni'])
		self.node_x = float(packet['Nx'])
		self.node_y = float(packet['Ny'])

		if packet.has_key('Vt'):
			self.vs_type = int(packet['Vt'])

		if packet.has_key('Vc') and packet.has_key('Vr'):
			center = packet['Vc'].split(',')
			x = float(center[0])
			y = float(center[1])
			r = float(packet['Vr'])
			self.region = CircularRegion(x, y, r)
