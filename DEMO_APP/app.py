
import os
import numpy as np
import cv2
import glob
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from retrieval_system.retrieve_and_evaluate import retrieve_image
from retrieval_system.feature_extraction import VGG16_FE, Xception_FE, ResNet50_FE, MobileNetV2__FE, EfficientNetV2__FE, InceptionV3__FE

from flask_cors import CORS


UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

CORS(app)


@app.route("/", methods=["GET"])
def index():
    removing_files = glob.glob('static/query/*.jpg')
    for i in removing_files:
        os.remove(i)
    return render_template("home.html", ALERT=0)

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/result", methods=["GET", "POST"])
def return_res():
    dst_dir = "static/query/"

    file = request.files.get("uploaded_img")

    print(file.filename)

    K = request.form.get("K")
    K = int(K) if K != "" else 3

    dataset_name = request.form.get("dataset")

    file.save(os.path.join(
        app.config['UPLOAD_FOLDER'],
        "query.jpg"
    ))

    method = request.form.get("method")

    img_query = cv2.imread("query.jpg")

    cv2.imwrite(dst_dir + "query.jpg", img_query)

    os.remove("query.jpg")
    
    dataset_folder_path = Path('static/datasets') / dataset_name
    if not dataset_folder_path.exists():
        dataset_folder_path.mkdir()

    images_folder_path = dataset_folder_path / 'images'
    if not images_folder_path.exists():
        images_folder_path.mkdir()

    binary_folder_path = dataset_folder_path / 'binary'
    if not binary_folder_path.exists():
        binary_folder_path.mkdir()

    methods_folder_path = binary_folder_path / method
    if not methods_folder_path.exists():
        methods_folder_path.mkdir()

    groundtruth_folder_path = dataset_folder_path / 'groundtruth'
    if not groundtruth_folder_path.exists():
        groundtruth_folder_path.mkdir()

    if method == 'VGG16':
        feature_extractor = VGG16_FE()
    elif method == 'Xception':
        feature_extractor = Xception_FE()
    elif method == 'ResNet50':
        feature_extractor = ResNet50_FE()
    elif method == 'MobileNetV2':
        feature_extractor = MobileNetV2__FE()
    elif method == 'EfficientNetV2':
        feature_extractor = EfficientNetV2__FE()
    elif method == 'InceptionV3':
        feature_extractor = InceptionV3__FE()
    

    res, time = retrieve_image("static/query/query.jpg", K, methods_folder_path, feature_extractor)

    paths = list(np.array(res)[:, 0])
    paths = [str(p) for p in paths]

    print(paths)
    return render_template("result.html", TIME=round(time, 2), PATHS=paths, METHOD=method,
                           QUERY=dst_dir + "query.jpg", K=K)