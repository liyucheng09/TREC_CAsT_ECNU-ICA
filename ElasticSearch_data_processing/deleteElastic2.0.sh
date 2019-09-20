#!/bin/bash

echo "ready to delete..."

#str1=curl -XDELETE 'localhost:9200/trec/article/
#str2=?pretty&pretty'
while read -r line
do
curl -XDELETE localhost:9200/trec/article/$line
done < $1

