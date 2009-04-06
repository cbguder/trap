from point import Point

def interpolate(a, b, ratio):
	dx = b.x - a.x
	dy = b.y - a.y

	x = a.x + ratio * dx
	y = a.y + ratio * dy

	return Point(x, y)

# Cohen-Sutherland Algorithm
def intersect(movement, region):
	LEFT, RIGHT, BOTTOM, TOP = 1, 2, 4, 8

	xmin = region.x
	xmax = region.x + region.width
	ymin = region.y
	ymax = region.y + region.height

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

	x0, y0 = movement.src.x, movement.src.y
	x1, y1 = movement.dest.x, movement.dest.y

	start_code = outcode(x0, y0)
	end_code = outcode(x1, y1)

	while True:
		if start_code | end_code == 0:
			return (Point(x0, y0), Point(x1, y1))

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
