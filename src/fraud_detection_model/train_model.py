import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def train_spam_model():
    """
    Train a spam detection model.
    """
    # Load preprocessed spam data
    X, y = joblib.load('data/preprocessed_spam_data.pkl')
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Spam Detection Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    joblib.dump(model, 'models/spam_detection_model.pkl')
    print("Spam detection model saved to 'models/spam_detection_model.pkl'.")

def train_fraud_model():
    """
    Train a fraud detection model.
    """
    # Load preprocessed fraud data
    X, y = joblib.load('data/preprocessed_fraud_data.pkl')
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Fraud Detection Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    joblib.dump(model, 'models/fraud_detection_model.pkl')
    print("Fraud detection model saved to 'models/fraud_detection_model.pkl'.")

if __name__ == "__main__":
    # Train the spam detection model
    train_spam_model()
    
    # Train the fraud detection model
    train_fraud_model()
