# import pysftp
import paramiko
import os

'''
sftp_info.txt

hostname: "xxx.xxx.xxx.xxx"
post: "xxxx"
username: "xxxxx"
Password: "xxxx"
localpath: "xx/xxx/"
remotepath: "/xxxx/xxx/xx/"
'''

f = open("sftp_info.txt")
lines=f.readlines()
    
if len(lines)<6:
    print("Error: line of sftp_info.txt < 6")
    exit()

f.close()

Hostname = lines[0].split("\"")[1]
post = int(lines[1].split("\"")[1])
Username = lines[2].split("\"")[1]
Password = lines[3].split("\"")[1]
localpath = lines[4].split("\"")[1]
remotepath = lines[5].split("\"")[1]

print(Hostname, post, Username, Password, localpath, remotepath) 

client = paramiko.Transport((Hostname,post))
client.connect( username=Username,password=Password)
sftp = paramiko.SFTPClient.from_transport(client)

'''检查本地空间内有哪些文件, 如果与远端空间存在重复文件, 则不用重复下载'''
# relative_paths=[]
# for root,dirs,files in os.walk(localpath):
#         for file in files:
#                 rela_path=os.path.join(root,file)
#                 print(rela_path)
#                 relative_paths.append(rela_path)

# print(relative_paths)

sftp.chdir(remotepath)
directory_structure = sftp.listdir_attr()
for attr in directory_structure:
    if str(attr)[0]=="d":
        print("dir: ",attr)
    else:
        print("     ",attr)
    # if str(attr)[0]=="d":
    #     print("is dir , ", remotepath+attr.filename)
    # else:
    #     print("is file, ", remotepath+attr.filename)

'''[i][0] is remotepath, [i][1] is localpath'''
files_path_tobe_download=[]
for attr in directory_structure:
    if not(str(attr)[0]=="d"):
        files_path_tobe_download.append([remotepath + attr.filename, localpath + attr.filename])

print(files_path_tobe_download)

# for paths in files_path_tobe_download:
#     sftp.get(remotepath=paths[0], localpath=paths[1])
    

client.close()