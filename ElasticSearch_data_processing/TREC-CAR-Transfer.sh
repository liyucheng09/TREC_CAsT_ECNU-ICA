#!/bin/bash
#读取python文件
python3 switch_json_2.0.py $1
echo "File has been ready..."
echo "----------------------------"

str1="/home/trec/TREC/collections/TREC-CAR-Tiny/TREC-CAR-tiny" 
str2=".json"
state="is ready..."

#在ES中加入数据

for((i=1;i<=300;i++));
do
echo $str1$i$str2$state
curl -H "Content-Type: application/json"  -XPOST localhost:9200/trec/article/_bulk?pretty --data-binary @$str1$i$str2
done
echo "Transfer end..."
echo "----------------------------"