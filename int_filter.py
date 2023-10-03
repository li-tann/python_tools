import math
import numpy as np

def rect(x):
    if np.abs(x) <= 0.5:
        return 1
    return 0

def hamming_wgt_inv_rg(fr, fs, br, wgt):
    """
    距离向的反hamming加权函数
    :param fr: 斜距频率, 可变量, 数组?
    :param fs: 距离向采样频率
    :param br: 距离向带宽
    :param wgt: 加权系数
    """
    return rect(fr/br) / (wgt + (1-wgt)* np.cos(2*np.pi * fr / fs))

def hamming_wgt_rg(fr, dfr, br, ms, wgt):
    """
    距离向的反hamming加权函数
    :param fr: 斜距频率, 可变量, 数组?
    :param dfr: delta_fr, 距离向频谱偏移
    :param br: 距离向带宽
    :param ms: 表示影像的主辅, 主为mas 辅为sla
    :param wgt: 加权系数
    """

    k = -1
    if ms == "sla":
        k = 1
    b = (fr - k/2*np.abs(dfr))/(br-np.abs(dfr))
    return (wgt + (1-wgt)* np.cos(2*np.pi* b))*rect(b)

def filter_slant_range(fr, fs, dfr, br, ms, wgt):
    return hamming_wgt_inv_rg(fr, fs, br, wgt) * hamming_wgt_rg(fr, dfr, br, ms, wgt)


def wgt_azi(fa, fdi, prf, fdop, bw, wgt):
    """
    方位向滤波
    :param fa: 频率, 可变量
    :param fdi: 影像多普勒中心频率
    :param prf: 脉冲重复频率, 也是方位向采用频率
    :param dop: 多普勒带宽
    :param bw: 方位向带宽
    :param wgt: 加权系数
    """
    fa_fdi = fa - fdi
    return (wgt + (1-wgt)*np.cos(2 * np.pi * fa_fdi/prf)) * (np.sinc(fa_fdi/fdop))^2 * rect(fa_fdi/bw)

def pai(fa, Bac):
    if np.abs(fa) <=  np.abs(Bac):
        return 1
    return 0

def filter_azimuth(fa, fd1, fd2, prf, dop, bw, ms, wgt):
    delta_fd = fd1-fd2
    Bac = bw - np.abs(delta_fd)
    if ms == "sla":
        return np.sqrt(wgt_azi(fa-fd2)/wgt_azi(fa-fd1)) * pai(fa,Bac)
    else:
        return np.sqrt(wgt_azi(fa-fd1)/wgt_azi(fa-fd2)) * pai(fa,Bac)