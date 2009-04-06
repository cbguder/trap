class Packet:
	def __init__(self, line=None):
		if line != None:
			self.parse(line)

	def parse(self, line):
		packet = {}
		parts  = line.split()

		for i in range(1, len(parts), 2):
			packet[parts[i][1:]] = parts[i+1]

		self.event_type = parts[0]
		self.time       = float(packet['t'])

		self.node_id     = int(packet['Ni'])
		self.node_x      = float(packet['Nx'])
		self.node_y      = float(packet['Ny'])
		self.node_z      = float(packet['Nz'])
		self.node_energy = float(packet['Ne'])

		self.trace_level = packet['Nl']
		self.reason      = packet['Nw']

		self.source      = packet['Is']
		self.destination = packet['Id']

		self.type    = packet['It']
		self.size    = packet['Il']
		self.flow_id = packet['If']
		self.id      = packet['Ii']
