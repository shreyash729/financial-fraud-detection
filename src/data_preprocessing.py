import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def preprocess_spam_data(filepath):
    """
    Preprocess the spam messages dataset.
    """
    # Load the dataset
    df = pd.read_csv(filepath)
    
    # Rename columns for clarity
    df.columns = ['label', 'message']
    
    # Convert labels to binary (spam = 1, ham = 0)
    df['label'] = df['label'].map({'spam': 1, 'ham': 0})
    
    # Split into features (X) and labels (y)
    X = df['message']
    y = df['label']
    
    # Vectorize text data using TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_vectorized = vectorizer.fit_transform(X)
    
    # Save the vectorizer for later use
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    
    return X_vectorized, y

def preprocess_fraud_data(filepath):
    """
    Preprocess the fraud call dataset.
    """
    # Load the dataset
    df = pd.read_csv(filepath, sep='\t')
    
    # Rename columns for clarity
    df.columns = ['type', 'clue']
    
    # Convert labels to binary (fraud = 1, normal = 0)
    df['type'] = df['type'].map({'fraud': 1, 'normal': 0})
    
    # Split into features (X) and labels (y)
    X = df['clue']
    y = df['type']
    
    # Vectorize text data using TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_vectorized = vectorizer.fit_transform(X)
    
    # Save the vectorizer for later use
    joblib.dump(vectorizer, 'models/tfidf_vectorizer_fraud.pkl')
    
    return X_vectorized, y

if __name__ == "__main__":
    # Preprocess spam data
    X_spam, y_spam = preprocess_spam_data('./../data/spam.csv')
    
    # Preprocess fraud data
    X_fraud, y_fraud = preprocess_fraud_data('./../data/fraud_call.file')
    
    # Save preprocessed data
    joblib.dump((X_spam, y_spam), 'data/preprocessed_spam_data.pkl')
    joblib.dump((X_fraud, y_fraud), 'data/preprocessed_fraud_data.pkl')
    
    print("Data preprocessing complete! Preprocessed data saved to 'data/'.")
