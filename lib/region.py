from util import distance

class Region:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def contains(self, p):
		return self.x <= p[0] <= self.x + self.width and \
		       self.y <= p[1] <= self.y + self.height

class CircularRegion:
	def __init__(self, x, y, r):
		self.r = r
		self.center = (x, y)

	def contains(self, p):
		return distance(self.center, p) <= self.r
