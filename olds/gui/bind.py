import PySimpleGUI as sg

#レイアウト
layout= [
    [sg.InputText('表示させるテキストを入力してください',key='Input1'),
     sg.Button(button_text="入力", key='button1')],
    [sg.Multiline(key='OUTPUT', expand_x=True, expand_y=True)], #expandで表示エリアをWindowに追従させる
]

#window
window= sg.Window('bindの練習GUI', layout, finalize=True, resizable=True) #resizableでGUIサイズを可変にしておく

#windowへbindを設定
"""表示Windowが最前面でアクティブな時「CtrlとEnterを同時押し」すると「Enter1」というイベントを起こす"""
window.bind('<Control-Key-Return>', 'Enter1') #Enter2イベントと衝突しないようにあえてCtrlキーを混ぜてます

#部品へbindを設定 ※部品の場合はkeyに対してさらに機能をのせる感じに書く
"""テキスト入力エリアがアクティブな時に「Enterを押す」と「Enter2」というイベントを起こす"""
window['Input1'].bind("<Key-Return>", "Enter2")

while True:
    event, values= window.read()
    if event== sg.WINDOW_CLOSED:
        break

    elif event == "Enter1" or event == "button1": #Enter1イベント(Enterキー or 入力ボタンを押す)
        #"Enter1"のイベント時は黒でテキスト表示
        window['OUTPUT'].print(values['Input1'], colors='#000000') #表示エリアにprintさせる
        window['Input1'].update('') #入力領域をクリア

    elif event == "Input1" + "Enter2": #部品にバインドさせた場合は「＋」で元イベントと連結させる必要がある
        #"Enter2"のイベント時は赤でテキスト表示
        window['OUTPUT'].print(values['Input1'], colors='#ff0000')
        window['Input1'].update('') #入力領域をクリア

window.close()