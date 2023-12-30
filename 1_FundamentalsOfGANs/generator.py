"""
The Generator for our simple MNIST GAN.
"""

import argparse
import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision as tv
from torch.utils.data import DataLoader


def save_sample_images(generator, path, cfg):
    z = z_sampler(cfg["batch_size"], cfg["z_dim"], cfg["cuda"])
    xhat = generator(z)
    xhat = F.interpolate(xhat, scale_factor=(5.0, 5.0))
    tv.utils.save_image(xhat, path)

def z_sampler(batch_size, z_dim, cudev):
    if cudev >= 0:
        z = torch.cuda.FloatTensor(batch_size, z_dim).normal_(0.0,1.0)
    else:
        z = torch.FloatTensor(batch_size, z_dim).normal_(0.0,1.0)
    return z


class Generator(nn.Module):
    def __init__(self, z_dim):
        super().__init__()
        self._fc1 = nn.Linear(z_dim, 150, bias=False)
        self._fc2 = nn.Linear(150, 784, bias=False)

        nn.init.normal_(self._fc1.weight, mean=0, std=0.1)
        nn.init.normal_(self._fc2.weight, mean=0, std=0.1)

    def forward(self, x):
        x = F.relu( self._fc1(x) )
        x = torch.sigmoid( self._fc2(x) )
        x = x.view(-1, 1, 28, 28)
        return x


def _test_main(args):
    cfg = vars(args)
    generator = Generator(z_dim=args.z_dim)
    save_sample_images(generator, "./samples/test_gen.png", cfg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--z-dim", type=int, default=100,
            help="Size of the input layer")
    parser.add_argument("--cuda", type=int, default=0,
            help="Cuda device number, select -1 for cpu")
    args = parser.parse_args()
    _test_main(args)

