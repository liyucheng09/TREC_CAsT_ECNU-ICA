#!/bin/bash
#读取python文件
python3 switch_WSTO.py $1
echo "----------------------------stateOne"
python3 /home/trec/TREC/collections/WashingtonPost.v2/data/data_process.py
echo "File has been ready..."
echo "----------------------------"

str1="/home/trec/TREC/collections/WashingtonPost.v2/data/WAPO_TREC_files" 
str2=".json"
state="is ready..."

#在ES中加入数据
for((i=0;i<=238;i++));
do
echo $str1$i$str2
curl -H "Content-Type: application/json"  -XPOST localhost:9200/trec/article/_bulk?pretty --data-binary @$str1$i$str2
done
echo "Transfer end..."
echo "----------------------------"