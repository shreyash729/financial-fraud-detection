# AWS Fraud Detection System

This project is a modular system for detecting fraud and spam in real-time using AWS services and machine learning. It includes preprocessing scripts, model training, and integration with AWS Lambda for real-time analysis.

## Features
- **Spam Detection**: Detects spam messages using a trained machine learning model.
- **Fraud Detection**: Detects fraudulent calls by analyzing call transcripts.
- **Real-Time Alerts**: Sends real-time alerts using AWS SNS when fraud is detected.
- **Scalable**: Built on AWS services, making it highly scalable and cost-effective.


## Datasets
1. **spam_messages.csv**:
   - `v1`: Label (spam/ham)
   - `v2`: Message text

2. **fraud_call.tsv**:
   - `type`: Label (fraud/normal)
   - `clue`: Call transcript or message

## Setup Instructions

### Prerequisites
- Python 3.8+
- AWS Account
- AWS CLI configured

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shreyash729/financial-fraud-detection.git
   cd financial-fraud-detection

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Preprocess the data:
    ```bash
    python src/data_preprocessing.py
    ```
4. Train the models:
    ```bash
    python src/train_model.py
    ```


## Usage

1. Test the models:
    ```bash
    jupyter notebook notebooks/example_usage.ipynb
    ```

2. Deploy to AWS:
   1. Zip the lambda_handler.py script:
    ```bash
    zip lambda_handler.zip src/lambda_handler.py
    ```
   2. Upload the zip file to AWS Lambda.
   3. Configure triggers (e.g., Amazon Connect → AWS Lambda).    



## Contribution
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request for review.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any questions or support, please contact [shreyash70019@gmail.com](mailto:shreyash70019@gmail.com).

