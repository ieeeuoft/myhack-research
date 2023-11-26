import numpy as np
import torch
from research.utils.ann.numpy import NumPy


class Torch(NumPy):
    def __init__(self, config):
        super().__init__(config)

        self.all, self.cat, self.dot, self.zeros = torch.all, torch.cat, torch.mm, torch.zeros

    def tensor(self, array):
        if isinstance(array, np.ndarray):
            array = torch.from_numpy(array)

        if torch.cuda.is_available():
            return array.cuda()
        return array

    def settings(self):
        return {"torch": torch.__version__}
