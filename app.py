#import zip
import os
from flask import Flask, redirect, request, url_for, flash, send_file, Response
from jinja2 import Environment, PackageLoader
from werkzeug.utils import secure_filename
from PIL import Image,ImageDraw,ImageFont
import re
import shutil

UPLOAD_FOLDER = '/Users/itstimetogetout/Desktop/Projects/FranciscanLads/MiniProjects/certi_generator/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'docx', 'css'}

app = Flask(__name__)
get = Environment(loader=PackageLoader(__name__, 'templates')).get_template
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        names = request.form.get('names', '')
        font = request.form.get('font', '')
        height = request.form.get('height', '')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            create_certificate(os.path.join(app.config['UPLOAD_FOLDER'], filename), names, int(font), int(height))
            return redirect(url_for('downloads'))
    return get('login.html').render()

@app.route('/downloads/')
def downloads():
    return get('download.html').render()

@app.route('/return-files/')
def return_files_tut():
    try:
        result = send_file('/Users/itstimetogetout/Desktop/Projects/FranciscanLads/MiniProjects/certi_generator/outputzip.zip', attachment_filename='outputzip.zip')
        os.remove('outputzip.zip')
        return result
    except Exception as e:
        return str(e)

def create_certificate(filename, names, fontsize, height):
    names=names.split("\n")
    font = ImageFont.truetype("arial.ttf", fontsize)
    img = Image.open(filename)
    W, H = img.size
    for name in names:
        name = name.replace(chr(13), '')
        img = Image.open(filename)
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(name, font=font)
        draw.text(((W-w)/2, height), name, (0, 0, 0), font=font, align="center")
        name = re.sub('\W+',' ', name)
        s = name+'.png'
        print(s) 
        if s != ".png":
            img.save("/Users/itstimetogetout/Desktop/Projects/FranciscanLads/MiniProjects/certi_generator/output/"+s, 'PNG')
    shutil.make_archive('outputzip', 'zip', 'output')
    shutil.rmtree('output')
    shutil.rmtree('uploads')
    os.mkdir('output')
    os.mkdir('uploads')

if __name__ == '__main__':
    app.debug = True
    app.run()
