import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import xml.etree.ElementTree as ET
import command

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['zip', 'tar.gz', 'tar.gz2', 'rar'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def construct_error(root):
    error = {}
    error['checker'] = root[0].text
    error['file'] = root[2].text
    error['function'] = root[3].text
    error['description'] = root[6][2].text
    error['line'] = root[6][3].text
    return error

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    with open('C:\\Users\\walker\\Desktop\\MOLINT.RECURSIVE.CALL.xml') as myfile:
        data = myfile.read().replace('\n', '')
    parser = ET.XMLParser()
    parser.feed('<errors>')
    parser.feed(data)
    parser.feed('</errors>')
    root = parser.close()
    errors = []
    for child in root:
        error = construct_error(child)
        errors.append(error)
    return render_template("index.html", errors=errors)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            os.chdir(UPLOAD_FOLDER)
            path = command.unzip(filename)
            command.run_make(path)
            command.run_checker(path)

            return redirect(url_for('upload_file', filename=filename))

    return render_template('upload.html')

if __name__ == "__main__":
    app.run()
