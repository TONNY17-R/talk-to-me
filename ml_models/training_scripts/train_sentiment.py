"""
Training script for sentiment analysis model.

Trains a model to analyze sentiment in user inputs.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

def train_sentiment_model():
    """Train sentiment analysis model."""
    # Load training data
    df = pd.read_csv('datasets/uganda_mental_health.csv')
    
    # Prepare data
    X = df['text']
    y = df['sentiment']
    
    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000)),
        ('classifier', MultinomialNB())
    ])
    
    # Train model
    pipeline.fit(X, y)
    
    # Save model
    joblib.dump(pipeline, 'trained_models/sentiment_uganda.pkl')
    print("Sentiment model trained and saved")

if __name__ == '__main__':
    train_sentiment_model()
