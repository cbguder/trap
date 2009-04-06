class Region:
	def __init__(self, x, y, width, height):
		self.x = float(x)
		self.y = float(y)
		self.width = float(width)
		self.height = float(height)

	def contains(self, p):
		return self.x <= p.x <= self.x + self.width and \
		       self.y <= p.y <= self.y + self.height
