"""
Matplotlibのグラフを別Winodwで表示

"""
import numpy as np
import matplotlib.pyplot as plt

import PySimpleGUI as sg

def make_data_fig(make=True):
    fig = plt.figure()

    if make:
        # x = np.linspace(0, 2*np.pi, 500)
        x = np.arange(0, 2*np.pi, 0.05*np.pi)
        ax = fig.add_subplot(111)
        ax.plot(x, np.sin(x))
        return fig

    else:
        return fig


def draw_plot(fig):

    plt.show(block=False)
    # block=Falseに指定。これが重要
    # コンソールは何も入力を受け付けなくなり、GUI を閉じないと作業復帰できない。

def del_plot(fig):

    # plt.cla(): Axesをクリア
    # plt.clf(): figureをクリア
    # plt.close(): プロットを表示するためにポップアップしたウィンドウをクローズ

    plt.close()


sg.theme('Light Blue 2')

layout = [[sg.Text('Graph Diasplay')],
          [sg.Button('Display',key='-display-'), sg.Button('clear',key='-clear-'), sg.Cancel()]
          ]

window = sg.Window('Plot', layout, location=(100, 100), finalize=True)

while True:
    event, values = window.read()

    if event in (None, 'Cancel'):
        break

    elif event == '-display-':
        fig_ = make_data_fig(make=True)
        draw_plot(fig_)

    elif event == '-clear-':
        del_plot(fig_)

window.close()