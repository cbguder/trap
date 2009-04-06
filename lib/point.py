from math import sqrt

class Point:
	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def __str__(self):
		return (self.x, self.y).__str__()

	def distance_to(self, p):
		dx = self.x - p.x
		dy = self.y - p.y
		return sqrt(dx**2 + dy**2)
