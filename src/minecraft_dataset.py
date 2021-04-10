import glob
import io
import os

import numpy as np
import torch
from torch.utils.data import Dataset
from torchvision import transforms, utils


class MinecraftDataset(Dataset):
    """Minecraft Dataset"""

    def __init__(self, root_dir, image_dir, mask_dir, transform=None):
        self.root_dir = root_dir
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform

    def __len__(self):
        return len(next(os.walk(os.path.join(self.root_dir,
                                             self.image_dir)))[2])

    def __getitem__(self, idx):
        assert isinstance(idx, int)

        img_name = os.path.join(self.root_dir, self.image_dir, f'{idx}.png')
        image = io.imread(img_name)

        msk_name = os.path.join(self.root_dir, self.mask_dir, f'{idx}.png')
        mask = io.imread(msk_name)
        sample = {'image': image, 'mask': mask}

        if self.transform:
            return self.transform(sample)

        return sample


class Rescale(object):
    """Rescale the image in a sample to a given size.

    Args:
        output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image, mask = sample['image'], sample['mask']

        h, w = image.shape[:2]
        if isinstance(self.output_size, int):
            if h > w:
                new_h, new_w = self.output_size * h / w, self.output_size
            else:
                new_h, new_w = self.output_size, self.output_size * w / h
        else:
            new_h, new_w = self.output_size

        new_h, new_w = int(new_h), int(new_w)

        img = transformsIn. .resize(image, (new_h, new_w))

        # h and w are again swapped for masks because for images,
        # x and y axes are axis 1 and 0 respectively
        mask = mask * [new_w / w, new_h / h]

        return {'image': img, 'mask': mask}


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, mask = sample['image'], sample['mask']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        image = image.transpose((2, 0, 1))
        mask = mask.transpose((2, 0, 1))
        return {'image': torch.from_numpy(image),
                'mask': torch.from_numpy(mask)}
