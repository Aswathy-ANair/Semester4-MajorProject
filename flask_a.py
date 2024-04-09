from flask import Flask, render_template, request  # Import request module

import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sports"
)

# Create a cursor object
cursor = conn.cursor()

@app.route('/loan_applications')
def loan_applications():
    # Fetch data from the loan_applications table
    cursor.execute("SELECT * FROM loan_applications")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # Get column names

    return render_template('loan_applications.html', data=data, columns=columns)

@app.route('/update_status', methods=['POST'])
def update_status():
    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('status_'):
                loan_id = key.split('_')[1]
                new_status = value
                # Update the status in the database
                cursor.execute("UPDATE loan_applications SET status = %s WHERE id = %s", (new_status, loan_id))
                conn.commit()
        return 'Status updated successfully'
    return 'Invalid request'

if __name__ == '__main__':
    app.run(debug=True)
