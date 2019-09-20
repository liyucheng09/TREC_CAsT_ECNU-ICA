#!/usr/bin/env python
# coding: utf-8

# In[6]:


import threading
import os
import sys

from contextlib import ExitStack
global file_sp
file_sp = 0 # 文件指针
global file_count  # 数据量
file_count = 0
global file_num  # 文件数目
file_num = 0


# In[11]:


def run(filename1,filename2):
    global file_sp
    global file_count
    global file_num
    with open(filename1,"r",encoding="utf-8") as f1:
        with open(filename2,"w",encoding="utf-8") as f2:
            
            f1.seek(file_sp,0)
            line = f1.readline()
            while line:
                line = line.replace("\n","")
                line = line.replace("\r","")
                file_count += 1
                line = "{\"delete\":{\"_id\":\""+line+"\"}}" + "\n"
                f2.write(line)
                sys.stdout.write("data "+str(file_count)+" has been ready!" +"\n")
                sys.stdout.flush()
                
                if file_count % 100000 == 0:
                    file_num += 1
                    file_sp = f1.tell()
                    break
                line = f1.readline()


# In[12]:


if __name__ == "__main__":
    filename1 = sys.argv[1]
    path = os.path.dirname(filename1)
    path = os.path.join(path,"flies_delete")
    files = []
    if os.path.exists(path):
        
        for i in range(30):
            filename2 = path + "/de_file" + str(i+1) + ".json"
            files.append(filename2)
        for filename2 in files:
            run(filename1,filename2)
    else:
        os.mkdir(path)
        for i in range(30):
            filename2 = path + "/de_file" + str(i+1) + ".json"
            files.append(filename2)
        for filename2 in files:
            run(filename1,filename2)


# In[ ]:




