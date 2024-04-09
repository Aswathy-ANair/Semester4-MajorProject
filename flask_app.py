import pandas as pd
from flask import Flask, render_template, request
import mysql.connector

# Import predict_loan_approval function from loan.py
from loan import predict_loan_approval

# Initialize Flask app
app = Flask(__name__)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="sports",
)

# Load the dataset
loan_data = pd.read_csv('loan_prediction.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the form
    account_number = request.form['account_number']
    gender = request.form['gender']
    married = request.form['married']
    dependents = request.form['dependents']
    education = request.form['education']
    self_employed = request.form['self_employed']
    applicant_income = float(request.form['applicant_income'])
    coapplicant_income = float(request.form['coapplicant_income'])
    loan_amount = float(request.form['loan_amount'])
    loan_amount_term = float(request.form['loan_amount_term'])
    credit_history = float(request.form['credit_history'])
    property_area = request.form['property_area']

    # Make prediction using loan.py
    prediction = predict_loan_approval(account_number, gender, married, dependents, education, self_employed,
                                       applicant_income,
                                       coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area)

    # Check if the predicted status is 'Y' in the dataset for approval
    if prediction == 1:  # 1 represents 'Y' in the dataset
        message = 'Congratulations! Your loan is approved.'
    else:
        message = 'Sorry, your loan application is not approved.'

    # Store the submitted data into the MySQL database
    try:
        cursor = conn.cursor()
        # SQL query to insert data into the table
        sql = "INSERT INTO loan_applications (account_number, gender, married, dependents, education, self_employed, applicant_income, coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area, status, mlpredict) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Execute the SQL query
        cursor.execute(sql, (
        account_number, gender, married, dependents, education, self_employed, applicant_income, coapplicant_income,
        loan_amount, loan_amount_term, credit_history, property_area, 'pending', message))

        # Commit changes to the database
        conn.commit()
    except Exception as e:
        # Rollback in case of any error
        conn.rollback()
        raise e
    finally:
        # Close the cursor
        cursor.close()

    return render_template('result.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
