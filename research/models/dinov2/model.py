import time

import PIL.Image
import torch

from research.data.synthetic.utils.datapoints.image import ImageType, ImageData
from research.models.base import BaseModel
from torchvision import transforms
from enum import Enum, auto

IMAGENET_DEFAULT_MEAN = (0.485, 0.4546, 0.406)
IMAGENET_DEFAULT_STD = (0.229, 0.224, 0.225)


class ModelSize(Enum):
    SMALL = 's'
    BIG = 'b'
    LARGE = 'l'
    GIANT = 'g'


class DinoV2(BaseModel):
    def __init__(self, model_size: ModelSize, resize_size: int = 518, crop_size: int = 518):
        self.transform = transforms.Compose([
            transforms.Resize(resize_size, interpolation=transforms.InterpolationMode.BICUBIC, antialias=True),
            transforms.CenterCrop(crop_size),
            transforms.Normalize(mean=IMAGENET_DEFAULT_MEAN, std=IMAGENET_DEFAULT_STD)
        ])

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.hub.load('facebookresearch/dinov2', f'dinov2_vit{model_size.value}14').to(self.device)
        self.model.eval()

    def preprocess(self, image: torch.Tensor) -> torch.Tensor:
        return self.transform(image)

    def inference(self, image: ImageType):
        image = ImageData(image).get_image(with_wrapper=False)
        image = image.type(torch.FloatTensor).to(self.device)
        image = self.preprocess(image).unsqueeze(0)
        with torch.no_grad():
            features = self.model(image)
        return features.cpu().detach().numpy()


if __name__ == "__main__":
    model = DinoV2(ModelSize.BIG)
    features = model.inference(
        'https://img.freepik.com/premium-vector/young-girl-anime-style-character-vector-illustration-design-manga-anime-girl_147933-100.jpg?w=2000')
    print(features.shape)
