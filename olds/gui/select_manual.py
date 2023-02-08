import PySimpleGUI as sg
import csv

def readcsv(csvfile):
	with open(csvfile, encoding='utf8') as f:
		csvread = list(csv.reader(f))
	return csvread

def csvdatawindow(csvread):
	ncolm_list = [str(x) for x in range(len(csvread[0]))]

	# ウィンドウのレイアウト
	layout=[
			# [sg.Text('選択した読み取り対象のファイル:'), sg.Text(csvfile)],
			[sg.Text('ラベルの行番号', size=(15,1)), sg.Input('28', key='-r_label-', size=(4,1))],
			[sg.Text('ラベルの行数', size=(15,1)), sg.Spin([1,2,3,4,5], '2', key='-n_label-')],
			[sg.Text('測定点数', size=(15,1)), sg.Input('11', key='-n_data-', size=(4,1))],
			# [sg.Text('温度のカラム番号'), sg.Spin(ncolm_list, '2', key='n_label')],
			# [sg.Text('角周波数のカラム番号'), sg.Spin(ncolm_list, '3', key='n_label')],
			# [sg.Text('貯蔵弾性率のカラム番号'), sg.Spin(ncolm_list, '9', key='n_label')],
			# [sg.Text('損失弾性率のカラム番号'), sg.Spin(ncolm_list, '10', key='n_label')],
			# [sg.Text('損失正接のカラム番号'), sg.Spin(ncolm_list, '12', key='n_label')],
			[sg.Button('Submit',key='submit')],
			[sg.Table(csvread, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=30)]
			]

	return sg.Window('CSV data table !', layout, resizable = True, finalize=True)

def main_routin():
	# ウィンドウのテーマ
	sg.theme('SandyBeach')

	# CSVの値
	csvfile = 'datafile.csv'
	csvread = readcsv(csvfile)

	# ウィンドウオブジェクトの作成
	window = csvdatawindow(csvread)

	# イベントのループ
	while True:
		# イベントの読み込み
		event, values = window.read()
		# ウィンドウの×ボタンクリックで終了
		if event == sg.WIN_CLOSED:
			break

		elif event == 'submit':
			r_label = values['-r_label-']
			n_label = values['-n_label-']
			n_data = values['-n_data-']
			inputdata = f'ラベルの行番号: {r_label}\nラベルの行数: {n_label}\n測定点数: {n_data}'
			sg.popup(inputdata)

			pos = []
			for i in ['温度', '角周波数', '貯蔵弾性率', '損失弾性率', '損失正接']:
				pos.append(csvread[int(r_label)].index(i))
			print(pos)

	# ウィンドウ終了処理
	window.close()
	return

if __name__ == '__main__':
	main_routin()