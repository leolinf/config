#!/usr/bin/python
#coding=utf-8

import StringIO
import xlwt
import json
import sys


each_encode=lambda x:[i.encode('utf-8') for i in x]


def filter_none(one_list):
    for i in range(len(one_list)):
        if one_list[i]==None:
            one_list[i]=""
    return one_list


def make_xls_file(header_list,data_list):
    headers=each_encode(filter_none(header_list))
    datas=[each_encode(filter_none(row)) for row in data_list]

    mem_file=StringIO.StringIO()
    wb=xlwt.Workbook(encoding='utf-8', style_compression=0)
    ws=wb.add_sheet('Sheet1')
    r=0
    c=0
    for header in headers:
        ws.write(r,c,header)
        c+=1

    for data in datas:
        r+=1
        c=0
        for datais in data:
            #datai = json.loads(datais)
            #datai = json.dumps(datai, ensure_ascii=False)
            ws.write(r,c,datais)
            c+=1
    wb.save(mem_file)
    mem_file.flush()
    return mem_file

def chg_doc(doc):
    newdoc={}
    for k in doc:
        v=doc[k]
        if k == 'result':
            if doc['result']['all'] != 0:
                for a in doc['result']:
                    v = doc['result'][a]
                    newdoc['count_'+a] = doc['result'][a]
            else:
                newdoc['count_all'] = ''
                newdoc['count_zw'] = ''
                newdoc['count_wb'] = ''
                newdoc['count_app'] = ''
                newdoc['count_jw'] = ''
                newdoc['count_baokan'] = ''
                newdoc['count_wz'] = ''
                newdoc['count_lt'] = ''
                newdoc['count_bk'] = ''
                newdoc['count_xw'] = ''
                newdoc['count_sp'] = ''
                newdoc['count_wx'] = ''

#        elif k == 'others':
#            if len(doc['others']) == 6:
#                newdoc['brand'] = doc['others'][2].strip()
#                newdoc['type'] = doc['others'][0].strip()
#                newdoc['tag1'] = doc['others'][1]
#                newdoc['tag2'] = doc['others'][3]
#                newdoc['tag3'] = doc['others'][4]
#                newdoc['tag4'] = doc['others'][5]
#            else:
#                newdoc['brand'] = doc['others'][2].strip()
#                newdoc['type'] = doc['others'][0].strip()
#                newdoc['tag1'] = ''
#                newdoc['tag2'] = ''
#                newdoc['tag3'] = ''
#                newdoc['tag4'] = ''
        else:
            newdoc[k]=doc[k]

    for k in newdoc:
        v=newdoc[k]
        if v==None:
            newdoc[k]=""
        elif type(v)!=unicode:
            newdoc[k]=str(v)
    return newdoc


def chg_doc_1(doc):
    newdoc={}
    for k in doc:
        v=doc[k]
        if k == 'other':
            a = doc['other']
            for a1 in a:
                newdoc[a1] = a[a1]
        elif k == 'tags':
            b = doc['tags']
            newdoc['create_time'] = b[0]
            try:
                newdoc['category'] = b[1]
            except:
                newdoc['category'] = ''
        elif k == 'detail':
            c = doc['detail']
            for c1 in c:
                newdoc[c1['key']] = c1['values']
        else:
            newdoc[k]=doc[k]
    data = json.dumps(newdoc, ensure_ascii=False).encode('utf-8')
    with open('newdoc.json', 'a') as f:
        f.write(data + '\n')

    for k in newdoc:
        v=newdoc[k]
        if v is None:
            newdoc[k]=""
        elif type(v)!=unicode:
            newdoc[k]=str(v)
    return newdoc


def chg_doc_2(doc):
    newdoc={}
    for k in doc:
        newdoc[k]=doc[k]
    for k in newdoc:
        v=newdoc[k]
        if v is None:
            newdoc[k]=""
        elif type(v)!=unicode:
            newdoc[k]=str(v)
    return newdoc


def readfile(fin):
    header_list=[]
    data_list=[]
    for line in fin:
        do=json.loads(line)
        doc = do.get("data", {}) or {}
        doc=chg_doc_2(doc)
        header_list=doc.keys()
        data=[]
        for k in header_list:
            data.append(doc[k])
        data_list.append(data)
    return header_list, data_list


def writefile(mem_file, fout):
    fout.write(mem_file.getvalue())
    fout.close()


def main(fin, fout):
    header_list, data_list=readfile(fin)
    mem_file=make_xls_file(header_list, data_list)
    writefile(mem_file, fout)


if __name__ == '__main__':
    fin_name=sys.argv[1]
    fout_name=sys.argv[2]
    fin=open(fin_name, 'r')
    fout=open(fout_name, 'w')
    main(fin, fout)
