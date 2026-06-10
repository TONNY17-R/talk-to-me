"""
Training script for Luganda NLP model.

Trains a model for Luganda language processing.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

def train_luganda_model():
    """Train Luganda language model."""
    # Load Luganda corpus
    corpus = []
    with open('datasets/luganda_corpus.txt', 'r', encoding='utf-8') as f:
        corpus = f.readlines()
    
    # Create feature extraction
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(corpus)
    
    # Train model
    model = MultinomialNB()
    model.fit(X, [0] * len(corpus))  # Placeholder labels
    
    # Save model and vectorizer
    joblib.dump(model, 'trained_models/luganda_classifier.pkl')
    joblib.dump(vectorizer, 'trained_models/luganda_vectorizer.pkl')
    print("Luganda model trained and saved")

if __name__ == '__main__':
    train_luganda_model()
