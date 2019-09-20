#!/bin/bash
#读取python文件
python3 switch_tsv3.0.py $1
echo "File has been ready..."
echo "----------------------------"

str1="/home/trec/TREC/collections/MS_files/MS_file" 
str2=".json"
state="is ready..."

#在ES中加入数据
for((i=1;i<=89;i++));
do
echo $str1$i$str2
curl -H "Content-Type: application/json"  -XPOST localhost:9200/trec/article/_bulk?pretty --data-binary @$str1$i$str2
done
echo "Transfer end..."
echo "------------------------------"
