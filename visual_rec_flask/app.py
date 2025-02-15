from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob

#visual recognition
import json
from watson_developer_cloud import VisualRecognitionV3

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('base.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        visual_recognition = VisualRecognitionV3('2018-03-19',iam_apikey='Iv_iTjakXjT0jIp6hYUbg9bi4vrs4sAhkgfgI192Y4s-')
        with open(file_path, 'rb') as images_file:
            classes = visual_recognition.classify(images_file,threshold='0.6',classifier_ids='DefaultCustomModel_1653430306').get_result()
            a=json.loads(json.dumps(classes, indent=2))
            preds=a['images'][0]['classifiers'][0]['classes'][0]['class']
        return preds
    return None


if __name__ == '__main__':
    app.run(debug=True)

