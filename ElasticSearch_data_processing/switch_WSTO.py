#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys
import os

from contextlib import ExitStack
global file_sp
file_sp = 0 # 文件指针
global file_count  # 数据量
file_count = 0
global file_num  # 文件数目
file_num = 0


# In[5]:


def split_file(filename1,filename2):
    with open(filename1,"r",encoding="utf-8") as file_read:
        with open(filename2,"w",encoding="utf-8") as file_write:
            global file_sp
            global file_count
            global file_num
            file_read.seek(file_sp,0)
            lines = file_read.readline()
            while lines:
                file_count += 1 
                file_write.write(lines)
                print("data" + str(file_count) + " ready ---")
                sys.stdout.flush()
                if file_count % 2500 == 0:
                    file_num += 1
                    file_sp = file_read.tell()
                    sys.stdout.write("file"+str(file_num)+" has been ready!" +"\n")
                    sys.stdout.flush()
                    break
                lines = file_read.readline()
                


# In[6]:


if __name__ == "__main__":
    filename1 = sys.argv[1]
    path = os.path.dirname(filename1)
    path = os.path.join(path,"WAPO_TREC_files")
    if os.path.exists(path):
        for i in range(239):
            filename2 = path + "/WAPO_TREC_file" + str(i) + ".json"
            split_file(filename1,filename2)
    else:
        print("crating fold")
        os.mkdir(path)
        for i in range(239):
            filename2 = path + "/WAPO_TREC_file" + str(i) + ".json"
            split_file(filename1,filename2)


# In[ ]:



