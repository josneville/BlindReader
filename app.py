import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    for file in request.files.getlist("file[]")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "Success", 200

@app.route('/', methods=['GET'])
def main():
    return "Success", 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '1000')))
