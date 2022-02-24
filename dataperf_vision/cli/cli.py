
from dataperf_vision.data.load_dataset import load_train_dataset
from dataperf_vision.data.load_dataset import load_test_dataset

from dataperf_vision.embeddings.get_embeddings import get_embeddings
from dataperf_vision.model.train_model import train_model

from dataperf_vision.eval.report_accuracy import report_accuracy

from dataperf_vision.util.config import initialize_config_and_logging

def main():
    config = initialize_config_and_logging()

    # Get the training and test data
    training_dataset = load_train_dataset(config)
    test_dataset = load_test_dataset(config)

    # Compute embeddings
    training_embeddings = get_embeddings(training_dataset, config)
    test_embeddings = get_embeddings(test_dataset, config)

    # Train the model
    model = train_model(training_embeddings, config)

    # Report accuracy
    report_accuracy(model, test_embeddings, config)

main()



