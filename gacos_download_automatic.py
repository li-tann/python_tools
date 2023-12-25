import os
import requests
import shutil
import datetime
from requests.exceptions import RequestException
import subprocess

def download_file(url, local_filename, headers=None, resume=True):
    if headers is None:
        headers = {}

    # 检查文件是否已经部分下载
    if os.path.exists(local_filename) and resume:
        first_byte = os.path.getsize(local_filename)
        headers['Range'] = 'bytes=%s-' % first_byte
    else:
        first_byte = 0

    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 206:  # Partial Content
            content_length = int(response.headers.get('content-length', 0))
            total_size = first_byte + content_length
        elif response.status_code == 200:  # OK
            total_size = int(response.headers.get('content-length', 0))
        else:
            raise Exception(f"Unexpected HTTP status code: {response.status_code}")

        if total_size <= first_byte:
            print("Nothing left to download.")
            return

        with open(local_filename, 'ab') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    done = first_byte + len(chunk)
                    print("\rDownloading: %.2f%%" % (done * 100.0 / total_size), end='')
        print()  # 新行，完成进度条

    except RequestException as e:
        print(f"Error during download: {str(e)}")
        if os.path.exists(local_filename):
            os.remove(local_filename)

def url_exists(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {str(e)}")
        return False




with open("last_gacos_data_date.txt", "r+", encoding='utf-8') as f:  
    data = f.readline()
    print(data)
    #这里需要把真实的地址写下来
    url='.../{}.tar.gz'.format(data)
    print('url:',url)
    current_day=datetime.datetime.strptime(data,"%Y%m%d")
    print("current_day: ", current_day)
    next_day=(current_day+datetime.timedelta(days=1)).strftime('%Y%m%d')
    print("next_day: ", next_day)
    f.close()
    local_filepath=".../{}.tar.gz".format(data)
    print(local_filepath)

if(url_exists(url)):
    print('url is exist')
    print('download...')
    # download...
    # subprocess.run("d:/msys/usr/bin/wget.exe -c {}".format(url))

    if download_file(url,local_filepath):
        print('downloaded, update txt from current({}) to  next({})'.format(data,next_day))
        with open("last_gacos_data_date.txt", "w", encoding='utf-8') as f:
            f.write(next_day)
            f.close()
    else:
        print("download_file failed.")
else:
    print('url isn\'t exist')

