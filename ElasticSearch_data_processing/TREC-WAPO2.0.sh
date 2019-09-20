#!/bin/bash
#读取python文件

str1="/home/trec/TREC/collections/WashingtonPost.v2/data/WAPO_TREC/WAPO_TREC_file" 
str2=".json"
state="is ready..."

#在ES中加入数据
for((i=0;i<=238;i++));
do
echo $str1$i$str2 + "-----------------ready for transfer..."
curl -H "Content-Type: application/json"  -XPOST localhost:9200/trec/article/_bulk?pretty --data-binary @$str1$i$str2
done
echo "Transfer end..."
echo "----------------------------"
