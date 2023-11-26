import torch

from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def preprocess(self, image: torch.Tensor)-> torch.Tensor:
        pass
