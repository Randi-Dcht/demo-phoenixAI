"""
Author : Dochot.be
Date : 2024-04-10
Version : 1.0
Description : create little demo to test the model on the edge device
Source : https://pytorch.org/hub/nvidia_deeplearningexamples_efficientnet/
"""


import torch
from torchvision.transforms import transforms


class Ai:
    def __init__(self):
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.efficientnet = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0',
                                           pretrained=True)
        self.utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_convnets_processing_utils')
        self.efficientnet.eval().to(self.device)

    def load_image_url(self, image_url):
        """
        This function will load the image from the URL and prepare it for the inference.
        :param image_url:
        :return:
        """
        batch = torch.cat(
            [self.utils.prepare_input_from_uri(image_url)]
        ).to(self.device)
        return self.efficientnet(batch)

    def load_image_path(self, img):
        """
        This function will load the image from the path and prepare it for the inference.
        :param img
        :return:
        """
        img_transforms = transforms.Compose(
            [transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor()]
        )
        img = img_transforms(img)
        with torch.no_grad():
            mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
            std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
            img = img.float()
            img = img.unsqueeze(0).sub_(mean).div_(std)
        batch = torch.cat(
            [img]
        ).to(self.device)
        return self.efficientnet(batch)

    def image_analyse(self, batch_img):
        """
        This function will run the inference on the image and print the top 5 predictions.
        :param batch_img:
        :return:
        """
        with torch.no_grad():
            output_predic = torch.nn.functional.softmax(batch_img, dim=1)
        return output_predic

    def analyse_predictions(self, output_predic, num_predictions=5):
        """
        This function will analyse the predictions.
        :param output_predic:
        :param num_predictions:
        :return:
        """
        # Get the top 5 predictions
        result = self.utils.pick_n_best(predictions=output_predic, n=num_predictions)
        return result


if __name__ == '__main__':
    ai = Ai()
    print(ai.analyse_predictions(ai.image_analyse(ai.load_image_url('http://images.cocodataset.org/test-stuff2017/000000024309.jpg')), 5))
    print(ai.analyse_predictions(ai.image_analyse(ai.load_image_url('http://images.cocodataset.org/test-stuff2017/000000006149.jpg')), 5))
