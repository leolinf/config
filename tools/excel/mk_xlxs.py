# -*- coding:utf-8 -*-

from io import BytesIO
import xlsxwriter


output = BytesIO()
wb = xlsxwriter.Workbook(output, {'in_memory': True})
ws = wb.add_worksheet()
fmt = wb.add_format()
fmt.set_num_format('@')
ws.set_column('A:Z', None, fmt)
rows = [
    '大区名称', '大区负责人', '大区负责人身份证号', '大区负责人手机号',
    '门店名称', '门店详细地址', '门店管理人姓名', '门店管理人身份证号', '门店管理人手机号',
    '门店销售员姓名', '门店销售员身份证号', '门店销售员手机号'
]
for index, name in enumerate(rows):
    ws.write_string(0, index, name)
wb.close()
content = output.getvalue()
print(output.seek(0))
