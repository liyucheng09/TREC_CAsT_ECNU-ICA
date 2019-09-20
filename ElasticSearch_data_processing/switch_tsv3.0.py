#!/usr/bin/env python
# coding: utf-8

# In[41]:


import sys
import re
import os

from contextlib import ExitStack
global file_sp
file_sp = 0 # 文件指针
global file_count  # 数据量
file_count = 0
global file_num  # 文件数目
file_num = 0


# In[42]:


def switch_tsv(filename,filename2):
    global file_sp
    global file_count
    global file_num
    with open(filename1,"r",encoding="utf-8") as file_read:
        with open(filename2,"w",encoding="utf-8") as file_write:
            file_read.seek(file_sp,0)
            lines = file_read.readline()
            # 改变数据的格式
            data_count = 0
            while lines:
                data_count += 1
                lines = lines.split("	",1)
                data_index = lines[0]
                line1 = "{\"index\":{\"_index\":\"trec\",\"_id\":\"MARCO_"+ str(data_index) +"\"}}" + "\n"
                file_write.write(line1)
                data_body = lines[1].replace("\n","")
                data_body = re.sub(r"[^A-Za-z0-9 .,()-‘']"," ",data_body)
                line2 = "{\"BODY\":\""+ data_body +"\"}" + "\n"
                file_write.write(line2)
    #            lines = file_read.readline()
                file_count += 1

                sys.stdout.write("data " + str(file_count)+" has been ready..." + "\n")
                sys.stdout.flush()
                if data_count % 100000 == 0:
                    file_num += 1
                    file_sp = file_read.tell()
                    sys.stdout.write("file"+str(file_num)+" has been ready!" +"\n")
                    sys.stdout.flush()
                    break
                lines = file_read.readline()


# In[43]:


if __name__ == "__main__":
    filename1 = sys.argv[1]
    path = os.path.dirname(filename1)
    #path = os.path.join(path,"MS_TREC_Files")
    files = []
    for i in range(89):
        filename2 = os.path.join(path,"MS_files") + "/MS_file" +str(i+1) +".json"
        files.append(filename2)
    for filename2 in files:
        switch_tsv(filename1,filename2)


# In[ ]:





# In[ ]:



