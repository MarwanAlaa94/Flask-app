import os
import sys
from flask import Flask, request, render_template, send_from_directory, send_file
from utils import pre_process, generate_video, clean_data
__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")

@app.route('/file-downloads/')
def file_downloads():
    return render_template('download.html')

@app.route('/return-files/')
def return_files_tut():
    target = os.path.join(APP_ROOT, 'files/')
    for file in os.listdir(target):
        if file.endswith("out.mp4"):
            return  send_file(target + file , attachment_filename=file)

@app.route("/upload", methods=["POST"])
def upload():
   # folder_name = request.form['superhero']
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, 'files/')
    clean_data(target)
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        print(filename + "ana henaaa")
        ext = os.path.splitext(filename)[1]
        destination = "".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        pre_process(target, destination ,filename)
        generate_video(target, filename)




    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", value=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)


if __name__ == "__main__":
    app.run(port=4555, debug=True)
