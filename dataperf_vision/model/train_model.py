import numpy as np
import sklearn.linear_model

import logging

logger = logging.getLogger(__name__)

def train_model(train_embeddings, config):
    embeddings = list(train_embeddings)

    label_ids = {}

    for embedding in embeddings:
        if not embedding["label_id"] in label_ids:
            label_ids[embedding["label_id"]] = len(label_ids)

    x = np.concatenate([embedding["embeddings"] for embedding in embeddings])
    y = np.asarray([label_ids[embedding["label_id"]] for embedding in embeddings], dtype=np.int)

    logger.debug("x shape: " + str(x.shape))
    logger.debug("y shape: " + str(y.shape) + " " + str(y))

    model = sklearn.linear_model.LogisticRegression()
    model.fit(x, y)

    return model

