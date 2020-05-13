# -*- coding: utf-8 -*-
import sys

sys.path.append('../')
from PublicLib import public as pub
from AppInterfaceTool.Interface.CollectionTaskSchedulingInterface import *
from AppInterfaceTool.Interface.CommonInterface import *
from AppInterfaceTool.Interface.DataCenterInterface import *
from AppInterfaceTool.Interface.DeskTopInterface import *
from AppInterfaceTool.Interface.DialingModuleInterface import *
from AppInterfaceTool.Interface.MeterReadingModuleInterface import *
from AppInterfaceTool.Interface.ModuleManagerInterface import *
from AppInterfaceTool.Interface.SafetyMonitoringInterface import *
from AppInterfaceTool.Interface.SystemInterface import *



def idParsing(at):
    idd = at['TAG'][:4]
    iop = at['TAG'][4:8]

    ret = {}

    if idd == '0000':  # 0000H：通用消息接口
        ret = CommInterface(iop, at)
    elif idd == '0001':  # 0001H：系统管理器消息接口
        ret = SysInterface(iop, at)
    elif idd == '0002':  # 0002H：无线模块拨号管理App消息接口
        ret = DialingInterface(iop, at)
    elif idd == '0003':  # 0003H：本地抄表模块管理App消息接口
        ret = MeterReadingInterface(iop, at)
    elif idd == '0004':  # 0004H：模组管理器消息接口
        ret = ModuleManagerInterface(iop, at)
    elif idd == '0005':  # 0005H：数据中心消息接口
        ret = DataCenterInterface(iop, at)
    elif idd == '0006':  # 0006H：安全在线监测消息接口
        ret = SafetyMonitoringInterface(iop, at)
    elif idd == '0007':  # 0007H：桌面消息接口
        ret = DeskTopInterface(iop, at)
    elif idd == '1003':  # 1003H：采集任务调度管理消息接口
        ret = CollectionTaskSchedulingInterface(iop, at)

    return ret


def frame_head_process(s):
    at = {'PRIORITY': 0,
          'PRM': 0,
          'INDEX': 0,
          'LABEL': 0,
          'SOURCE': '',
          'DESTINATION': '',
          'TAG': 0,
          'Length': 0,
          'Payload': ''
          }

    s = s.replace(' ', '')
    s = s.replace(':', '')
    s = s.replace(';', '')
    s = s.replace('：', '')
    s = s.replace('；', '')

    if len(s) < 16:
        at['err'] = 'frame len error'
        return at
    # PRIORITY  PRM 1
    # 优先级（数值越小优先级越高，0为最高优先级）
    # 启动标志位（PRM=1，表示启动）
    priprm = int(s[:2], 16)
    at['PRM'] = priprm & 0x01
    at['PRIORITY'] = priprm >> 1
    s = s[2:]

    # INDEX 2
    # 消息序号（从0循环递增，响应消息同请求消息保持一致）
    at['INDEX'] = int(pub._strReverse(s[:4]), 16)
    s = s[4:]

    # LABEL 2
    # 消息标签（发送方附加标签，响应时带回）
    at['LABEL'] = int(pub._strReverse(s[:4]), 16)
    s = s[4:]

    # SOURCE N
    # 消息发送方名称，字符串，以0结尾，命名规范见5.2
    end_source = s.find('00')
    if end_source > 0:
        b = bytes.fromhex(s[:end_source])
        at['SOURCE'] = str(b, encoding="utf-8")
    else:
        at['err'] = 'SOURCE err'
        return at
    s = s[(end_source + 2):]

    # DESTINATION N
    # 消息接收方名称，字符串，以0结尾，命名规范见5.2
    end_dest = s.find('00')
    if end_dest > 0:
        b = bytes.fromhex(s[:end_dest])
        at['DESTINATION'] = str(b, encoding="utf-8")
    else:
        at['err'] = 'DESTINATION err'
        return at
    s = s[(end_dest + 2):]

    if len(s) < 8:
        at['err'] = 'TAG len error'
        return at
    # MSG’s—TAG 4
    # 消息接口ID（消息接口定义见第7章）
    at['TAG'] = pub._strReverse(s[:8])
    s = s[8:]

    if len(s) < 2:
        at['err'] = 'Length error'
        return at
    # MSG’s—Length  N
    # 消息有效载荷长度，采用可变长度编码（A-XDR）
    l = int(s[:2], 16)
    if l & 0x80:
        ln = l & 0x7F
        ln = ln * 2 + 2
        try:
            at['Length'] = int(s[2:ln], 16)
        except:
            at['Length'] = 0
    else:
        ln = 2
        at['Length'] = l
    s = s[ln:]

    if len(s) != at['Length'] * 2:
        at['err'] = 'Payload Length error'

    # MSG’s—Payload N
    # 有效载荷，即消息数据单元（定义见附录）
    at['Payload'] = s

    return at


if __name__ == '__main__':
    s = '51 34 12 00 F0 49 2D 6D 79 41 70 70 31 00 49 2D 73 6D 69 4F 53 00 10 00 01 00 19 00 00 00 03 08 49 2D 6D 79 41 70 70 31 00 00 00 00 01 07 E3 09 03 00 00 00'
    s = s.replace(' ', '')

    # 01 								# 优先级 = 0，PRM = 1
    # 00 00 							# 序号 = 0
    # 00 00 							# 消息标签 = 0
    # 49 2D 6D 79 41 70 70 31 00 		# 消息发送者 = I-myApp1
    # 49 2D 73 6D 69 4F 53 00			# 消息接收者 = I-smiOS（系统管理器）
    # 10 00 01 00 						# MSG’s TAG = 00010010（请求注册）
    # 19 								# MSG’s Length = 25
    # 									# MSG’s Payload
    # 00 00 00 03 						# 进程号 = 00000003
    # 08 49 2D 6D 79 41 70 70 31		# 组件名称 = I-myApp1
    # 00 								# 订阅事件（未订阅任何事件）
    # 00 00 00 01 						# 版本信息 = 00000001
    # 07 E3 09 03 00 00 00				# 发布日期 = 2019年9月3日 00:00:00

    s = s.replace(' ', '')
    s = s.replace(':', '')
    s = s.replace(';', '')
    s = s.replace('：', '')
    s = s.replace('；', '')
    # print(s)
    at = frame_head_process(s)
    pt = idParsing(at)
    print(at)
    print(pt)
