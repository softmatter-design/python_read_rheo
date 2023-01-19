import PySimpleGUI as sg
import xlwings as xw
import pandas as pd

# GUIのテーマカラー
sg.change_look_and_feel('DarkAmber')

# 各項目のレイアウト
layout = [[sg.Text('ファイル選択'),
          sg.InputText('ファイルパス・名',key='-file-'),
          sg.FilesBrowse('ファイル読込', target='-file-', file_types=(('csv ファイル', '*.csv'),))],
          [sg.Button('実行',key='bt')]]


# ウィンドウ作成
window = sg.Window('csvファイルの入出力', layout)

# イベントループ
while True:
    event, values = window.read() #イベントの読み取り

    if event is None:   # ウィンドウ閉じるとき
        break

    # エクセルファイル処理関連
    elif event == 'bt':
        f = values['-file-'] # ファイルパスを取得

        if f != 'ファイルパス・名':
            # エクセルファイルのsheet1を読み込み
            sht = xw.Book(f).sheets['sheet1']
            # テーブルデータを読み込んだ後、転置して書き込む
            df = sht.range('A1').options(pd.DataFrame,header=False,index=False,expand='table').value
            sht.range('A1').value = df.T.values

            # ポップアップでメッセージ表示
            sg.popup('処理を実行しました')

        else:
            # ポップアップでメッセージ表示
            sg.popup('ファイル指定なし')

# 終了処理
window.close()