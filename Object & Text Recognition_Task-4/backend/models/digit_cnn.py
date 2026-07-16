"""
digit_cnn.py
-------------
A small, from-scratch Convolutional Neural Network for handwritten
digit recognition (0-9), trained on MNIST.

This is the "custom-trained module" of the project: unlike the OCR
and object-detection services (which lean on pretrained models), this
network's weights are produced entirely by train_digit_model.py in
this repository, giving the project genuine depth beyond wiring up
off-the-shelf APIs.

Architecture: two conv blocks (Conv -> BatchNorm -> ReLU -> MaxPool)
followed by a small fully-connected classifier head with dropout for
regularization. Deliberately lightweight (~130K params) so it trains
in a couple of minutes on a CPU.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class DigitCNN(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()

        # Block 1: 1x28x28 -> 16x14x14
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)

        # Block 2: 16x14x14 -> 32x7x7
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)

        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.25)

        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.bn1(self.conv1(x))))   # -> 16x14x14
        x = self.pool(F.relu(self.bn2(self.conv2(x))))   # -> 32x7x7
        x = torch.flatten(x, 1)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)                                    # raw logits
        return x

    @torch.no_grad()
    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        self.eval()
        logits = self.forward(x)
        return F.softmax(logits, dim=1)
