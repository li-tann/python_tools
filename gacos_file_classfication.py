import os
import sys

path=sys.argv[1]
new_path=sys.argv[2]

'''
将path地址下的gacos数据以文件名中的时间作为参考信息, 移动到new_path/data/的地址内
'''

for root, dirs, files in os.walk(path):
    for name in files:
        if not str(name).endswith('.tif'):
            continue
        file_path = os.path.join(root, name)
        # print(root)
        underline_splited = file_path.split("_")
        date_str=underline_splited[len(underline_splited)-1].split(".")[0]
        # print(date_str)
        
        data_dir=os.path.join(new_path, date_str)
        if not(os.path.exists(data_dir)):
            os.mkdir(data_dir)
            print("mkdir: [{}]".format(data_dir))

        new_file_path=os.path.join(data_dir, name)
        print(new_file_path)
        os.rename(file_path,new_file_path)
