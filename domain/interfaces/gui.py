from wsgiref import validate
import PySimpleGUI as sg
import datetime
import sys

class GUI:
    def validate(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except:
            return None

        return date_text

    def display_gui(self):
        input = {}

        sg.theme('DarkAmber')   # デザインテーマの設定

        # ウィンドウに配置するコンポーネント
        layout = [  [sg.Text('code'), sg.InputText()],
                    [sg.Text('注文日のはじめ (yyyy-mm-dd)'), sg.InputText()],
                    [sg.Text('注文日のおわり (yyyy-mm-dd)'), sg.InputText()],
                    [sg.Text('出力ファイルパス'), sg.InputText()],
                    [sg.Button('実行'), sg.Button('キャンセル')] ]

        # ウィンドウの生成
        window = sg.Window('入力画面', layout)

        # イベントループ
        while True:
            event, values = window.read()
            if event == '実行':
                input['code'] = values[0]
                input['start'] = (values[1])
                input['end'] = (values[2])
                input['filepath'] = (values[3])
                window.close()
                break
            if event == 'キャンセル':
                window.close()
                sys.exit()

        return input