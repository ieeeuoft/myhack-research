import torch
from torchvision import transforms

dinov2_vitl14 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14')

transform1 = transforms.Compose([
                                transforms.Resize(520),
                                transforms.CenterCrop(518), #should be multiple of model patch_size
                                transforms.ToTensor(),
                                transforms.Normalize(mean=0.5, std=0.2)
                                ])

patch_size = dinov2_vitl14.patch_size # patchsize=14

#520//14
patch_h  = 520//patch_size
patch_w  = 520//patch_size

feat_dim = 1024 # vitl14

folder_path = "harryported_giffin_images/"
total_features = []
with torch.no_grad():
    for img_path in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_path)
        img = Image.open(img_path).convert('RGB')
        img_t = transform1(img)

        features_dict = dinov2_vitl14.forward_features(img_t.unsqueeze(0))
        features = features_dict['x_norm_patchtokens']
        total_features.append(features)

total_features = torch.cat(total_features, dim=0)
total_features.shape