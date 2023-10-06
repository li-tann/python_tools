import osgeo.gdal as gdal
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, ifft

from utils import getComputerName

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
        if np.isnan(c):
            continue
        k = int(c*100)
        if k<0:
            k=0
        if k >=100:
            k=99
        coh_stat[k] = coh_stat[k] + 1
    coh_stat = coh_stat / np.size(array_coh,0)
    return array_coh, coh_stat  

if getComputerName() == "LITANR7000P":
    path_mas = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\master.rslc.vrt"
    path_mas_json = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\master.rslc.json"
    path_sla = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\slave.rslc.vrt"
    path_sla_json = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\slave.rslc.json"

    '''配准前的主辅影像'''
    # path_mas = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\DInSAR\\_slc\\sarbox\\slc\\LT1A_20230321.slc.vrt"
    # path_sla = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\DInSAR\\_slc\\sarbox\\slc\\LT1A_20230329.slc.vrt"

else:
    '''DESKTOP-4U7COK0'''
    path_mas = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\master.rslc.vrt"
    path_mas_json = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\master.rslc.json"
    path_sla = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\slave.rslc.vrt"
    path_sla_json = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\slave.rslc.json"

# '''thinkbook'''
# # path_mas = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\master.rslc.vrt"
# # path_sla = "d:\\1_Data\\L-SAR_TEST\\dinsar_mono_cut2\\_slc\sarbox\\registration\\slave.rslc.vrt"
# '''legion'''
# path_mas = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\master.rslc.vrt"
# path_sla = "e:\\_REMOTE_SENSING_DATA\\LSAR_TEST\\DInSAR\\_slc\\sarbox\\registration\\slave.rslc.vrt"




