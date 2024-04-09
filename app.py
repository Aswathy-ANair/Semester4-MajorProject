# app.py
from flask import request
from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
from flask import render_template, request, redirect, url_for, session
from flask import flash

conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="", database="sports")
cursor = conn.cursor()
from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd


app = Flask(__name__)
app.secret_key = "super secret key"

app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'templates'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sports"  # Change to your database name
)

cursor = conn.cursor()


@app.route('/index')
def index():
    # Set The upload HTML template '\templates\index1.html'
    return render_template('index1.html')



# Get the uploaded files
from flask import flash

@app.route("/uploadFiles", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        parseCSV(file_path)
        flash('File uploaded successfully!', 'success')  # Flash success message
    else:
        flash('No file selected!', 'error')  # Flash error message for no file selected
    return redirect(url_for('index'))



def parseCSV(filePath):
    # CVS Column Names
    col_names = ['mstudent_name', 'mstudent_gender', 'mstudent_city', 'mstudent_email', 'mstudent_contact',
                 'mstudent_course']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    # Loop through the Rows
    for i, row in csvData.iterrows():
        sql = "INSERT INTO mcaregistration (mstudent_name, mstudent_gender, mstudent_city, mstudent_email, mstudent_contact, mstudent_course) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (row['mstudent_name'], row['mstudent_gender'], row['mstudent_city'], row['mstudent_email'],
                 row['mstudent_contact'], row['mstudent_course'])
        cursor.execute(sql, value)
        conn.commit()
        print(i, row['mstudent_name'], row['mstudent_gender'], row['mstudent_city'], row['mstudent_email'],
              row['mstudent_contact'], row['mstudent_course'])

@app.route("/departments")
def departments():
    return render_template("admin_dash.html", username=session.get('username'))

@app.route("/studentlog")
def studentlog():
    return render_template("student_home.html", username=session.get('username'))

@app.route("/students")
def students():
    return render_template("departments.html")

@app.route("/RMCA")
def mcar():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='RMCA'")
    data = cursor.fetchall()
    return render_template("registration.html", data=data, department_name='RMCA')



@app.route("/AutomobileEngineering")
def Automobile():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='AutomobileEngineering'")
    data = cursor.fetchall()
    return render_template("registration.html", data=data, department_name='AutomobileEngineering')


@app.route("/Intmca")
def integratedmca():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='Intmca'")
    data = cursor.fetchall()

    return render_template("registration.html", data=data, department_name='Intmca')


@app.route("/ME")
def mech():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='Mechanical Engineering'")
    data = cursor.fetchall()

    return render_template("registration.html", data=data, department_name='Mechanical Engineering')

@app.route("/CS")
def Comps():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='Computer Science'")
    data = cursor.fetchall()

    return render_template("registration.html", data=data, department_name='Computer Science')

@app.route("/BC")
def BCA():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='BCA'")
    data = cursor.fetchall()

    return render_template("registration.html", data=data, department_name='BCA')

# Define other routes similarly

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username, password))
        record = cursor.fetchone()
        if record:
            # Check if the status is active
            if record[3] == 'Active':  # Assuming status is in the fourth column
                # Assuming user_type is in the third column
                if record[2] == 'admin':
                    session['loggedin'] = True
                    session['username'] = record[0]
                    return redirect(url_for('departments'))
                elif record[2] == 'student':
                    session['loggedin'] = True
                    session['username'] = record[0]
                    return redirect(url_for('studentlog'))
                else:
                    msg = 'You do not have permission to access this page.'
            else:
                msg = 'Your account is inactive. Please contact the administrator.'
        else:
            msg = 'Incorrect username/password. Try again!'
    return render_template('logih.html', msg=msg)



@app.route('/update_status/<int:mstudent_id>', methods=['POST'])
def update_status(mstudent_id):
    new_status = request.form['status']
    try:
        cursor.execute("UPDATE mcaregistration SET status = %s WHERE mstudent_id = %s", (new_status, mstudent_id))
        conn.commit()
        flash('Status updated successfully!', 'success')
    except Exception as e:
        # Print or log the error for debugging
        print("Error:", e)
        # Rollback changes if an error occurs
        conn.rollback()
        flash('An error occurred while updating the status.', 'error')
    return redirect(request.referrer)



