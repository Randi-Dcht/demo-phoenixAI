"""
Author : Dochot.be
Date : 2024-04-10
Version : 1.0
Description : create little demo to test the model on the edge device
Source : https://pytorch.org/hub/nvidia_deeplearningexamples_efficientnet/
"""


import unittest
from PIL import Image
from edge.Ai import Ai


class TestAi(unittest.TestCase):
    def test_load_image_url(self):
        ai = Ai()
        image_url = "http://images.cocodataset.org/test-stuff2017/000000024309.jpg"
        result = ai.load_image_url(image_url)
        self.assertIsNotNone(result)

    def test_load_image_path(self):
        ai = Ai()
        image_path = "test.jpg"
        result = ai.load_image_path(Image.open(image_path))
        self.assertIsNotNone(result)

    def test_image_analyse(self):
        ai = Ai()
        image_url = "http://images.cocodataset.org/test-stuff2017/000000024309.jpg"
        batch_img = ai.load_image_url(image_url)
        result = ai.image_analyse(batch_img)
        self.assertIsNotNone(result)

    def test_analyse_predictions(self):
        ai = Ai()
        image_url = "http://images.cocodataset.org/test-stuff2017/000000024309.jpg"
        batch_img = ai.load_image_url(image_url)
        predictions = ai.image_analyse(batch_img)
        result = ai.analyse_predictions(predictions, 5)
        self.assertIsNotNone(result)
