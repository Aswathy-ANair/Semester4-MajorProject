import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score




# Load the dataset
data = pd.read_csv('loan_prediction.csv')

# Preprocessing
data.fillna(method='ffill', inplace=True)  # Forward fill missing values
data = pd.get_dummies(data, drop_first=True)  # One-hot encoding for categorical variables

# Split the data into features and target variable
X = data.drop('Loan_Status_Y', axis=1)
y = data['Loan_Status_Y']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Define a function to predict loan approval
def predict_loan_approval(account_number,gender, married, dependents, education, self_employed, applicant_income,
                          coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area):
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'AccountNumber': [account_number] if account_number else [None],
        'Gender': [gender],
        'Married': [married],
        'Dependents': [dependents],
        'Education': [education],
        'Self_Employed': [self_employed],
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [coapplicant_income],
        'LoanAmount': [loan_amount],
        'Loan_Amount_Term': [loan_amount_term],
        'Credit_History': [credit_history],
        'Property_Area': [property_area]
    })

    # Perform one-hot encoding for categorical variables
    input_data = pd.get_dummies(input_data)

    # Ensure input data has the same columns as the training data
    input_data = input_data.reindex(columns=X.columns, fill_value=0)

    # Make prediction
    prediction = model.predict(input_data)

    # Return the prediction result
    return prediction[0]
