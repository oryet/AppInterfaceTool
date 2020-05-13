

# 0000H：通用消息接口
def CommInterface(iop, at):
    # 0001H：紧急停电（事件）
    # 0002H：系统停电（事件）
    # 0003H：系统复位（事件）
    # 0004H：系统上电（事件）
    # 0005H：系统校时（事件）
    # 0010H：心跳检测
    # 0011H：执行维护命令
    # 0012H：透明传输
    # 0013H：版本信息
    # 0014H：错误信息
    if iop == '0001':  # 0001H：紧急停电（事件）
        pass
    elif iop == '0002':  # 0002H：系统停电（事件）
        pass
    elif iop == '0003':  # 0003H：系统复位（事件）
        pass
    elif iop == '0004':  # 0004H：系统上电（事件）
        pass
    elif iop == '0005':  # 0005H：系统校时（事件）
        pass
    elif iop == '0010':  # 0010H：心跳检测
        pass
    elif iop == '0011':  # 0011H：执行维护命令
        pass
    elif iop == '0012':  # 0012H：透明传输
        pass
    elif iop == '0013':  # 0013H：版本信息
        pass
    elif iop == '0014':  # 0014H：错误信息
        pass

    return {}