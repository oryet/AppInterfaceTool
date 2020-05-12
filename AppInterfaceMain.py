# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from AppInterfaceTool.FrameProcess import *

__author__ = 'jiangzy'


if __name__ == '__main__':

    while (1):
        s = input("请输入报文: ")
        s = s.replace(' ', '')
        s = s.replace(':', '')
        s = s.replace(';', '')
        s = s.replace('：', '')
        s = s.replace('；', '')
        # print(s)
        at = frame_head_process(s)
        pt = idParsing(at)
        # print(at)
        # print(pt)
        for a in at:
            print(a, at[a])
        for a in pt:
            print(a, pt[a])


