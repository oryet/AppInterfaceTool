from PublicLib import public as pub

OOP_FULL_RATES = 4 + 1


def signed_hex_str2signed(d):
    if min(d.lower()) == 'f':
        return 0

    d = pub._strReverse(d)
    try:
        a = int(d, 16)
    except:
        a = 0
        print(signed_hex_str2signed.__name__, 'err')
    if a > 0x80000000:
        b = -(~a + 2)
        d = -0xffffffff + b
    else:
        d = a
    return d


def unsigned_hex_str2signed(d):
    if min(d.lower()) == 'f':
        return 0

    d = pub._strReverse(d)
    try:
        a = int(d, 16)
    except:
        a = 0
        print(unsigned_hex_str2signed.__name__, 'err')
    return a


def OOP_ENERGY(d):
    nNum = unsigned_hex_str2signed(d[:8])
    rsv = unsigned_hex_str2signed(d[8:16])
    n = 16
    step = 8
    nValue = []
    for i in range(OOP_FULL_RATES):
        nValue += [unsigned_hex_str2signed(d[(16 + i * step):(16 + step + i * step)])]
        n += step
    ld = [nNum, rsv, nValue]
    return n, ld


def OOP_HENERGY(d):
    nNum = unsigned_hex_str2signed(d[:8])
    rsv = unsigned_hex_str2signed(d[8:16])
    n = 16
    nValue = []
    step = 16
    for i in range(OOP_FULL_RATES):
        nValue += [unsigned_hex_str2signed(d[(16 + i * step):(16 + step + i * step)])]
        n += step
    ld = [nNum, rsv, nValue]
    return n, ld


def OOP_WORD4V(d):
    nNum = unsigned_hex_str2signed(d[:8])
    rsv = unsigned_hex_str2signed(d[8:16])
    n = 16
    nValue = []
    step = 4
    for i in range(4):
        nValue += [unsigned_hex_str2signed(d[(16 + i * step):(16 + step + i * step)])]
        n += step
    ld = [nNum, rsv, nValue]
    return n, ld


def OOP_INT4V(d):
    nNum = unsigned_hex_str2signed(d[:8])
    rsv = unsigned_hex_str2signed(d[8:16])
    n = 16
    nValue = []
    step = 8
    for i in range(4):
        nValue += [signed_hex_str2signed(d[(16 + i * step):(16 + step + i * step)])]
        n += step
    ld = [nNum, rsv, nValue]
    return n, ld


def OOP_LONG4V(d):
    nNum = unsigned_hex_str2signed(d[:8])
    rsv = unsigned_hex_str2signed(d[8:16])
    n = 16
    nValue = []
    step = 4
    for i in range(4):
        nValue += [unsigned_hex_str2signed(d[(16 + i * step):(16 + step + i * step)])]
        n += step
    ld = [nNum, rsv, nValue]
    return n, ld


#  define ID_OBJ_ENE01            (0x96000001) // 有功电量
def ID_OBJ_ENE01(d):
    l = []
    n = 0
    for i in range(3):
        rn, ld = OOP_ENERGY(d[n:])
        n += rn
        l += ld
    return l


#  define ID_OBJ_ENE02            (0x96000002) // 无功电量
def ID_OBJ_ENE02(d):
    l = []
    n = 0
    for i in range(6):
        rn, ld = OOP_ENERGY(d[n:])
        n += rn
        l += ld
    return l


#  define ID_OBJ_HENE01            (0x96000005) // 高精度有功电量
def ID_OBJ_HENE01(d):
    l = []
    n = 0
    for i in range(3):
        rn, ld = OOP_HENERGY(d[n:])
        n += rn
        l += ld
    return l


#  define ID_OBJ_HENE02            (0x96000006) // 高精度无功电量
def ID_OBJ_HENE02(d):
    l = []
    n = 0
    for i in range(6):
        rn, ld = OOP_HENERGY(d[n:])
        n += rn
        l += ld
    return l


#   define ID_OBJ_VAR01            (0x96000201) // 变量类数据
def VARIANT_01(d):
    l = []
    n = 0
    rn, ld = OOP_WORD4V(d[n:])  # 电压
    n += rn
    l += ld
    rn, ld = OOP_INT4V(d[n:])  # 电流
    n += rn
    l += ld
    # 零线电流
    l += [pub._strReverse(d[n:n + 8])]
    return l


#   define ID_OBJ_VAR03            (0x96000203) // 变量类数据
def VARIANT_03(d):
    l = []
    n = 0
    for i in range(3):
        rn, ld = OOP_INT4V(d[n:])  # 有功功率 无功功率 视在功率
        n += rn
        l += ld
    rn, ld = OOP_LONG4V(d[n:])  # 功率因素
    n += rn
    l += ld
    return l


if __name__ == '__main__':
    # d = '0400000000000000280c000085020000c4050000df03000004000000000000003affffffcbffffffdfffffff92ffffffffffffffffffffffffffffffffffffffffffffffffffffff0400000000000000e603e503e803e203'
    # d = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0500000000000000ab390000000000000000000000000000160000000000000080390000000000001400000000000000050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000050000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000050000000000000033b407000000000000000000000000004e7c020000000000b0300300000000003507020000000000'
    d = '0500000000000000d200010000000000635200001b820000542c000005000000000000000000000000000000000000000000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    l = ID_OBJ_ENE01(d)
    for b in l:
        if isinstance(b,list):
            for a in b:
                print(a)
        else:
            print(b)
