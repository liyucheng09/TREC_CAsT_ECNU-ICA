#!/bin/bash
#读取python文件
python3 changeForm_delete.py $1
str1="/home/trec/TREC/tools/flies_delete/de_file" 
str2=".json"
state="is ready..."

#在ES中加入数据
for((i=1;i<=30;i++));
do
echo $str1$i$str2 + "-----------------ready for transfer..."
curl -H "Content-Type: application/json"  -XPOST localhost:9200/trec/article/_bulk?pretty --data-binary @$str1$i$str2
done
echo "delete end..."
echo "----------------------------"