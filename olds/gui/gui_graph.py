#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import random

def org_data():
	x = [i for i in range(100)]
	y = [np.sin(i*np.pi/20.) for i in range(100)]
	return np.vstack([x,y])

def set_data():
	x = [i for i in range(100)]
	y = [random.random() for i in range(100)]
	return np.vstack([x,y])

def make_fig(data):
	fig, ax = plt.subplots()
	ax.plot(data[0], data[1])
	ax.set_xlabel('x')  # x軸ラベル
	ax.set_ylabel(r'y')  # y軸ラベル
	ax.set_title('Title') # グラフタイトル
	return fig


def draw_plot(fig):
	plt.show(block=False)

def del_plot(fig):
	plt.close()

def main():
	sg.theme('Light Blue 2')
	fig_ = ''


	layout = [[sg.Text('Graph Diasplay')],
			[sg.Button('Original',key='-org-'), sg.Button('Rewrite',key='-rewrite-'), sg.Button('Clear',key='-clear-'), sg.Cancel()]
			]

	window = sg.Window('Plot', layout, location=(100, 100), finalize=True)

	while True:
		event, values = window.read()

		if event in (None, 'Cancel'):
			break

		elif event == '-org-':
			if fig_ != '':
				del_plot(fig_)
			datalist = org_data()
			fig_ = make_fig(datalist)
			draw_plot(fig_)

		elif event == '-rewrite-':
			del_plot(fig_)

			datalist = set_data()
			fig_ = make_fig(datalist)
			draw_plot(fig_)
		
		elif event == '-clear-' and fig_ != '':
			del_plot(fig_)

	window.close()

if __name__ == '__main__':
	main()