
import torch
import torch.nn as nn

from PIL import Image
from torchvision import transforms

import logging

logger = logging.getLogger(__name__)

def get_embeddings(dataset, config):

    model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=True)

    # remove last fully-connected layer
    new_classifier = nn.Sequential(*list(model.classifier.children())[:-1])
    model.classifier = new_classifier

    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    for sample in dataset:
        new_sample = sample.copy()

        input_image = Image.open(new_sample["image_path"]).convert(mode='RGB')
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        with torch.no_grad():
            output = model(input_batch)

        logger.debug("Got embeddings: " + str(output))

        new_sample["embeddings"] = output

        yield new_sample

