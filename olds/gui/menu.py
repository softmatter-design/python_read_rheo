import PySimpleGUI as sg

menu_def = [
			['F&ile', 
			['&Open   Ctrl+o', 
    		'!&Save   Ctrl+s',
			'E&xit']
			],
			['&Sample', 
			['Sample', 
				'---',
				'&User', ['User &1', 'User &2']
			]
			],
			['&Help', ['&About...']]
			]
mytext = sg.Text('')
layout = [
	[sg.MenuBar(menu_def, key='-menu-')],
	[mytext]
]

window = sg.Window('メニューサンプル', layout, size=(200,100), finalize=True)
window.bind("<Control-o>", "_ctrl-o")
window.bind("<Control-s>", "_ctrl-s")
window.bind("<Control-e>", "_ctrl-e")
# イベントループ
while True:
	event, values = window.read()
	print(event)
	if event in [None, 'Exit']:
		break
	elif 'User 1' in event:
		mytext.update(value='User1')
	elif 'About' in event:
		mytext.update(value='About')
	elif '_ctrl-o' or 'Open' in event:
		mytext.update(value='Open')
	elif '_ctrl-s' or 'Save' in event:
		mytext.update(value='Save')
	

window.close()