# -*- encoding: utf-8 -*-

import xlrd
import sys
import json


data = xlrd.open_workbook(sys.argv[1])
sheet = data.sheet_by_index(0)
rows = sheet.nrows
result = {}
for row in range(rows):
    args = [str(i.value) for i in sheet.row(row)]
    a = {"brand": args[5], "name": args[3], "ch_name": args[4], "car_model": args[6]}
#    data = json.dumps(a, ensure_ascii=False)
    result[args[3]] = a

with open(sys.argv[2], 'a') as f:
    result = json.dumps(result, ensure_ascii=False)
    f.write(result)
