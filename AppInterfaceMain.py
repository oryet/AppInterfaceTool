# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from AppInterfaceTool.FrameProcess import *
from PyQt5.QtWidgets import QMainWindow
from AppInterfaceTool.AppTool import *



__author__ = 'jiangzy'




class mainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)
        # 将响应函数绑定到指定Button
        # self.pushButton.clicked.connect(self.showMessage)
        self.createActions()


    def createActions(self):
        self.pushButton.clicked.connect(self.buttonOn)


    # Button响应函数
    def showMessage(self):
        self.textEdit_show.setText('hello world')


    def buttonOn(self):
        # 获取输入文本框报文
        s = self.textEdit_in.toPlainText()

        # 解析
        at = frame_head_process(s)
        pt = idParsing(at)

        # 输出到显示文本框
        show = ''
        for a in at:
            show += str(a) + ':' + str(at[a])
            show += '\r\n'
        for a in pt:
            show += str(a) + ':' + str(pt[a])
            show += '\r\n'
        self.textEdit_show.setText(show)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_win = mainWin()
    main_win.show()
    sys.exit(app.exec_())
