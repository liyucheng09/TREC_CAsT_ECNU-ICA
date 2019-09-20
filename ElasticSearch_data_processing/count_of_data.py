#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import sys


# In[14]:


def count_num(filename):
    """计算长度"""
    count = 0
    file_count = 0 
    with open(filename,"r",encoding="utf-8") as f:
        load_file = f.readline()
        while load_file:
            count += 1
            if count % 5 == 0:
                file_count += 1
                sys.stdout.write("we have " + str(file_count) +" datas already\n")
                sys.stdout.flush()
            load_file = f.readline()
    return file_count


# In[15]:


if __name__ == "__main__":
    filename = sys.argv[1]
    # filename = "/Users/tinymountain/Desktop/TREC-CAR-TEST.json"
    data_count = count_num(filename)
    print("Processing finished---------------")
    print("the count of the datas are " + str(data_count))


# In[ ]:




