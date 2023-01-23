#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv

def make_window():
	layout = [
			[sg.Text('読み取り対象のファイルを指定してください')],
			[sg.Button('Select', key='-select-'), sg.Button('Write', key='-write-'), sg.Button('Cancel', key='-cancel-')]
			]
	return sg.Window('CSV file の読み込み', layout)

def main():
	window = make_window()

	while True:
		event, values = window.read()

		if event in [sg.WIN_CLOSED, '-cancel-'] : #ウィンドウのXボタンを押したときの処理
			break
		
		if event == '-select-':
			csvfile = sg.popup_get_file('get file', file_types=(("CSV Files", ".csv"),))
			with open(csvfile, encoding='utf8') as f:
				csvlist = list(csv.reader(f))
			for line in csvlist:
				print(line)

		if event == '-write-':
			filename = sg.popup_get_file('save', save_as=True, file_types=(("CSV Files", ".csv"),))
			if filename:
				with open(filename, 'w') as f:
					csv.writer(f).writerows(csvlist)
	window.close()

if __name__ == '__main__':
	main()