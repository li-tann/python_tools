import osgeo.gdal as gdal
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, ifft

N = 64                        # 采样点数
sample_freq=120                 # 采样频率 120 Hz, 大于两倍的最高频率
sample_interval=1/sample_freq   # 采样间隔
signal_len=N*sample_interval    # 信号长度
t=np.arange(0,signal_len,sample_interval)

signal = 5 + 2 * np.sin(2 * np.pi * 20 * t) + 3 * np.sin(2 * np.pi * 30 * t) + 4 * np.sin(2 * np.pi * 40 * t)  # 采集的信号
print('len(signal)', len(signal))
fft_data = fft(signal)
print('len(fft_data)', len(fft_data))
# 在python的计算方式中，fft结果的直接取模和真实信号的幅值不一样。
# 对于非直流量的频率，直接取模幅值会扩大N/2倍， 所以需要除了N乘以2。
# 对于直流量的频率(0Hz)，直接取模幅值会扩大N倍，所以需要除了N。
fft_amp0 = np.array(np.abs(fft_data)/N*2)   # 用于计算双边谱
fft_amp0[0]=0.5*fft_amp0[0]
N_2 = int(N/2)
fft_amp1 = fft_amp0[0:N_2]  # 单边谱
fft_amp0_shift = fftshift(fft_amp0)    # 使用fftshift将信号的零频移动到中间

# 计算频谱的频率轴
list0 = np.array(range(0, N))
list1 = np.array(range(0, int(N/2)))
list0_shift = np.array(range(0, N))
freq0 = sample_freq*list0/N        # 双边谱的频率轴
freq1 = sample_freq*list1/N        # 单边谱的频率轴
freq0_shift=sample_freq*list0_shift/N-sample_freq/2  # 零频移动后的频率轴

# 绘制结果
plt.figure()
# 原信号
plt.subplot(221)
plt.plot(t, signal)
plt.title(' Original signal')
plt.xlabel('t (s)')
plt.ylabel(' Amplitude ')
# 双边谱
plt.subplot(222)
plt.plot(freq0, fft_amp0)
plt.title(' spectrum two-sided')
plt.ylim(0, 6)
plt.xlabel('frequency  (Hz)')
plt.ylabel(' Amplitude ')
# 单边谱
plt.subplot(223)
plt.plot(freq1, fft_amp1)
plt.title(' spectrum single-sided')
plt.ylim(0, 6)
plt.xlabel('frequency  (Hz)')
plt.ylabel(' Amplitude ')
# 移动零频后的双边谱
plt.subplot(224)
plt.plot(freq0_shift, fft_amp0_shift)
plt.title(' spectrum two-sided shifted')
plt.xlabel('frequency  (Hz)')
plt.ylabel(' Amplitude ')
plt.ylim(0, 6)

plt.show()