@app.route('/profile')
def profile():
    if 'loggedin' in session and session['loggedin']:
        # Fetch the username of the logged-in user from the session
        username = session.get('username')
        print("Username from session:", username)  # Debugging

        # Fetch the student's details from the mcaregistration table based on the username
        cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_id = %s", (username,))
        student_data = cursor.fetchone()
        print("Student data:", student_data)  # Debugging

        if student_data:
            # If student data is found, render the profile template with the data
            return render_template('stprofile.html', student_data=student_data)
        else:
            # If no student data is found, redirect to a page indicating the profile is not available
            flash('Student profile not found.', 'error')
            return redirect(url_for('index'))
    else:
        # If user is not logged in, redirect them to the login page
        return redirect(url_for('login'))


import re

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Retrieve current password from database
        username = session['username']
        cursor.execute('SELECT password FROM user WHERE username=%s', (username,))
        current_password = cursor.fetchone()[0]

        # Verify old password
        if old_password != current_password:
            flash('Incorrect old password. Please try again.', 'error')
            # Fetch student data again for rendering the profile template
            cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_id = %s", (username,))
            student_data = cursor.fetchone()
            return render_template('stprofile.html', student_data=student_data)

        # Check if new password matches confirm password
        if new_password != confirm_password:
            flash('New password and confirm password do not match.', 'error')
            # Fetch student data again for rendering the profile template
            cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_id = %s", (username,))
            student_data = cursor.fetchone()
            return render_template('stprofile.html', student_data=student_data)

        # Check if new password is at least 12 characters long
        if len(new_password) < 12:
            flash('New password must be at least 12 characters long.', 'error')
            # Fetch student data again for rendering the profile template
            cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_id = %s", (username,))
            student_data = cursor.fetchone()
            return render_template('stprofile.html', student_data=student_data)

        # Check if new password contains a mix of letters, numbers, and special characters
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$', new_password):
            flash('New password must contain at least one letter, one number, one special character, and be at least 12 characters long.', 'error')
            # Fetch student data again for rendering the profile template
            cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_id = %s", (username,))
            student_data = cursor.fetchone()
            return render_template('stprofile.html', student_data=student_data)

        # Update password in the database
        cursor.execute('UPDATE user SET password=%s WHERE username=%s', (new_password, username))
        conn.commit()

        flash('Password updated successfully.', 'success')

    # Fetch student data for rendering the profile template
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_id = %s", (username,))
    student_data = cursor.fetchone()
    return render_template('stprofile.html', student_data=student_data)


@app.route('/reset_password_form', methods=['GET'])
def reset_password_form():
    return render_template('reset_password.html')

# Route for handling the password reset request
@app.route('/reset_password', methods=['POST'])

def reset_password():
    # Get the form data
    username = request.form.get('username')
    phone_number = request.form.get('phone')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Password validation
    if (
        len(new_password) < 12
        or not re.search(r'[A-Za-z]', new_password)  # Check for characters
        or not re.search(r'\d', new_password)        # Check for numbers
        or not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password)  # Check for special symbols
    ):
        flash("Password must contain at least 12 characters, including characters, numbers, and special symbols.", 'error')
        return redirect(url_for('reset_password_form'))

    # Query the database to verify the username and phone number
    query = "SELECT * FROM user WHERE username = %s AND phone = %s"
    cursor.execute(query, (username, phone_number))
    user = cursor.fetchone()

    # Check if the user exists and if the new password matches the confirm password
    if user and new_password == confirm_password:
        # Update the password in the database
        update_query = "UPDATE user SET password = %s WHERE username = %s AND phone = %s"
        cursor.execute(update_query, (new_password, username, phone_number))
        conn.commit()
        flash("Password reset successfully for user {}".format(username), 'success')
        return redirect(url_for('reset_password_form'))
    else:
        flash("Username or phone number is incorrect, or new password does not match confirm password.", 'error')
        return redirect(url_for('reset_password_form'))


@app.route('/add_house', methods=['POST', 'GET'])
def add_house():
    if request.method == 'POST':
        house_name = request.form['house_name']

        try:
            # Execute INSERT query to add house to the table
            insert_query = "INSERT INTO houses (house_name) VALUES (%s)"
            cursor.execute(insert_query, (house_name,))
            conn.commit()
            # Redirect to a different page after successfully adding the house
            return redirect(url_for('add_house'))
        except Exception as e:
            # Handle database error
            return "An error occurred: " + str(e)
    else:
        return render_template('add_house1.html')



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('You were successfully logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

