import os

def search_files(path, keyword):
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



