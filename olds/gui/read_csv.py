# ステップ1. インポート
import PySimpleGUI as sg
import os
import csv

def make_window():
	# ステップ3. ウィンドウの部品とレイアウト
	layout = [
			[sg.Text('読み取り対象のファイルを指定してください')],
			[sg.Text('ファイル選択'),
				sg.InputText('file path',key='-file-'),
				sg.FilesBrowse('Browse', target='-file-', file_types=(('csv ファイル', '*.csv'),))],
			[sg.Button('read', key='read')]
			]
	return sg.Window('CSV file の読み込み', layout)

def main_routin():
	# ステップ2. デザインテーマの設定
	sg.theme('DarkTeal7')
	# ステップ4. ウィンドウの生成
	window = make_window()

	# ステップ5. イベントループ
	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED: #ウィンドウのXボタンを押したときの処理
			break

		if event == 'read': #「読み取り」ボタンが押されたときの処理
			csvfile = values['-file-'] # ファイルパスを取得
			if csvfile != 'file path' and os.path.isfile(csvfile):
				with open(csvfile, encoding='utf8') as f:
					csvlist = list(csv.reader(f))
				# for line in csvlist:
					# print(line)
			else:
				# ポップアップでメッセージ表示
				sg.popup('CSV ファイルを指定してください。')

	window.close()

if __name__ == '__main__':
	main_routin()