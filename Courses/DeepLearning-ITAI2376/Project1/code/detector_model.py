"""
Object Detection Model
Computer Vision Project - Deep Learning ITAI2376

This module contains the implementation of an object detection model
using PyTorch and pre-trained architectures.
"""

import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms


class ObjectDetector(nn.Module):
    """
    Object Detection Model using transfer learning
    
    This model uses a pre-trained ResNet backbone for feature extraction
    and custom layers for object detection.
    """
    
    def __init__(self, num_classes=10, pretrained=True):
        """
        Initialize the Object Detector
        
        Args:
            num_classes (int): Number of object classes to detect
            pretrained (bool): Whether to use pre-trained weights
        """
        super(ObjectDetector, self).__init__()
        
        # Load pre-trained ResNet model
        self.backbone = models.resnet50(pretrained=pretrained)
        
        # Get the number of features from the backbone
        num_features = self.backbone.fc.in_features
        
        # Replace the final fully connected layer
        self.backbone.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        """
        Forward pass through the network
        
        Args:
            x (torch.Tensor): Input image tensor
            
        Returns:
            torch.Tensor: Class predictions
        """
        return self.backbone(x)
    

def get_transforms(train=True):
    """
    Get image transformation pipeline
    
    Args:
        train (bool): Whether to apply training augmentations
        
    Returns:
        torchvision.transforms.Compose: Transformation pipeline
    """
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])


def load_model(checkpoint_path, num_classes=10, device='cpu'):
    """
    Load a trained model from checkpoint
    
    Args:
        checkpoint_path (str): Path to model checkpoint
        num_classes (int): Number of classes
        device (str): Device to load model on
        
    Returns:
        ObjectDetector: Loaded model
    """
    model = ObjectDetector(num_classes=num_classes, pretrained=False)
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    return model


if __name__ == "__main__":
    # Example usage
    print("Initializing Object Detector...")
    model = ObjectDetector(num_classes=10)
    
    # Create a dummy input
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # Forward pass
    output = model(dummy_input)
    print(f"Output shape: {output.shape}")
    print("Model initialized successfully!")
