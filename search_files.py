# 在path文件夹地址下, 逐个打开每个文件, 搜索关键词keyword
import os


def search_files(path, keyword):
    """
    在path文件夹地址下, 逐个打开每个文件, 搜索关键词keyword
    :param path: 文件地址
    :param keyword: 关键字
    """
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