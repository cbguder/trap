from lib.node import Node, Movement
from lib.packet import Packet

class TraceParser:
	def __init__(self):
		self.nodes = {}
		self.vs_types = set()

	def get_nodes(self):
		return self.nodes.values()

	def get_node(self, id):
		if not self.nodes.has_key(id):
			self.nodes[id] = Node(id)
		return self.nodes[id]

	def parse(self, f):
		for line in f:
			event_type = line[0]

			if event_type == 'M':
				m = Movement(line)
				self.get_node(m.node_id).movements.append(m)
			elif event_type in ['s', 'r']:
				packet = Packet(line)
				node   = self.get_node(packet.node_id)

				if event_type == 'r':
					node.receive_packet(packet)
				elif event_type == 's':
					node.send_packet(packet)

				if packet.type == 'VirtualSign':
					self.vs_types.add(packet.vs_type)
