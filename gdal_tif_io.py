import osgeo.gdal as gdal
import sys

'''
指定tar起始行列号, 以及宽高，计算起始点的经纬度, 并转换到ref的行列号, 并计算tar.width/tar.height转换到ref.height和ref.width后的值
从ref中提取数据, 写入到tar中
'''

path_tar = "C:/Users/lenovo/Desktop/DataV.GeoAtlas/shp/河北省.tif"
path_ref = "C:/Users/lenovo/Desktop/DataV.GeoAtlas/shp/河北省.tif"



'''打开栅格数据'''
try:
    tar_ds: gdal.Dataset=gdal.Open(path_tar)
except RuntimeError as e:
    print( 'Unable to open %s'% path_tar)
    sys.exit(1)

tar_cols = tar_ds.RasterXSize #图像长度
tar_rows = tar_ds.RasterYSize #图像宽度
# data_mas = ds_mas.ReadAsArray(0, 0, cols, rows) #转为numpy格式

tar_rb: gdal.Band= tar_ds.GetRasterBand(1)
tar_datatype = tar_rb.DataType

try:
    ref_ds: gdal.Dataset=gdal.Open(path_ref)
except RuntimeError as e:
    print( 'Unable to open %s'% path_ref)
    sys.exit(1)

ref_cols = ref_ds.RasterXSize #图像长度
ref_rows = ref_ds.RasterYSize #图像宽度
# data_mas = ds_mas.ReadAsArray(0, 0, cols, rows) #转为numpy格式

ref_rb: gdal.Band= ref_ds.GetRasterBand(1)
ref_datatype = ref_rb.DataType

if not tar_datatype == ref_datatype:
    print( 'tar.datatype({}) is diff with ref.datatype({})'.format(gdal.GetDataTypeName(tar_datatype),  gdal.GetDataTypeName(ref_datatype)))
    sys.exit(1)

