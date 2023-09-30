import math
import numpy as np

def rect(x):
    if np.abs(x) <= 0.5:
        return 1
    return 0

def azi_W(fa, fdi, prf, dop, bw, wgt = 0.15):
    """
    方位向滤波
    :param fa: 频率, 可变量
    :param fdi: 影像多普勒中心频率
    :param prf: 脉冲重复频率, 也是方位向采用频率
    :param dop: 多普勒带宽
    :param bw: 方位向带宽
    :param wgt: 加权系数
    """
    return (wgt + (1-wgt)*np.cos(2 * np.pi * (fa - fdi)/prf)) * (np.sinc((fa - dop)/prf))^2 * rect((fa-fdi)/bw)

def azi_filter(fa, fd1, fd2, prf, dop, bw, wgt = 0.15):
    
    # wgt + (1-wgt)*np.cos(2 * math.pi * (fa - fd))
    pass