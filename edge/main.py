"""
Author : Dochot.be
Date : 2024-04-10
Version : 1.0
Description : create little demo to test the model on the edge device
Source : https://pytorch.org/hub/nvidia_deeplearningexamples_efficientnet/
"""


# Importing the required libraries
import warnings
import logging
import os
import flask
from PIL import Image
from flask_cors import CORS
from edge.Ai import Ai

# Suppressing the warnings
warnings.filterwarnings('ignore')

# Initializing the logger
logging.basicConfig(filename='phoenix-demo.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initializing the Flask app
app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
ai = Ai()


# ------------------ Request ------------------ #
@app.route('/predict/url', methods=['POST'])
def predict():
    """
    This function will predict the image using the model.
    :return:
    """
    url = flask.request.json['url']
    batch_img = ai.load_image_url(url)
    predictions = ai.image_analyse(batch_img)
    result = ai.analyse_predictions(predictions, 5)
    return flask.jsonify([{'result': r} for r in result])


@app.route('/predict/image', methods=['POST'])
def predict_path():
    """
    This function will predict the image using the model.
    :return:
    """
    if flask.request.method == 'POST':
        if 'file' not in flask.request.files:
            return flask.jsonify({'error': 'No file part'})
        file = flask.request.files['file']
        file_name = file.filename
        file.save('static/' + file_name)
        batch_img = ai.load_image_path(Image.open('static/' + file_name))
        predictions = ai.image_analyse(batch_img)
        result = ai.analyse_predictions(predictions, 5)
        file.close()
        os.remove('static/' + file_name)
        return flask.jsonify([{'result': r} for r in result])


def main():
    """
    This function will run the Flask app.
    :return:
    """
    app.run(host='0.0.0.0', port=5050, debug=True)


if __name__ == '__main__':
    main()
