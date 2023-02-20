import PySimpleGUI as sg

# グラフのサイズを設定
GRAPH_SIZE = (400, 400)

# グラフの描画内容を定義
graph = sg.Graph(GRAPH_SIZE, (0, 0), GRAPH_SIZE, background_color='white', key='graph')

# ウィンドウのレイアウトを定義
layout = [[graph]]

# ウィンドウを作成
window = sg.Window('Graph Window', layout, finalize=True)

# グラフを描画
graph.draw_line((0, 0), (200, 200), color='red')

# イベントループを開始
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

# ウィンドウを閉じる
window.close()
