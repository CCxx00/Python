import os
import os.path
import struct

def fun(textname,textname1):
    filehandle=open(textname)
    file=open(textname1,'w')
    filelist=filehandle.readlines()
    for l in filelist:
        # print(l)
        if l not in ['\n','\r',' \n',' \r\n']:
            file.write(l)
    file.close()
    filehandle.close()
    os.system("type "+textname1+" | clip")

fun('1.txt','2.txt')
