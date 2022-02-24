
# Dataperf Vision Creation Reference

Submitters compete to generate the best training dataset.

This benchmark:

 * User submits images to train on
 * Embeddings are computed for each image using Mobilenet
 * A linear regression model is trained on the embeddings for the user images
 * The same model is evaluated on a test set from Cats4ML
 * Average accuracy on all Cats4ML classes is reported

## Optimizations

To save compute costs and upload bandwidth, users can submit the embeddings
for their images instead of the images themselves.

To prevent cheating, they should also make their images available so that
it is possible to verify that the embeddings match their images.

# Installation

## Install docker

The only dependency is docker.  Follow the instructions at:

```
https://docs.docker.com/get-docker

```

## Clone this repo

```
git clone git@github.com:greg1232/dataperf-vision-creation.git
```

# Run

The run script will run download the required data, train, and evaluate a reference model.

```
    ./run_benchmark
```

# Exploring the code

Start by looking at: dataperf_vision/cli/cli.py

