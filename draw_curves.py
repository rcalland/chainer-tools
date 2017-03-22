#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import fnmatch
import numpy as np
import re
import sys
import json
from scipy import signal

if 'linux' in sys.platform:
	import matplotlib
	matplotlib.use('Qt4Agg')
	import matplotlib.pyplot as plt
else:
	import matplotlib.pyplot as plt

from matplotlib.pyplot import cm 

def style_selector(name):
	if fnmatch.fnmatch(name, "critic/*"):
		return "dashed"
	elif fnmatch.fnmatch(name, "labeler/*"):
		return "dotted"
	else:
		return "solid"

def draw_plots(logfile, outfile, x_start, x_end, logy=False, filter=False, skip=None, colors=None):
	with open(logfile, "r") as f:
		log = json.load(f)
		
		iteration = []
		curves = {}

		# first make the structure to store points
		for element in log[0]:
			if not element in skip:
				curves[element] = []
			#curves[curve.key] = []

		for epoch in log:
			i = int(epoch["iteration"])

			if i > int(x_start) and i < int(x_end):
				iteration.append(i)
				
				for key, value in epoch.items():
					if not key in skip:
						curves[key].append(value)

		# median filter
		if filter:
			ks = 51
			for key, value in curves.items():
				curves[key] = signal.medfilt(value, kernel_size=ks)

		plt.clf()
		plt.ion()
		plt.figure(1)
		ax = plt.subplot(111)

		plt.grid()
		if logy:
			plt.yscale('log')

		lw = 3
		#colors = [colormap(i) for i in np.linspace(0, 1,len(curves))]
		#color = iter(colors)

		if colors is None:
			color=cm.nipy_spectral(np.linspace(0,1,len(curves)))
		else:
			color=colors
		#color = 3

		#color.reset()

		ic = 0
		for key, value in curves.items():
			#print(key, len(value))
			#print(key, value)
			ax.plot(iteration, value, ls=style_selector(key), c=color[ic], linewidth=lw, label=key)
			ic += 1
			#color += 2

		plt.xlabel("Iteration")
		plt.ylabel("loss")

		plt.legend().remove()
		#box = ax.get_position()
		#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
		ax.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5,1.14), shadow=False)

		plt.xlim(iteration[0], iteration[-1])

		#plt.tight_layout()
		plt.pause(2)
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--logfile', "-l", type=str, default='log.txt')
	parser.add_argument('--outfile', "-o", type=str, default='log.png')
	parser.add_argument("--start", "-s", type=int, default=0)
	parser.add_argument("--end", "-e", type=int, default=1E8)
	parser.add_argument("--filter", "-f", action="store_true")
	parser.add_argument("--update", "-u", type=bool, default=True)
	parser.add_argument("--logy", "-ly", action="store_true")
	args = parser.parse_args()

	skip = ["epoch", "iteration", "elapsed_time", "labeler/loss",  "refiner/critic/loss",  "refiner/labeler/loss",  "self_reg/loss" , "labeler/loss/synth", "labeler/loss/refined"]
	colors = ["blue", "green", "red", "yellow","pink","gray","c", "m","black"]

	looper = True
	while looper:
		draw_plots(args.logfile, args.outfile, x_start=args.start, x_end=args.end, logy=args.logy, filter=args.filter, skip=skip, colors=colors)
		looper = args.update