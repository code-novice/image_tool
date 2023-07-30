# Author: cp

import sys, time, logging
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPen, QPainter, QColor, QGuiApplication
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from easygui_xianshi import *
from ocr import ocr
from fanyi import fanyi
import keyboard
from threading import Thread, current_thread
import os
import easygui as gui


ocrInfo = None

class Screenshot(QWidget):
    """截图"""

    # 初始化变量
    # 初始化变量
    fullScreenImage = None
    captureImage = None
    isMousePressLeft = None
    beginPosition = None
    endPosition = None

    # 创建 QPainter 对象
    painter = QPainter()
    def __init__(self):
        super().__init__()
        self.initWindow()             # 初始化窗口
        self.captureFullScreen()      # 捕获全屏

    def initWindow(self):
        """初始化窗口"""
        self.setCursor(Qt.CrossCursor)               # 设置光标
        self.setWindowFlag(Qt.FramelessWindowHint)   # 产生无边框窗口，用户不能通过窗口系统移动或调整无边界窗口的大小
        self.setWindowState(Qt.WindowFullScreen)     # 窗口全屏无边框

    def captureFullScreen(self):
        """捕获全屏"""
        # 捕获当前屏幕，返回像素图
        self.fullScreenImage = QGuiApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        # 如果鼠标事件为左键，则记录起始鼠标光标相对于窗口的位置
        if event.button() == Qt.LeftButton:
            self.beginPosition = event.pos()
            self.isMousePressLeft = True
        # 如果鼠标事件为右键，如果已经截图了则重新开始截图，如果没有截图就退出
        if event.button() == Qt.RightButton:
            if self.captureImage is not None:
                self.captureImage = None
                self.update()    # 更新，会擦除之前的选框
            else:
                self.close()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.isMousePressLeft is True:
            self.endPosition = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.endPosition = event.pos()
        self.isMousePressLeft = False

    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        self.saveImage()
        self.close()

    def paintBackgroundImage(self):
        """绘制背景图"""
        # 填充颜色，黑色半透明
        fillColor = QColor(0, 0, 0, 100)
        # 加载显示捕获的图片到窗口
        self.painter.drawPixmap(0, 0, self.fullScreenImage)
        # 填充颜色到给定的矩形
        self.painter.fillRect(self.fullScreenImage.rect(), fillColor)

    def getRectangle(self, beginPoint, endPoint):
        """获取矩形选框"""
        # 计算矩形宽和高
        rectWidth = int(abs(beginPoint.x() - endPoint.x()))
        rectHeight = int(abs(beginPoint.y() - endPoint.y()))
        # 计算矩形左上角 x 和 y
        rectTopleftX = beginPoint.x() if beginPoint.x() < endPoint.x() else endPoint.x()
        rectTopleftY = beginPoint.y() if beginPoint.y() < endPoint.y() else endPoint.y()
        # 构造一个以（x，y）为左上角，给定宽度和高度的矩形
        pickRect = QRect(rectTopleftX, rectTopleftY, rectWidth, rectHeight)
        # 调试日志
        # logging.info('开始坐标：%s,%s', beginPoint.x(),beginPoint.y())
        # logging.info('结束坐标：%s,%s', endPoint.x(), endPoint.y())
        return pickRect

    def paintSelectBox(self):
        """绘制选框"""
        # 画笔颜色，蓝色
        penColor = QColor(30, 150, 255)  # 画笔颜色
        # 设置画笔属性，蓝色、2px大小、实线
        self.painter.setPen(QPen(penColor, 2, Qt.SolidLine))
        if self.isMousePressLeft is True:
            pickRect = self.getRectangle(self.beginPosition, self.endPosition)  # 获得要截图的矩形框
            self.captureImage = self.fullScreenImage.copy(pickRect)             # 捕获截图矩形框内的图片
            self.painter.drawPixmap(pickRect.topLeft(), self.captureImage)      # 填充截图的图片
            self.painter.drawRect(pickRect)     # 绘制矩形边框

    def paintEvent(self,event):
        """接收绘制事件开始绘制"""
        self.painter.begin(self)        # 开始绘制
        self.paintBackgroundImage()     # 绘制背景
        self.paintSelectBox()           # 绘制选框
        self.painter.end()              # 结束绘制

    def saveImage(self):
        """保存图片"""
        # 获取用户选择的文件名的完整路径
        fileName = '1.png' #QFileDialog.getSaveFileName(self, '保存图片', time.strftime("%Y%m%d%H%M%S"), ".png")
        # 保存用户选择的文件。如果选取了区域，就保存区域图片；如果没有选取区域，就保存全屏图片
        if self.captureImage is not None:
            self.captureImage.save(fileName)
        else:
            self.fullScreenImage.save(fileName)

        #ocr()

    def keyPressEvent(self, event):
        """按键事件"""
        # 如果按下 ESC 键，则退出截图
        if event.key() == Qt.Key_Escape:
            self.close()
        # 如果按下 Enter 键，并且已经选取了区域，就截图选区图片
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.captureImage is not None:
                self.saveImage()
                self.close()

def get_buttonInfo(info):
    global ocrInfo
    info = ocrInfo
    if info == '继续':
        if configInfo[0] == '1':
            ScreenshotFunction()
            ret = '截图已完成'
        if configInfo[1] == '1':
            ret = ocr()
        if configInfo[2] == '1':
            ret = fanyi(ret, configInfo[3], configInfo[4])
    elif info == '配置信息':
        ret = config()
        print(ret)
    elif info == '关闭' or info == None:
        os._exit(0)

    ocrInfo = get_text(ret)

def ScreenshotFunction():
    app = QApplication(sys.argv)    # 创建 QApplication 对象
    windows = Screenshot()          # 创建 Screenshot 对象
    windows.setWindowFlag(Qt.WindowStaysOnTopHint, True) #设置 "AlwaysOnTop" 标志
    windows.show()                  # 显示窗口
    app.exec_()          # 进入主事件循环并等待直到 exit() 被调用

def OcrRun():
    global ocrInfo
    while True:
        if ocrInfo != '快捷':
            time.sleep(0.5)
            get_buttonInfo(ocrInfo)
            #print('主循环')
        else:
            time.sleep(0.5)
            #print('快捷按键', ocrInfo)

def on_key_pressed(event):
    global ocrInfo
    #print('开始监听')
    if event.event_type == 'down' and event.name == 's' and keyboard.is_pressed('ctrl'):
        #print('按键成功')
        gui.ObjectClose()
        while True:
            if ocrInfo == '快捷':
                ocrInfo = '继续'
                break

def key_envt():
    keyboard.on_press(on_key_pressed)
    keyboard.wait('esc')
    #print('监听结束')


thread01 = Thread(target=key_envt)
thread01.setDaemon(True)
thread01.start()
text = '配置已完成: ' + configInfo[0] + configInfo[1] + configInfo[2] + '\n翻译配置:' + configInfo[3] + '---->' + configInfo[4]
ocrInfo = get_text(text)
OcrRun()




'''
if __name__ == '__main__':
    # 调试日志
    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    # sh = logging.StreamHandler()
    # formatter = logging.Formatter('%(message)s')
    # sh.setFormatter(formatter)
    # logger.addHandler(sh)

    thread01 = Thread(target=key_envt)
    thread01.start()
    ocrInfo = get_text('')
    while True:
        if ocrInfo != ' ':
            print('正常循环中 ！！！', ocrInfo)
            get_buttonInfo(ocrInfo)

'''
