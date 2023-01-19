import PySimpleGUI as sg
import csv

def mainwindow(csvfile):
	with open(csvfile, encoding='utf8') as f:
		csvread = list(csv.reader(f))

	ncolm_list = [str(x) for x in range(len(csvread[0]))]

	# ウィンドウのレイアウト
	layout=[
			[sg.Text('選択した読み取り対象のファイル:'), sg.Text(csvfile)],
			[sg.Text('ラベルの行番号'), sg.Input('28', key='c_label')],
			[sg.Text('ラベルの行数'), sg.Spin([1,2,3,4,5], '2', key='n_label')],
			[sg.Text('測定点数'), sg.Input('11', key='c_label')],
			[sg.Text('温度のカラム番号'), sg.Spin(ncolm_list, '2', key='n_label')],
			[sg.Text('角周波数のカラム番号'), sg.Spin(ncolm_list, '3', key='n_label')],
			[sg.Text('貯蔵弾性率のカラム番号'), sg.Spin(ncolm_list, '9', key='n_label')],
			[sg.Text('損失弾性率のカラム番号'), sg.Spin(ncolm_list, '10', key='n_label')],
			[sg.Text('損失正接のカラム番号'), sg.Spin(ncolm_list, '12', key='n_label')],
			[sg.Table(csvread, headings=ncolm_list, display_row_numbers=True, def_col_width=6, auto_size_columns=False, vertical_scroll_only=False, num_rows=30)]
			]

	return sg.Window('CSV data table !', layout, resizable = True, finalize=True)



def main_routin():
	# ウィンドウのテーマ
	sg.theme('SandyBeach')

	# 行列の値
	csvfile = 'datafile.csv'

	# ウィンドウオブジェクトの作成
	window = mainwindow(csvfile)

	# イベントのループ
	while True:
		# イベントの読み込み
		event, values = window.read()
		# ウィンドウの×ボタンクリックで終了
		if event == sg.WIN_CLOSED:
			break
	# ウィンドウ終了処理
	window.close()
	return

if __name__ == '__main__':
	main_routin()