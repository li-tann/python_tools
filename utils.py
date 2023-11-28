import ctypes
import os
import re

#获取计算机名
def getComputerName():
    '''
    获取计算机名称
    '''
    pcName = ctypes.c_char_p(''.encode('utf-8'))
    pcSize = 16
    pcName = ctypes.cast(pcName, ctypes.c_char_p)
    try:
        ctypes.windll.kernel32.GetComputerNameA(pcName, ctypes.byref(ctypes.c_int(pcSize)))
    except Exception:
        print("Sth wrong in getname!")
    print(pcName.value.decode('utf-8'))
    return pcName.value.decode('utf-8')

def search_files(path, keyword):
    '''
    在path文件夹地址下, 逐个打开每个文件, 搜索关键词keyword
    :param path: 文件地址
    :param keyword: 关键字
    '''
    for root, dirs, files in os.walk(path):
        for name in files:
            if not str(name).endswith('.c'):
                continue
            file_path = os.path.join(root, name)
            try:
                with open(file_path, encoding='utf-8') as f:
                    if keyword in f.read():
                        print(file_path + " has keyword")
            except:
                print("open failed:" + file_path)
                pass

def filter_files_baseon_regex(root, regex):
    '''
    使用正则表达式筛选目录下的文件
    '''
    filterd_fileapths=[]
    rgx = re.compile(regex)
    for root, dirs, files in os.walk(root):
        for name in files:
            file_path = os.path.join(root, name)
            match_obj=re.findall(rgx,name)
            if match_obj:
                filterd_fileapths.append(name)
    return filterd_fileapths
