import os
import cv2
import random, string
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from stitching import AlignImagesRansac
import logging
from PIL import Image
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import subprocess

# Register the streaming http handlers with urllib2
register_openers()

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
@app.route('/uploadImages', methods=['POST'])
def uploadImage():
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
            dst = Image.open(os.path.join(newpath, filename))
            dst = dst.rotate(90)
            dst.save(os.path.join(newpath, filename))
            filenames.append(filename)
    AlignImagesRansac(newpath, "main1.jpg", finishedpath)
    finishedFileList = os.listdir(finishedpath)
    finishedFileList = [s.replace('.jpg', '') for s in finishedFileList]
    finishedFileList = [s.replace('.JPG', '') for s in finishedFileList]
    finishedFileList = [s.replace('main', '') for s in finishedFileList]
    finishedFileList = [int(numeric_string) for numeric_string in finishedFileList]
    ocrimage = finishedpath + "/" + str(max(finishedFileList)) + ".JPG"
    datagen, headers = multipart_encode({"image": open(ocrimage), "language": "en", "apikey": "rQn56HMQks"})
    req = urllib2.Request("http://api.ocrapiservice.com/1.0/rest/ocr", datagen, headers)
    # Actually do the request, and get the response
    text = urllib2.urlopen(req).read()
    return text, 200

@app.route('/uploadVideo', methods=['POST'])
def uploadVideo():
    uploadedVideo = request.files.getlist("file[]")
    randomString = ''.join(random.choice(string.lowercase) for i in range(10))
    newpath = app.config['UPLOAD_FOLDER'] + "/" + randomString
    videopath = newpath + "/Video"
    startpath = newpath + "/Initial"
    finishedpath = newpath + "/Finished"

    os.makedirs(newpath)
    os.makedirs(videopath)
    os.makedirs(startpath)
    os.makedirs(finishedpath)

    uploadedVideo[0].save(os.path.join(videopath, "video.mp4"))
    command = "ffmpeg -i "+os.path.join(videopath, "video.mp4")+" -f image2 -r 1 "+startpath+"/main%2d.jpg"
    p = subprocess.call(command, shell=True)


    AlignImagesRansac(startpath, "main01.jpg", finishedpath)
    print "Alignment Finished"
    finishedFileList = os.listdir(finishedpath)
    finishedFileList = [s.replace('.jpg', '') for s in finishedFileList]
    finishedFileList = [s.replace('.JPG', '') for s in finishedFileList]
    finishedFileList = [s.replace('main', '') for s in finishedFileList]
    finishedFileList = [int(numeric_string) for numeric_string in finishedFileList]
    ocrimage = finishedpath + "/" + str(max(finishedFileList)) + ".JPG"
    datagen, headers = multipart_encode({"image": open(ocrimage), "language": "en", "apikey": "rQn56HMQks"})
    req = urllib2.Request("http://api.ocrapiservice.com/1.0/rest/ocr", datagen, headers)
    # Actually do the request, and get the response
    text = urllib2.urlopen(req).read()
    return text, 200


    return "Success", 200
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
