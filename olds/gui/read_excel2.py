# ステップ1. インポート
import PySimpleGUI as sg
import os
import csv
import openpyxl
# import pandas as pd

def make_window():
	# ステップ3. ウィンドウの部品とレイアウト
	layout = [
			[sg.Text('読み取り対象のファイルを指定してください')],
			# [sg.Text('ファイル選択'),
			# 	sg.InputText('file path',key='-file-'),
			# 	sg.FilesBrowse('Browse', target='-file-', file_types=(('csv ファイル', '*.csv'),))],
			[sg.Button('Read', key='-read-'), sg.Button('Write', key='-write-')]
			]
	return sg.Window('CSV file の読み込み', layout)

def main():
	window = make_window()

	# ステップ5. イベントループ
	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED: #ウィンドウのXボタンを押したときの処理
			break

		if event == '-read-': #「読み取り」ボタンが押されたときの処理
			excelfile = sg.popup_get_file('get file', file_types=(("Excel Files", ".xlsx"),))
			wb = openpyxl.load_workbook(excelfile)
			print(wb.sheetnames)
			ws = wb['data']
			print(len(ws.rows[0]))
			# for row in ws.rows:
			#    print( [cell.value for cell in row] )

			# with open(csvfilename, 'w', newline="") as csvfile:
			#     writer = csv.writer(csvfile)
			#     for row in ws.rows:
			#         writer.writerow( [cell.value for cell in row] )
			
			
			# df_sheet_all = pd.read_excel(excelfile, sheet_name=None)
			# print(df_sheet_all['data'])

		
		if event == '-write-': #「読み取り」ボタンが押されたときの処理
			value = sg.popup_get_file('save', save_as=True, file_types=(("Text Files", ".txt"),))
			# csvfile = values['-file-'] # ファイルパスを取得
			# if csvfile != 'file path' and os.path.isfile(csvfile):
			# 	with open(csvfile, encoding='utf8') as f:
			# 		csvlist = list(csv.reader(f))
			# 	# for line in csvlist:
			# 		# print(line)
			# else:
			# 	# ポップアップでメッセージ表示
			# 	sg.popup('CSV ファイルを指定してください。')
			print(value)

	window.close()

if __name__ == '__main__':
	main()