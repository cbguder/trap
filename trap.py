#!/usr/bin/env python

import sys
import os.path
from lib.region import Region
from traceparser import TraceParser

REGION = Region(550, 0, 300, 110)
SIMULATION_TIME = 60.0
TRUST = 1

def main():
	if len(sys.argv) < 2:
		print "USAGE: trap <TRACEFILES>"
		sys.exit()

	for file in sys.argv[1:]:
		print "Trapping %s..." % file
		with open(file) as f:
			graph = analyze(f)
			with open(file + '.region.gpi', 'w') as f:
				plot(f, graph, file)

def analyze(f):
	vr = {} # Vehicles in Region
	avr = {} # Active Vehicles in Region

	tp = TraceParser()
	tp.parse(f)

	nodes = tp.get_nodes()

	for node in nodes:
		enter, exit = node.intersect(REGION)

		if enter != None:
			vr[enter] = vr.get(enter, 0) + 1
			vr[exit] = vr.get(exit, 0) - 1

			if node.has_trust_at(enter, TRUST):
				avr[enter] = avr.get(enter, 0) + 1
				avr[exit] = avr.get(exit, 0) - 1
			elif node.has_trust_at(exit, TRUST):
				t_trust = node.packet_times[TRUST - 1]
				avr[t_trust] = avr.get(t_trust, 0) + 1
				avr[exit] = avr.get(exit, 0) - 1

	times = sorted(list(set(vr.keys() + avr.keys())))
	graph = []
	total = 0
	active = 0

	for t in times:
		if t > SIMULATION_TIME:
			break

		if vr.has_key(t):
			total += vr[t]

		if avr.has_key(t):
			active += avr[t]

		if total == 0:
			graph.append({'t': t, 'percentage': 0.0})
		else:
			graph.append({'t': t, 'percentage': 1.0 * active / total})

	return graph

def plot(f, graph, file):
	f.write("set title '%s Regional Delivery'\n" % os.path.basename(file))
	f.write("set style data lines\n")
	f.write("set xlabel 'Time (s)'\n")
	f.write("set ylabel 'Percentage'\n")
	f.write("set xrange[0:]\n")
	f.write("set yrange[0:]\n")
	f.write("plot '-' t 'Aware Vehicles'\n")

	for g in graph:
		f.write('%(t)f %(percentage)f\n' % g)

if __name__ == '__main__':
	main()
