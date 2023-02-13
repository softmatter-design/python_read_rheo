import PySimpleGUI as sg

sg.theme('SystemDefault')
menu_def = [
    ['&Sample', ['Sample &1::sample1key', '!Sample &2::sample2key']],
    ['&Help', ['&About...::aboutkey']]
]
mytext = sg.Text('', font=('Noto Serif CJK JP',30))
layout = [
    [sg.Menu(menu_def)],
    [mytext]
]

window = sg.Window('メニューサンプル', layout, size=(200,100))
# イベントループ
while True:
    event, values = window.read()
    print(event,values)
    if event is not None and event.endswith('sample1key'):
        mytext.update(value='Sample1')
    if event is not None and event.endswith('sample2key'):
        mytext.update(value='Sample2')
    if event is not None and event.endswith('aboutkey'):
        mytext.update(value='About')
    if event == sg.WIN_CLOSED:
        break

window.close()