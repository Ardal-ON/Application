#!/usr/bin/env python3
"""
Machine Learning Model Training Script for Engine Condition Prediction

This script loads data, preprocesses it, trains multiple models, evaluates them,
and saves the best performing model.

Dataset Source: Automotive Vehicles Engine Health Dataset
URL: https://www.kaggle.com/datasets/parvmodi/automotive-vehicles-engine-health-dataset/data
"""

import logging
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pickle
import warnings

warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    A class to handle the complete machine learning pipeline for engine condition prediction.
    """

    def __init__(self, data_path=None, test_size=0.2, random_state=20):
        """
        Initialize the ModelTrainer.

        Args:
            data_path (str): Path to the dataset CSV file
            test_size (float): Proportion of dataset to include in test split
            random_state (int): Random state for reproducibility
        """
        self.data_path = data_path
        self.test_size = test_size
        self.random_state = random_state
        self.df = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.best_accuracy = 0

    def load_data(self):
        """
        Load data from the engine_data.csv file.

        Dataset Source: Automotive Vehicles Engine Health Dataset
        URL: https://www.kaggle.com/datasets/parvmodi/automotive-vehicles-engine-health-dataset/data

        This dataset contains engine health parameters including:
        - Engine rpm: Engine revolutions per minute
        - Lub oil pressure: Lubricating oil pressure
        - Fuel pressure: Fuel system pressure
        - Coolant pressure: Engine coolant pressure
        - lub oil temp: Lubricating oil temperature
        - Coolant temp: Engine coolant temperature
        - Engine Condition: Binary classification (0: Normal, 1: Faulty)
        """
        logger.info("Loading dataset from engine_data.csv...")

        # Set default data path if not provided
        if not self.data_path:
            self.data_path = "data/engine_data.csv"

        # Check if the data file exists
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at: {self.data_path}")

        # Load the dataset
        self.df = pd.read_csv(self.data_path)

        logger.info(f"Dataset loaded with shape: {self.df.shape}")
        return self.df

    def preprocess_data(self):
        """
        Clean and preprocess the data by removing outliers and handling missing values.
        """
        logger.info("Preprocessing data...")

        # Remove outliers using IQR method
        for column in self.df.columns:
            if column == "Engine Condition":
                continue

            percentile25 = self.df[column].quantile(0.25)
            percentile75 = self.df[column].quantile(0.75)
            iqr = percentile75 - percentile25

            upper_limit = percentile75 + 1.5 * iqr
            lower_limit = percentile25 - 1.5 * iqr

            outlier_count = len(self.df[self.df[column] > upper_limit]) + len(
                self.df[self.df[column] < lower_limit]
            )
            logger.info(f"Outliers in {column}: {outlier_count}")

            # Replace outliers with NaN
            self.df[column] = np.where(
                self.df[column] > upper_limit,
                np.nan,
                np.where(self.df[column] < lower_limit, np.nan, self.df[column]),
            )

        # Drop rows with missing values
        self.df = self.df.dropna().reset_index(drop=True)
        logger.info(f"Data shape after preprocessing: {self.df.shape}")

    def split_data(self):
        """
        Split the data into features and labels, then into training and testing sets.
        """
        logger.info("Splitting data into train and test sets...")

        # Separate features and labels
        df_features = self.df.drop(["Engine Condition"], axis=1)
        df_labels = self.df["Engine Condition"]

        # Split the data
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            df_features,
            df_labels,
            test_size=self.test_size,
            random_state=self.random_state,
        )

        # Scale the features
        self.scaler = MinMaxScaler()
        self.x_train = self.scaler.fit_transform(self.x_train)
        self.x_test = self.scaler.transform(self.x_test)

        logger.info(f"Training set size: {self.x_train.shape[0]}")
        logger.info(f"Test set size: {self.x_test.shape[0]}")

    def initialize_models(self):
        """
        Initialize all the machine learning models to be trained.
        """
        logger.info("Initializing models...")

        self.models = {
            "Logistic Regression": LogisticRegression(random_state=self.random_state),
            "Decision Tree": DecisionTreeClassifier(
                max_depth=6, random_state=self.random_state
            ),
            "Random Forest": RandomForestClassifier(
                max_depth=10, random_state=self.random_state
            ),
            "K-Neighbors": KNeighborsClassifier(),
            "Gaussian Naive Bayes": GaussianNB(),
            "SVM": SVC(class_weight="balanced", random_state=self.random_state),
        }

    def train_model(self, model_name, model):
        """
        Train a single model and evaluate its performance.

        Args:
            model_name (str): Name of the model
            model: The model instance to train

        Returns:
            dict: Dictionary containing training and testing accuracies
        """
        logger.info(f"Training {model_name}...")

        # Train the model
        model.fit(self.x_train, self.y_train)

        # Make predictions
        y_pred_train = model.predict(self.x_train)
        y_pred_test = model.predict(self.x_test)

        # Calculate accuracies
        train_accuracy = accuracy_score(self.y_train, y_pred_train) * 100
        test_accuracy = accuracy_score(self.y_test, y_pred_test) * 100

        logger.info(f"{model_name} - Training accuracy: {train_accuracy:.2f}%")
        logger.info(f"{model_name} - Testing accuracy: {test_accuracy:.2f}%")

        # Update best model if this one performs better
        if test_accuracy > self.best_accuracy:
            self.best_accuracy = test_accuracy
            self.best_model = model
            self.best_model_name = model_name

        return {
            "model": model,
            "train_accuracy": train_accuracy,
            "test_accuracy": test_accuracy,
            "classification_report": classification_report(self.y_test, y_pred_test),
        }

    def train_all_models(self):
        """
        Train all initialized models and store their results.
        """
        logger.info("Training all models...")

        for model_name, model in self.models.items():
            self.results[model_name] = self.train_model(model_name, model)

        logger.info(
            f"Best model: {self.best_model_name} with training accuracy: {self.best_accuracy:.2f}%"
        )

    def print_model_comparison(self):
        """
        Print a comparison of all model performances.
        """
        logger.info("\n" + "=" * 70)
        logger.info("MODEL PERFORMANCE COMPARISON")
        logger.info("=" * 70)

        for model_name, results in self.results.items():
            logger.info(
                f"{model_name:25} | Train: {results['train_accuracy']:6.2f}% | Test: {results['test_accuracy']:6.2f}%"
            )

        logger.info("=" * 70)
        logger.info(
            f"BEST MODEL: {self.best_model_name} (Training Accuracy: {self.best_accuracy:.2f}%)"
        )
        logger.info("=" * 70)

    def save_best_model(self, save_path="models/best_model.pkl"):
        """
        Save the best performing model to disk.

        Args:
            save_path (str): Path where to save the model
        """
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the model
        with open(save_path, "wb") as f:
            pickle.dump(self.best_model, f)

        # Also save the scaler
        scaler_path = save_path.replace("best_model.pkl", "scaler.pkl")
        with open(scaler_path, "wb") as f:
            pickle.dump(self.scaler, f)

        logger.info(f"Best model ({self.best_model_name}) saved to: {save_path}")
        logger.info(f"Scaler saved to: {scaler_path}")

        # Save model metadata
        metadata = {
            "model_name": self.best_model_name,
            "training_accuracy": self.best_accuracy,
            "test_accuracy": self.results[self.best_model_name]["test_accuracy"],
            "feature_columns": list(self.df.drop(["Engine Condition"], axis=1).columns),
            "model_path": save_path,
            "scaler_path": scaler_path,
        }

        metadata_path = save_path.replace("best_model.pkl", "model_metadata.json")
        import json

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Model metadata saved to: {metadata_path}")

    def run_full_pipeline(self, data_path=None, save_model=True):
        """
        Run the complete machine learning pipeline.

        Args:
            data_path (str): Path to the dataset
            save_model (bool): Whether to save the best model
        """
        try:
            # Set data path if provided
            if data_path:
                self.data_path = data_path

            # Run the pipeline
            self.load_data()
            self.preprocess_data()
            self.split_data()
            self.initialize_models()
            self.train_all_models()
            self.print_model_comparison()

            if save_model:
                self.save_best_model()

            logger.info("Pipeline completed successfully!")

        except Exception as e:
            logger.error(f"Error in pipeline: {str(e)}")
            raise


def main():
    """
    Main function to run the model training pipeline.
    """
    logger.info("Starting Engine Condition Prediction Model Training")

    # Initialize the trainer with the data path
    trainer = ModelTrainer(
        data_path="data/engine_data.csv", test_size=0.2, random_state=20
    )

    # Run the complete pipeline
    trainer.run_full_pipeline(save_model=True)

    logger.info("Training completed!")


if __name__ == "__main__":
    main()
