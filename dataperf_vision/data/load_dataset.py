import boto3
import botocore
import csv
import re
import os
import random

import logging

logger = logging.getLogger(__name__)

BUCKET_NAME = 'open-images-dataset'
REGEX = r'(test|train|validation|challenge2018)/([a-fA-F0-9]*)'

def load_train_dataset(config):
    return load_dataset(config["data"]["train"]["path"], config)

def load_test_dataset(config):
    return load_dataset(config["data"]["test"]["path"], config)

def load_dataset(dataset_path, config):

    bucket = boto3.resource(
      's3', config=botocore.config.Config(
          signature_version=botocore.UNSIGNED)).Bucket(BUCKET_NAME)

    count = 0

    with open(dataset_path) as dataset_file:
        dataset_csv = csv.reader(dataset_file)
        header = next(dataset_csv)

        samples = []

        for sample in dataset_csv:
            sample_dict = { field_name : value for field_name, value in zip(header, sample) }

            samples.append(sample_dict)

        generator = random.Random(42)

        generator.shuffle(samples)

        for sample_dict in samples:
            logger.debug("Loading sample: " + str(sample_dict))

            try:
                sample_dict["image_path"] = get_openimages_image(sample_dict["image_id"], bucket, config)

                count += 1

                yield sample_dict
            except botocore.exceptions.ClientError as exception:
                logger.debug("Skipping image...")
                pass

            if count > config["data"]["max_size"]:
                break

def get_openimages_image(image_id, bucket, config):
    download_folder = config["data"]["cache_directory"]

    split, local_image_id = check_and_homogenize_one_image(image_id)

    download_one_image(bucket, split, local_image_id, download_folder)

    return os.path.join(download_folder, f'{local_image_id}.jpg')

def check_and_homogenize_one_image(image):
    split, image_id = re.match(REGEX, "train/" + image).groups()
    return split, image_id

def download_one_image(bucket, split, image_id, download_folder):

    os.makedirs(download_folder, exist_ok=True)

    try:
        bucket.download_file(f'{split}/{image_id}.jpg',
                         os.path.join(download_folder, f'{image_id}.jpg'))
    except botocore.exceptions.ClientError as exception:
        logger.error(f'ERROR when downloading image `{split}/{image_id}`: {str(exception)}')
        raise

