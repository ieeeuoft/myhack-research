import os
import pandas as pd
<<<<<<< HEAD
from torchvision.io import read_image
from torch.utils.data import Dataset
=======
import pytorch_lightning as pl
from torchvision.io import read_image
from torch.utils.data import Dataset, DataLoader
>>>>>>> 1fd36c5a (1: Create Dataloader and Dataset for ML Research)

class MyHackImageDataset(Dataset):
    def __init__(self, metadata_csv, img_dir, category, transform=None):
        self.img_labels = pd.read_csv(metadata_csv)
        self.img_dir = img_dir
        self.transform = transform
        
    def size_dataset(self):
        return len(self.img_labels)
    
    def get_data(self, idx):
        img_path = os.path.join(img_dir, self.img_labels[idx, 'categories'])
        image = read_image(img_path)
        label = self.img_labels[idx, 'name']
        if self.transform: image = self.transform(image)
            
        return image, label

class MyHackDataModule(pl.LightningDataModule):
    def __init__(self, metadata_csv, img_dir, category, transform=None, batch_size=32):
        super().__init__()
        self.metadata_csv = metadata_csv
        self.img_dir = img_dir
        self.category = category
        self.transform = transform
        self.batch_size = batch_size

    def setup(self, stage=None):
        # Initialize the datasets for training and validation
        self.train_dataset = MyHackImageDataset(self.metadata_csv, self.img_dir, self.category, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)
    
    def test_dataloader(self):
        return DataLoader(test_data, batch_size=self.batch_size, shuffle=True)
