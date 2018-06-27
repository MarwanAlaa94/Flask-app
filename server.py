import os
import sys
from flask import Flask, request, render_template, send_from_directory, send_file
from utils import pre_process, generate_video, clean_data

__author__ = 'ibininja'

PEOPLE_FOLDER = os.path.join('static', 'photo')

app = Flask(__name__, static_url_path='/static')

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def show_index():
    return render_template("home.html")

@app.route('/return-video/')
def return_video_tut():
    target = os.path.join(APP_ROOT, 'files/')
    for file in os.listdir(target):
        if file.endswith("out.mp4"):
            return  send_file(target + file , attachment_filename=file)

@app.route('/return-image/')
def return_image_tut():
    target = os.path.join(APP_ROOT, 'files/')
    for file in os.listdir(target):
        if file.endswith(".png"):
            return  send_file(target + file , attachment_filename=file)

@app.route("/video_upload", methods=["POST"])
def video_upload():
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
        if (ext == ".mp4"):
            print("File supported moving on...")
        else:
            return render_template("Error.html", message=
                """The application supports only mp4
                videos, this format is not supported""")
        destination = "".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        pre_process(target, destination ,filename)
        generate_video(target, filename)
    return render_template("complete_video.html", value=filename)


@app.route("/image_upload", methods=["POST"])
def image_upload():
    target = os.path.join(APP_ROOT, 'static/photo/')
    clean_data(target)
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            return render_template("Error.html", message=
                """The application supports only jpg and png
                images, this format is not supported""")

        destination = "".join([target, filename])
        upload.save(destination)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template("complete_image.html", user_image = full_filename,
        filename = filename)


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
