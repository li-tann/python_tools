import osgeo.gdal as gdal
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, ifft

print(gdal.__version__)

def print_array_info(array, name='array'):
    """
    打印nparray的基本信息
    :param array: 数组
    :param name: 数组名称
    """
    print('''{}.info:
      dim:{}
      shape:{}
      size:{}
      dtype:{}'''.format(name,array.ndim, array.shape, array.size, array.dtype))
    
def coh_map(array_a, array_b):
    """
    计算两个nparray数组的相干性
    """
    size_a = np.size(array_a,0)
    size_b = np.size(array_b,0)
    size_min = min(size_a, size_b)
    array_coh = np.zeros(size_min)
    for i in range(size_min):
         
        sum_z = sum_m1 = sum_m2 = num = 0
        for k in range(7):
            j = k - 3
            if(i+j<0 or i+j >= size_min):
                continue
            re1 = np.real(array_a[i+j])
            im1 = np.imag(array_a[i+j])
            re2 = np.real(array_b[i+j])
            im2 = np.imag(array_b[i+j])              
            sum_z += np.sqrt(re1*re1+im1*im1) * np.sqrt(re2*re2+im2*im2)
            sum_m1 += re1*re1+im1*im1
            sum_m2 += re2*re2+im2*im2

        array_coh[i]=sum_z/np.sqrt(sum_m1)/np.sqrt(sum_m2)
        # if(array_coh[i] > 1):
        #     array_coh[i] = 1
    
    '''coh_stat: 统计相干性 纵轴单位是百分比'''
    coh_stat = np.zeros(100)
    for c in array_coh:
        k = int(c*100)
        if k<0:
            k=0
        if k >=100:
            k=99
        coh_stat[k] = coh_stat[k] + 1
    coh_stat = coh_stat / np.size(array_coh,0)
    return array_coh, coh_stat  

'''thinkbook'''
path_mas = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\master.rslc.vrt"
path_sla = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\slave.rslc.vrt"
'''legion'''
# path_mas = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\master.rslc.vrt"
# path_sla = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\slave.rslc.vrt"
gdal.UseExceptions()

'''打开栅格数据'''
try:
    ds_mas: gdal.Dataset=gdal.Open(path_mas)
except RuntimeError as e:
    print( 'Unable to open %s'% path_mas)
    sys.exit(1)

cols = ds_mas.RasterXSize#图像长度
rows = (ds_mas.RasterYSize)#图像宽度
data_mas = ds_mas.ReadAsArray(0, 0, cols, rows)#转为numpy格式

rb: gdal.Band= ds_mas.GetRasterBand(1)
datatype = rb.DataType

try:
    ds_sla: gdal.Dataset=gdal.Open(path_sla)
except RuntimeError as e:
    print( 'Unable to open %s'% path_sla)
    sys.exit(1)

if(cols != ds_sla.RasterXSize or rows != ds_sla.RasterYSize):
    print("diff size about mas({},{}) & sla({},{})".format(rows,cols,ds_sla.RasterYSize,ds_sla.RasterXSize))
    sys.exit(1)

data_sla = ds_sla.ReadAsArray(0, 0, cols, rows)#转为numpy格式

print('''dataset.info:
      cols:{}
      rows:{}
      datatype:{}'''.format(cols, rows, gdal.GetDataTypeName(datatype)))


print_array_info(data_mas,'data_mas')
print_array_info(data_sla,'data_sla')

xcol = np.linspace(0,cols,cols)
# xcol = np.linspace(0,rows,rows)

xcol_shift = xcol - np.size(xcol,0)/2

'''距离向取一行'''
sp_mas = data_mas[int(rows/2)]
sp_sla = data_sla[int(rows/2)]
'''方位向去取一列'''
# sp_mas = data_mas[:,int(cols/2)].T
# sp_sla = data_sla[:,int(cols/2)].T

# print(sp_sla[0])
# print(sp_sla[0].conjugate())
intf = sp_mas * np.conj(sp_sla)
[coh,coh_stat] = coh_map(sp_mas, sp_sla)
coh_stat_index = np.linspace(0,1,100)

print_array_info(intf,'intf')
print(intf[0:10])

fft_sla = fft(sp_sla)/np.size(xcol,0)*2
fft_mas = fft(sp_mas)/np.size(xcol,0)*2

# fft_sla = np.fft.fft(sp_sla,np.size(sp_sla,0),axis=0)/sp_sla.size*2
# fft_sla_freq =np.fft.fftfreq(np.size(sp_sla,0),1)
# fft_mas = np.fft.fft(sp_mas,np.size(sp_mas,0),axis=0)/sp_mas.size*2
# fft_mas_freq =np.fft.fftfreq(np.size(sp_mas,0),1)

fft_sla_shift = fftshift(fft_sla)
fft_mas_shift = fftshift(fft_mas)

# print("fft_sla \n",fft_sla[0:20])
# print_array_info(fft_sla,'fft_sla')
# print(max(fft_sla))

plt.figure(1)
# plt.plot(xcol,np.abs(sp_mas),label='sp_mas')
# plt.plot(xcol,np.abs(sp_sla),label='sp_sla')

# plt.plot(xcol,abs(fft_mas), linestyle='--',label='fft_mas')
# plt.plot(xcol,abs(fft_sla), linestyle='-',label='fft_sla')

plt.plot(xcol_shift,np.abs(fft_mas_shift),linestyle='-',label='fft_mas_shift')
plt.plot(xcol_shift,np.abs(fft_sla_shift),linestyle='-',label='fft_sla_shift')

# kaiser_win = np.kaiser(50,2.12)
# A = fft(kaiser_win,2048)/25.5
# mag = np.abs(fftshift(A))
# freq = np.linspace(-0.5, 0.5, len(A))
# response = 20 * np.log10(mag)
# # plt.plot(kaiser_win)
# plt.figure(1)
# plt.plot(freq, response)

# plt.figure(2)
# plt.plot(np.linspace(0,50,50), kaiser_win)

# plt.figure(3)
# plt.plot(xcol,np.angle(intf),label = 'intf')
# plt.plot(xcol,coh,label = 'coh')
# plt.plot(coh_stat_index,coh_stat,label = 'coh_stat')
# plt.hist(coh,100,(0,1),label = 'coh_stat')

plt.legend()
plt.show()



