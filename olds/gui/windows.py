import PySimpleGUI as sg

def mainwindow():
	# ------------ メインウィンドウ作成 ------------
	main_layout = [
					[sg.Text('読み取り対象のファイルを指定してください')],
					[sg.Text('ファイル選択'),sg.InputText('ファイルパス・名',key='-file-'),
			sg.FilesBrowse('ファイル読込', target='-file-', file_types=(('csv ファイル', '*.csv'),))],
					[sg.Button("Move to 2nd", key='move2'), sg.Button("Move to 3rd", key='move3')],
           			[sg.Button("Exit", key='exit')]
					]
	return sg.Window("Main Window", main_layout, finalize=True)

def secondw():
	# ------------ サブウィンドウ作成 ------------
	sub_layout1 = [
					[sg.Text("This is 2nd Window !")],
					[sg.Button("Return Main", key='return_m')],
					[sg.Button("Move to 3rd", key='move3')],
					[sg.Button("Exit", key='exit')]
					]
	return sg.Window("2nd Window", sub_layout1, finalize=True)

def thirdw():
	# ------------ サブウィンドウ作成 ------------
	sub_layout2 = [
					[sg.Text("This is 3rd Window !")],
					[sg.Button("Return Main", key='return_m')],
					[sg.Button("Move to 2nd", key='move2')],
					[sg.Button("Exit", key='exit')]
					]
	return sg.Window("3rd Window", sub_layout2, finalize=True)

def main_routin():
	# 最初に表示するウィンドウを指定する。
	window = mainwindow()

	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED or event == "exit":
			break

		# "Move to 2nd"ボタンが押された場合
		elif event == "move2":
			# メインウィンドウを閉じて、サブウィンドウを作成して表示する
			window.close()
			window = secondw()
		
		# "Move to 3rd"ボタンが押された場合
		elif event == "move3":
			# メインウィンドウを閉じて、サブウィンドウを作成して表示する
			window.close()
			window = thirdw()

		# Closeボタンが押された場合
		elif event == "return_m":
			# サブウィンドウを閉じて、メインウィンドウを作成して表示する
			window.close()
			window = mainwindow()

	# ウィンドウを終了する
	window.close()

if __name__ == '__main__':
	main_routin()