#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


# グラフツールバーを呼び出すクラス
class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

def set_scale(scale):

    root = sg.tk.Tk()
    root.tk.call('tk', 'scaling', scale)
    root.destroy()

# figureを作成する関数
def draw_plot():
    fig = plt.figure()
    set_scale(fig.dpi/72)
    
    ax = fig.add_subplot()
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.random.rand(len(x))
    ax.plot(x, y, label='sin(x)')
    ax.set_xlabel('x value')
    ax.set_ylabel('y value')

    return fig

# グラフとツールバーをgui window上のcanvasに描画する関数
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    # 更新処理がされた時に一旦グラフを消去する
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    # 一旦ツールバーを消去する
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    # ここで実際にgui上に書きこむ処理をする
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='left', fill='both', expand=2)


# gui上のツールバーを描画するcanvasを定義
figure_canvas_control = [sg.Canvas(key='controls_cv')]

# gui上のfigureを描画するcanvasを定義
figure_canvas = [sg.Canvas(key='fig_cv',
                           # ! サイズを確保しておく。
                           size=(400 * 2, 400))]

# レイアウトを定義
layout = [
    [sg.Button('Plot'), sg.Cancel(), sg.Button('Popup')],
    [sg.T('Controls:')],
    figure_canvas_control,
    [sg.T('Figure:')],
    figure_canvas
]

# windowを作成
window = sg.Window('matplotlib graph', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Plot':
        # windowに書きこむfigureを作成して受け取り
        drawing_fig = draw_plot()
        # windowに当てはめる処理をする
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas,
                              drawing_fig,
                              window['controls_cv'].TKCanvas)

    elif event == 'Popup':
        sg.popup('still running')

window.close()