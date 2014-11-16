import os
import random, string
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from stitching import AlignImagesRansac
import logging
import stitching
import Image
import pytesseract

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)
# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    randomString = ''.join(random.choice(string.lowercase) for i in range(10))
    newpath = app.config['UPLOAD_FOLDER'] + "/" + randomString
    finishedpath = app.config['UPLOAD_FOLDER'] + "/" + randomString + "-Finished"
    os.makedirs(newpath)
    os.makedirs(finishedpath)
    for idx, file in enumerate(uploaded_files):
        if file:
            fileSplit = file.filename.rsplit('.')
            filename = "main" + str(idx + 1) + "." + fileSplit[len(fileSplit)-1]
            file.save(os.path.join(newpath, filename))
            filenames.append(filename)
    AlignImagesRansac(newpath, "main1.jpg", finishedpath)
    finishedFileList = os.listdir(finishedpath)
    finishedFileList = [s.replace('.jpg', '') for s in finishedFileList]
    finishedFileList = [s.replace('.JPG', '') for s in finishedFileList]
    finishedFileList = [s.replace('main', '') for s in finishedFileList]
    finishedFileList = [int(numeric_string) for numeric_string in finishedFileList] 
    return finishedpath + "/main" + str(max(finishedFileList)) + ".jpg", 200

@app.route('/test', methods=["GET"])
def test():
    args = ['./uploads/test', '1.jpg', '.uploads/test']
    AlignImagesRansac(args)
    return "Success", 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '1000')))
