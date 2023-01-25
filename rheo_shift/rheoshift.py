#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import csv
#####
def main():
	# Main Window
	window = make_mainwindow()

	# Main Loop
	while True:
		event, values = window.read()

		if event in [sg.WIN_CLOSED, '-cancel-']:
			break
		
		if event == '-select-':
			csvfile = sg.popup_get_file('get file', file_types=(("CSV Files", ".csv"),))
			with open(csvfile, encoding='utf8') as f:
				csvlist = list(csv.reader(f))

	window.close()

	return

#####
# Main Window
#####
def make_mainwindow():

	main_layout = [
					[
						sg.Text('Original Data File:', size = (10,1)), 
						sg.Text('not selected yet', size = (10,1)),
						sg.Button('Select', key='-select-')
					],
					[sg.Cancel()]
				]
	return sg.Window('Main Window', main_layout)


#####
# Read csv
#####
def read_csv():
	csvfile = ''
	layout = [
			[sg.Text('読み取り対象のファイルを指定してください')],
			[sg.Button('Select', key='-select-'),
			sg.Cancel(), 
			]
			]
	window = sg.Window('CSV file の読み込み', layout)

	while True:
		event, values = window.read()

		if event in [sg.WIN_CLOSED, '-cancel-']:
			window.close()
		
		if event == '-select-':
			csvfile = sg.popup_get_file('get file', file_types=(("CSV Files", ".csv"),))
			with open(csvfile, encoding='utf8') as f:
				csvlist = list(csv.reader(f))

	

	return csvfile

#####
# Cut out
#####
def cutcsv_window(csvfile):
	with open(csvfile, encoding='utf8') as f:
		csvread = list(csv.reader(f))
	
	ncolm_list = [str(x) for x in range(len(csvread[0]))]
	# ウィンドウのレイアウト
	layout=[
			[sg.Text('選択した読み取り対象のファイル:'), sg.Text(csvfile)],
			[sg.Button('Submit',key='submit')],
			[sg.Table(csvread, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=30)]
			]
	window = sg.Window('CSV data table !', layout, resizable = True, finalize=True)
	return csvread, window

def cutcsv(csvfile):
	datalabel = ['温度', '角周波数', '貯蔵弾性率', '損失弾性率', '損失正接']
	# ウィンドウオブジェクトの作成
	csvread, window = cutcsv_window(csvfile)
	# イベントのループ
	while True:
		# イベントの読み込み
		event, values = window.read()
		# ウィンドウの×ボタンクリックで終了
		if event == sg.WIN_CLOSED:
			break

		elif event == 'submit':
			datalist = []
			for i, line in enumerate(csvread):
				if datalabel[0] in line and datalabel[1] in line:
					start = i
					pos = []
					for item in datalabel:
						pos.append(csvread[start].index(item))
					count = start + 2
					tmp = []
					for dataline in csvread[count:]:
						if dataline[0] != '':
							tmp.append([float(dataline[col]) for col in pos])
						
						else:
							break
					dataarray= np.array(tmp)
					tmp = []
					temp = round(np.mean(dataarray[:, 0]), 1)
					tmp.append(temp)
					for i in range(1, dataarray.shape[1]):
						tmp.append(list(dataarray[:, i]))
					datalist.append(tmp)
			print(datalist[0])

	# ウィンドウ終了処理
	window.close()
	return

if __name__ == '__main__':
	main()