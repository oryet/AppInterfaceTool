from PublicLib import public as pub


# 0001H：系统管理器消息接口
def SysInterface(iop, at):
    # 0001H：以太网插拔（事件）
    # 0010H：App请求注册
    # 0011H：App取消注册
    # 0012H：查询已注册App
    # 0013H：查询指定App信息
    # 0020H：事件订阅
    # 0021H：事件取消订阅
    # 0022H：查询订阅的事件信息
    # 0030H：请求系统重启
    # 0031H：查询电源状态
    # 0032H：查询以太网插拔状态
    # 0035H：配置本机IP地址
    # 0036H：添加路由表
    # 0037H：删除路由表
    # 0038H：时钟同步
    # 0039H：启动SNTP对时
    # 003AH：获取设备信息
    # 003BH：执行system命令
    # 003CH：获取容器信息
    # 003DH：获取容器内App信息

    ret = {}
    if iop == '0001':  # 0001H：以太网插拔（事件）
        pass
    elif iop == '0010':  # 0010H：App请求注册
        ret = fn0010(at['Payload'])
    elif iop == '0011':  # 0011H：App取消注册
        pass
    elif iop == '0012':  # 0012H：查询已注册App
        pass
    elif iop == '0013':  # 0013H：查询指定App信息
        pass
    elif iop == '0020':  # 0020H：事件订阅
        pass
    elif iop == '0021':  # 0021H：事件取消订阅
        pass
    elif iop == '0022':  # 0022H：查询订阅的事件信息
        pass
    elif iop == '0030':  # 0030H：请求系统重启
        pass
    elif iop == '0031':  # 0031H：查询电源状态
        pass
    elif iop == '0031':  # 0031H：查询电源状态
        pass
    elif iop == '0032':  # 0032H：查询以太网插拔状态
        pass
    elif iop == '0035':  # 0035H：配置本机IP地址
        pass
    elif iop == '0037':  # 0037H：删除路由表
        pass
    elif iop == '0038':  # 0038H：时钟同步
        pass
    elif iop == '0039':  # 0039H：启动SNTP对时
        pass
    elif iop == '003A':  # 003AH：获取设备信息
        pass
    elif iop == '003B':  # 003BH：执行system命令
        pass
    elif iop == '003C':  # 003CH：获取容器信息
        pass
    elif iop == '003D':  # 003DH：获取容器内App信息
        pass

    return ret


def fn0010(Payload):
    # MQT_PLUGIN ∷= SEQUENCE
    # {
    # 	组件名称		visible-string，
    # 	订阅事件		SEQUENCE OF double-long-unsigned，
    # 	版本信息		double-long-unsigned，
    # 	发布日期		date_time_s
    # }
    # REQ ∷= SEQUENCE
    # {
    # 	进程号		double-long，
    # 	组件信息		MQT_PLUGIN
    # }
    # ACK ∷= bool
    ProcessNum = Payload[:8]
    Payload = Payload[8:]

    n = int(Payload[:2], 16)
    n = (n + 1) * 2
    b = bytes.fromhex(Payload[2:n])
    ComponentName = str(b, encoding="utf-8")
    Payload = Payload[n:]

    SubEvents = Payload[:2]
    Payload = Payload[2:]

    Version = Payload[:8]
    Payload = Payload[8:]

    ReleaseDate = dateformate(Payload)

    st = {'进程号': ProcessNum, '组件名称':ComponentName, '订阅事件':SubEvents, '版本信息':Version, '发布日期':ReleaseDate}

    return st


import time
def dateformate(date):
    year = int(date[:4], 16)
    mon = int(date[4:6], 16)
    day = int(date[6:8], 16)
    hour = int(date[8:10], 16)
    min = int(date[10:12], 16)
    sec = int(date[12:14], 16)

    # 转标准时间格式
    # str(year) + str(mon) + str(day) + str(hour) + str(min) + str(sec)
    # ctime = time.struct_time(tm_year=year, tm_mon=mon, tm_mday=day, tm_hour=hour, tm_min=min, tm_sec=sec)
    timestamp = time.mktime((year, mon, day, hour, min, sec, 0, 0, 0))

    # 转换成localtime
    time_local = time.localtime(timestamp)

    # 转换成新的时间格式(2016-05-05 20:28:54)
    stime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    return stime

if __name__ == '__main__':
    t = '07E30903000000'
    st = dateformate(t)
