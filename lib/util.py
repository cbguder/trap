from math import sqrt

def distance(a, b):
	dx = a[0] - b[0]
	dy = a[1] - b[1]
	return sqrt(dx**2 + dy**2)

def interpolate(a, b, ratio):
	dx = b[0] - a[0]
	dy = b[1] - a[1]

	x = a[0] + ratio * dx
	y = a[1] + ratio * dy

	return (x, y)

# Cohen-Sutherland Algorithm
def intersect(movement, region):
	LEFT, RIGHT, BOTTOM, TOP = 1, 2, 4, 8

	xmin = region[0]
	xmax = region[0] + region[2]
	ymin = region[1]
	ymax = region[1] + region[3]

	def outcode(x, y):
		code = 0

		if y > ymax:
			code += TOP
		elif y < ymin:
			code += BOTTOM

		if x > xmax:
			code += RIGHT
		elif x < xmin:
			code += LEFT

		return code

	x0, y0 = movement.src[0], movement.src[1]
	x1, y1 = movement.dest[0], movement.dest[1]

	start_code = outcode(x0, y0)
	end_code = outcode(x1, y1)

	while True:
		if start_code | end_code == 0:
			return ((x0, y0), (x1, y1))

		if start_code & end_code != 0:
			return None

		max_code = max(start_code, end_code)

		if max_code & TOP == TOP:
			x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
			y = ymax
		elif max_code & BOTTOM == BOTTOM:
			x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
			y = ymin

		if max_code & RIGHT == RIGHT:
			y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
			x = xmax
		elif max_code & LEFT == LEFT:
			y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
			x = xmin

		if max_code == start_code:
			x0, y0 = x, y
			start_code = outcode(x0, y0)
		else:
			x1, y1 = x, y
			end_code = outcode(x1, y1)
