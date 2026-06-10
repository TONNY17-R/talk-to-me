"""
Training script for crisis detection model.

Trains a model to detect crisis indicators in text.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import joblib

def train_crisis_model():
    """Train crisis detection model."""
    # Load training data
    df = pd.read_csv('datasets/crisis_keywords.json', orient='records')
    
    # Prepare data
    texts = []
    labels = []
    for _, row in df.iterrows():
        texts.append(row['text'])
        labels.append(row['risk_level'])
    
    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000)),
        ('classifier', SVC(kernel='rbf', probability=True))
    ])
    
    # Train model
    pipeline.fit(texts, labels)
    
    # Save model
    joblib.dump(pipeline, 'trained_models/crisis_detector.pkl')
    print("Crisis detector model trained and saved")

if __name__ == '__main__':
    train_crisis_model()
