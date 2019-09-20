#!/usr/bin/env python
# coding: utf-8

# In[30]:


import json
import sys

# In[31]:


def changeform(filename1,filename2):
    """change the formation of json"""
    with open(filename2,"w",encoding="utf-8")  as f2:
        with open(filename1,"r",encoding='utf-8') as f:
            #申明全局变量
            global file_count
            global file_sp
            global data_count
            
            file_count += 1
            print("This is file No."+ str(file_count))
            
            #读取文件指针
            f.seek(file_sp,0)
            
            lines = f.readline()
            count = 0
            
            while lines:
                count += 1
                lines = lines.strip(" ").replace("\n","")
                lines = lines.replace(r"\"","")
                lines = lines.split(":", 1)
                
                if count % 5 == 2 :
                  #  print(lines)
                    insert_line1 = "{\"index\": {\"_index\": \"trec\", \"_type\": \"article\", \"_id\":" +lines[-1][:-1]+"}}"+"\n"
                    f2.write(insert_line1)
                    
                if count % 5 == 4 :
                    insert_line2 = "{\"BODY\": \"" + lines[-1][4:-3] + "\"}"+"\n"
                    f2.write(insert_line2)
                    data_count += 1
                    sys.stdout.write("data "+str(data_count)+" success\n")
                    sys.stdout.flush()
                    
                    if data_count % 100000 == 0:
                        f.readline()
                        file_sp = f.tell()
                        
                        break    
                    
                lines = f.readline()


# In[32]:


if __name__ == "__main__":

    file_count = 0
    file_sp = 0
    data_count = 0
    # 获取参数 前面为命令行获取
#     file1 = sys.argv[1]
#     file2 = sys.argv[2] 
#     file3 = sys.argv[3]
#     file4 = sys.argv[4]
    # 获取参数 为指定位置获�?#    file1 = "/Users/tinymountain/Desktop/TREC-CAR-TEST.json"
#     file2 = "/Users/tinymountain/Desktop/a.json"
#     file3 = "/Users/tinymountain/Desktop/b.json"
#     file4 = "/Users/tinymountain/Desktop/c.json"

    file1 = sys.argv[1]
    file_list = []
    for i in range(300):
        tiny_file = "/home/trec/TREC/collections/TREC-CAR-Tiny/TREC-CAR-tiny" + str(i+1) +".json"
        
        file_list.append(tiny_file)
        
#    file_list = [file2, file3, file4]
    file_count = 0  # 文件�?    file_sp = 0  # 文件指针
    
    for filename in file_list:
        changeform(file1,filename) 


# In[ ]:




