# -*- coding: utf-8 -*-
import os
import xlwt
import mimetypes
from io import BytesIO

from flask import Flask, request, redirect, url_for, send_from_directory, Response
from werkzeug.utils import secure_filename

from flask import make_response, send_file
# from raven.contrib.flask import Sentry
# from raven.handlers.logging import SentryHandler
# from raven import Client
import logging



# client = Client('https://3ac8f7df9e8b45149dbc68e7e6603bc9:731474d612b9473d844c3728e61ccbdb@sentry.io/1220553', capture_local=True)
# handler = SentryHandler(client)
# handler.setLevel(logging.WARN)
# log = logging.getLogger(__name__)
# log.addHandler(handler)


path = os.getcwd()
UPLOAD_FOLDER = '%s/uploads'%(path)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# sentry = Sentry(app, dsn='https://3ac8f7df9e8b45149dbc68e7e6603bc9:731474d612b9473d844c3728e61ccbdb@sentry.io/1220553')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/download/', methods=['GET'])
def download():

    filename = '/test.xlsx'
    with open(UPLOAD_FOLDER + filename, 'rb') as f:
        content = f.read()
    a = BytesIO(content)
    _file = Response(a)
    mime_type = mimetypes.guess_type(filename)[0]
    _file.headers['Content-Type'] = mime_type
    _file.headers['Content-Disposition'] = 'attachment; filename={}'.format("测试.xlsx".encode().decode('latin-1'))
    return _file


@app.route('/generate', methods=['GET'])
def test():
    out = BytesIO()
    wb = xlwt.Workbook()
    ws = wb.add_sheet('sheet1')
    ws.write(0, 0, 'Hello world')
    wb.save(out)
    content = out.getvalue()

    _file = Response(BytesIO(content))
    _file.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    _file.headers['Content-Disposition'] = 'attachment; filename={}'.format("测试.xlsx".encode().decode('latin-1'))
    return _file

    _file = send_file(BytesIO(content), mimetype='application/vnd.ms-excel', as_attachment=True,
            attachment_filename="测试.xlsx".encode().decode('latin-1'))
    return _file


@app.route('/test', methods=['GET'])
def web():
    import xlsxwriter
    out = BytesIO()
    wb = xlsxwriter.Workbook(out)
    worksheet = wb.add_worksheet()
    worksheet.write('A1', 'Hello world')
    wb.close()
    _file = send_file(BytesIO(out.getvalue()), mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True,
            attachment_filename="测试.xlsx".encode().decode('latin-1'))
    return _file
    _file = Response(BytesIO(out.getvalue()))
    _file.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    _file.headers['Content-Disposition'] = 'attachment; filename={}'.format("测试.xlsx".encode().decode('latin-1'))
    return _file


if __name__ == '__main__':
    app.run(debug=True)
