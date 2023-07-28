import easygui as gui
#from jietu import ScreenshotFunction
#from ocr import ocr
#from fanyi import fanyi
import time
import sys

configInfo = ['1', '1', '1']

'''
def get_buttonInfo(info):
    if info == '继续':
        if configInfo[0] == '1':
            ScreenshotFunction()
            ret = '截图已完成'
        if configInfo[1] == '1':
            ret = ocr()
        if configInfo[2] == '1':
            ret = fanyi(ret)

        get_text(ret)
    elif info == '配置信息':
        config()
'''

def config():
    global configInfo
    messgage = ['截图', 'ocr', '翻译']
    ret = gui.multenterbox('需要的功能填写1即可：', '配置功能', messgage)
    configInfo = ret


def get_text(text):
    print('text', text)
    ret = gui.buttonbox(text, "ocr", choices=('继续', '配置信息', '关闭'))
    return ret
        #get_buttonInfo(ret)


if __name__ == '__main__':
    get_text('')