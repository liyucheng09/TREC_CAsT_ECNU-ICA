import xml.etree.ElementTree as ET
import json
import traceback

file_output='/home/trec/TREC/collections/TREC-CAR-paragraph-v2.0.json'
file_output=open(file_output, 'w', encoding='utf-8', buffering=10000)

file='/home/trec/TREC/collections/TREC-CAR-paragraph-v2.0.xml'
s=''

replace_map=str.maketrans({'&':'', '<':'','>':''})
flag=0

with open(file, 'r', encoding='utf-8') as f:
    for new_line in f:
        if flag:
            new_line=new_line.translate(replace_map)
        if new_line=='<BODY>\n':
            flag=1
        if new_line=='</BODY>\n':
            flag=0
        s+=new_line
        if new_line=='</DOC>\n':
            #print('------')
            #print(s)
            #s=s.translate(replace_map)
            root=ET.fromstring(s)
            js={e.tag: e.text for e in root}
            file_output.write(json.dumps(js, indent=4, ensure_ascii=False))
            file_output.write('\n')
            s=''
            del js, root
            #print('*****')
file_output.close()
