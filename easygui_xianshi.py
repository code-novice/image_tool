import easygui as gui
#from jietu import ScreenshotFunction
#from ocr import ocr
#from fanyi import fanyi
import time
import sys

configInfo = ['1', '0', '0', 'auto', 'zh']
languagesInfo = {'自动检测':'auto', '中文':'zh', '英文':'en', '日文':'jp', '粤语':'yue', '文言文':'wyw', '韩语':'kor', '法语':'fra', '西班牙语':'spa', '阿拉伯语':'ara', '俄语':'ru'
                 , '意大利语':'it', '荷兰语':'nl', '希腊语':'el', '越南语':'vie'}

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
    ret_in = configInfo[3]
    ret_out = configInfo[4]
    messgage = ['截图', 'ocr', '翻译']
    languages_in = ['自动检测', '中文', '英文', '日文', '粤语', '文言文', '韩语', '法语', '西班牙语', '阿拉伯语', '俄语', '意大利语', '荷兰语', '希腊语', '越南语']
    languages_out = ['中文', '英文', '日文', '粤语', '文言文', '韩语', '法语', '西班牙语', '阿拉伯语',
                    '俄语', '意大利语', '荷兰语', '希腊语', '越南语']
    ret = gui.multenterbox('需要的功能填写1即可：', '配置功能', messgage)

    if ret == None:
        return '配置已取消: ' + configInfo[0] + configInfo[1] + configInfo[2]
    elif '' in ret:
        return '配置信息有误'
    else:
        configInfo[0] = ret[0]
        configInfo[1] = ret[1]
        configInfo[2] = ret[2]

    ret_in = gui.choicebox('设置需要被翻译语言语种:', '翻译语言设置', languages_in)
    if ret_in != None:

        ret_out = gui.choicebox('设置需要到什么语言语种:', '翻译语言设置', languages_out)



    if ret_in == None or ret_out == None:
        return '翻译配置已取消: ' + configInfo[3] + '---->' + configInfo[4]
    else:
        configInfo[3] = languagesInfo[ret_in]
        configInfo[4] = languagesInfo[ret_out]
    print(configInfo[3], configInfo[4])
    return '配置已完成: ' + configInfo[0] + configInfo[1] + configInfo[2] + '\n翻译配置:' + configInfo[3] + '---->' + configInfo[4]

def get_text(text):
    ret = gui.buttonbox(text, "ocr", choices=('继续', '配置信息', '关闭'))
    return ret
        #get_buttonInfo(ret)


if __name__ == '__main__':
    config()