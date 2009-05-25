#!/usr/bin/env python

import sys
import math
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
			with open(file + '.region.overall.gpi', 'w') as f:
				plot(f, graph, file)

def analyze(f):
	vr = {} # Vehicles in Region
	avr = {} # Active Vehicles in Region
	graph = {}

	tp = TraceParser()
	tp.parse(f)

	nodes = tp.get_nodes()
	vs_types = sorted(list(tp.vs_types))

	analyze_intersections(nodes)
	vr = analyze_vr(nodes)
	vr_times = set(vr.keys())

	num_types = len(vs_types)
	avr = analyze_num_types(nodes, num_types)
	times = vr_times.copy()
	times.update(avr.keys())
	times = sorted(list(times))
	key = '%d Messages' % num_types
	graph[key] = analyze_graph(times, vr, avr)

	return graph

def analyze_intersections(nodes):
	for node in nodes:
		enter, exit = node.intersect(REGION)
		node.enter = enter
		node.exit = exit

def analyze_vr(nodes):
	vr = {}

	for node in nodes:
		if node.enter != None:
			vr[node.enter] = vr.get(node.enter, 0) + 1
			vr[node.exit] = vr.get(node.exit, 0) - 1

	return vr

def analyze_avr(nodes, vs_type):
	avr = {}

	for node in nodes:
		if node.enter != None:
			if node.has_trust_at(node.enter, vs_type, TRUST):
				avr[node.enter] = avr.get(node.enter, 0) + 1
				avr[node.exit] = avr.get(node.exit, 0) - 1
			elif node.has_trust_at(node.exit, vs_type, TRUST):
				t_trust = node.packet_times[vs_type][TRUST - 1]
				avr[t_trust] = avr.get(t_trust, 0) + 1
				avr[node.exit] = avr.get(node.exit, 0) - 1

	return avr

def analyze_num_types(nodes, types):
	avr = {}

	for node in nodes:
		if node.enter != None:
			enter_types = node.unique_types_at(node.enter)
			exit_types = node.unique_types_at(node.exit)

			if enter_types <= types <= exit_types:
				t1 = node.unique_types_when(types)
				t2 = node.unique_types_when(types + 1)

				if t1 < node.enter:
					t1 = node.enter
				if t2 > node.exit:
					t2 = node.exit

				avr[t1] = avr.get(t1, 0) + 1
				avr[t2] = avr.get(t2, 0) - 1

	return avr

def analyze_graph(times, vr, avr):
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
			graph.append((t, 0.0))
		else:
			graph.append((t, 1.0 * active / total))

	return graph

def plot(f, graph, file):
	keys = sorted(graph.keys())
	xrange = max([last_interesting_time(graph[key]) for key in keys])

	f.write("set title '%s Regional Delivery'\n" % os.path.basename(file))
	f.write("set style data lines\n")
	f.write("set xlabel 'Time (s)'\n")
	f.write("set ylabel 'Percentage'\n")
	f.write("set xrange[0:%d]\n" % math.ceil(xrange))
	f.write("set yrange[0:1]\n")

	plot_commands = ["'-' t '%s'" % key for key in keys]
	f.write("plot %s\n" % ', '.join(plot_commands))

	for key in keys:
		for g in graph[key]:
			f.write('%f %f\n' % g)
		f.write('e\n')

def last_interesting_time(g):
	last_val = g[-1][1]
	i = len(g) - 1
	while i >= 0 and g[i][1] == last_val:
		i -= 1
	return g[i][0]

if __name__ == '__main__':
	main()
