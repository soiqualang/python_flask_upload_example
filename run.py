#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from flask import Flask, flash, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import json
import uuid
sys.path.append('func/')
import phuyen


app = Flask(__name__)

UPLOAD_FOLDER = './static/upload/'
OUTPUT_FOLDER = './static/output/'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return 'hahahaha'


#http://flask.pocoo.org/docs/1.0/patterns/fileuploads/

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/phuyen/tiendosanxuat', methods=['GET', 'POST'])
def flower_detection():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            kq_temp=''
            kq_temp+='File: <a href="{}" target="_blank">Download</a>'
            kq_temp+='<br>'
            kq_temp+='<b>Logs</b><br>'
            kq_temp+='<pre>{}</pre>'
            
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_extension = os.path.splitext(file.filename)[1]
            filename = secure_filename(uuid.uuid4().hex + '.' + file_extension)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            imgurl = '/static/upload/%s' % (filename)
            res = phuyen.tiendosanxuat_process(imgurl)
            return kq_temp.format(res[0],res[1])
    return '''
    <!doctype html>
    <title>Upload file - soiqualang chentreu</title>
    <h1>Upload file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=1075)