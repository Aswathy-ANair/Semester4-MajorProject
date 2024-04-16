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


@app.route('/add_games', methods=['GET', 'POST'])
def add_games():
    if request.method == 'POST':
        gender = request.form['gender']
        game_name = request.form['game_name']

        try:
            # Check if the game already exists in the database
            cursor.execute("SELECT * FROM student_games WHERE game_name = %s", (game_name,))
            existing_game = cursor.fetchone()
            if existing_game:
                flash('The game already exists.', 'error')
            else:
                # Insert data into the database
                cursor.execute("INSERT INTO student_games (gender, game_name, status) VALUES (%s, %s, %s)", (gender, game_name, 'Active'))
                conn.commit()
                flash('Game added successfully!', 'success')
            return redirect('/add_games')
        except Exception as e:
            # Print or log the error for debugging
            print("Error:", e)
            # Rollback changes if an error occurs
            conn.rollback()
            flash('An error occurred while adding the game.', 'error')
            return "An error occurred while adding the game."
    else:
        return render_template('add_games.html')


@app.route('/view_houses1')
def view_houses1():
    cursor.execute("SELECT house_name FROM houses")
    house_names = [row[0] for row in cursor.fetchall()]
    return render_template('view_houses1.html', house_names=house_names)



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

    cursor.execute("SELECT house_name FROM houses WHERE status = 'Active'")
    # Fetch house names
    house_names = [row[0] for row in cursor.fetchall()]

    return render_template("registration.html", data=data, department_name='RMCA', house_names=house_names)



@app.route("/AutomobileEngineering")
def Automobile():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='AutomobileEngineering'")
    data = cursor.fetchall()
    cursor.execute("SELECT house_name FROM houses WHERE status = 'Active'")
    house_names = [row[0] for row in cursor.fetchall()]

    return render_template("registration.html", data=data, department_name='AutomobileEngineering',house_names=house_names)


@app.route("/Intmca")
def integratedmca():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='Intmca'")
    data = cursor.fetchall()
    cursor.execute("SELECT house_name FROM houses WHERE status = 'Active'")
    house_names = [row[0] for row in cursor.fetchall()]


    return render_template("registration.html", data=data, department_name='Intmca',house_names=house_names)


@app.route("/ME")
def mech():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='Mechanical Engineering'")
    data = cursor.fetchall()
    cursor.execute("SELECT house_name FROM houses WHERE status = 'Active'")
    house_names = [row[0] for row in cursor.fetchall()]


    return render_template("registration.html", data=data, department_name='Mechanical Engineering',house_names=house_names)

@app.route("/CS")
def Comps():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='Computer Science'")
    data = cursor.fetchall()
    cursor.execute("SELECT house_name FROM houses WHERE status = 'Active'")
    house_names = [row[0] for row in cursor.fetchall()]


    return render_template("registration.html", data=data, department_name='Computer Science',house_names=house_names)

@app.route("/BC")
def BCA():
    cursor.execute("SELECT * FROM mcaregistration WHERE mstudent_course='BCA'")
    data = cursor.fetchall()
    cursor.execute("SELECT house_name FROM houses WHERE status = 'Active'")
    house_names = [row[0] for row in cursor.fetchall()]


    return render_template("registration.html", data=data, department_name='BCA',house_names=house_names)

@app.route("/select_house", methods=['POST'])
def select_house():
    if request.method == 'POST':
        mstudent_id = request.form['mstudent_id']  # Assuming you have a hidden input field for student ID in your form
        house_name = request.form['house_name']

        try:
            # Update the 'assign_house' column for the student in the database
            cursor.execute("UPDATE mcaregistration SET assign_house = %s WHERE mstudent_id = %s", (house_name, mstudent_id))
            conn.commit()
            flash(f"House '{house_name}' assigned to student ID {mstudent_id} successfully.", 'success')
        except Exception as e:
            # Print or log the error for debugging
            print("Error:", e)
            # Rollback changes if an error occurs
            conn.rollback()
            flash('An error occurred while assigning the house.', 'error')

    return redirect(url_for('departments'))

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
                    session['gender'] = record[4]  # Assuming 'gender' is in the fifth column
                    return redirect(url_for('studentlog'))
                else:
                    msg = 'You do not have permission to access this page.'
            else:
                msg = 'Your account is inactive. Please contact the administrator.'
        else:
            msg = 'Incorrect username/password. Try again!'
    return render_template('logih.html', msg=msg)


@app.route('/apply', methods=['POST'])
def apply():
    if request.method == 'POST':
        # Get the student ID from the session (assuming you have stored it in the session)
        student_id = session.get('username')
        # Get the game name from the form submission
        game_name = request.form['game_name']

        try:
            # Check if the student has already applied for this game
            cursor.execute("SELECT * FROM applications WHERE student_id = %s AND game_name = %s", (student_id, game_name))
            existing_application = cursor.fetchone()
            if existing_application:
                flash('You have already applied for this game.', 'error')
            else:
                # Insert the application details into the applications table
                cursor.execute("INSERT INTO applications (student_id, game_name) VALUES (%s, %s)", (student_id, game_name))
                conn.commit()
                flash('Application submitted successfully!', 'success')
        except Exception as e:
            # Print or log the error for debugging
            print("Error:", e)
            # Rollback changes if an error occurs
            conn.rollback()
            flash('An error occurred while submitting the application.', 'error')

    # Redirect the user back to the games page after applying
    return redirect(url_for('games'))

@app.route('/delete_applied_game', methods=['POST'])
def delete_applied_game():
    if request.method == 'POST':
        # Get the student ID from the session (assuming you have stored it in the session)
        student_id = session.get('username')
        # Get the game name from the form submission
        game_name = request.form['game_name']

        try:
            # Create a cursor to execute SQL queries
            cursor = conn.cursor()

            # Delete the applied game from the database
            cursor.execute("DELETE FROM applications WHERE student_id = %s AND game_name = %s", (student_id, game_name))
            conn.commit()

            # Check if any rows were affected by the deletion
            if cursor.rowcount > 0:
                flash(f'Applied game "{game_name}" deleted successfully!', 'success')
            else:
                flash(f'Error: Applied game "{game_name}" not found or already deleted!', 'error')

            # Close the cursor
            cursor.close()

        except Exception as e:
            # Print or log the error for debugging
            print("Error:", e)
            flash('An error occurred while deleting the applied game.', 'error')

    # Redirect the user back to the games page after deleting the applied game
    return redirect(url_for('games'))


@app.route('/games')
def games():
    # Check if the user is logged in and has games stored in the session
    if 'loggedin' in session and session['loggedin'] and 'games' in session:
        # Render the games.html template and pass the games stored in the session
        return render_template('games.html', games=session['games'])
    else:
        # If user is not logged in or games are not stored in the session, redirect to login page
        return redirect(url_for('login'))



@app.route('/update_student/<int:mstudent_id>', methods=['POST'])
def update_student(mstudent_id):
    new_status = request.form['status']
    new_house = request.form['house_name']
    try:
        cursor.execute("UPDATE mcaregistration SET status = %s, assign_house = %s WHERE mstudent_id = %s", (new_status, new_house, mstudent_id))
        conn.commit()
        flash('Status and Assigned House updated successfully!', 'success')
    except Exception as e:
        # Print or log the error for debugging
        print("Error:", e)
        # Rollback changes if an error occurs
        conn.rollback()
        flash('An error occurred while updating the status and assigned house.', 'error')
    return redirect(request.referrer)

@app.route('/my_games', methods=['GET', 'POST'])
def my_games():
    if request.method == 'GET':
        # Get the student's applied games from the database
        student_id = session.get('username')
        cursor.execute("SELECT game_name FROM applications WHERE student_id = %s", (student_id,))
        applied_games = cursor.fetchall()
        return render_template('my_games.html', applied_games=applied_games)
    elif request.method == 'POST':
        # Handle game deletion
        game_name = request.form['game_name']
        student_id = session.get('username')
        try:
            cursor.execute("DELETE FROM applications WHERE student_id = %s AND game_name = %s", (student_id, game_name))
            conn.commit()
            flash('Game deleted successfully!', 'success')
        except Exception as e:
            print("Error:", e)
            conn.rollback()
            flash('An error occurred while deleting the game.', 'error')
        return redirect(url_for('my_games'))




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
            insert_query = "INSERT INTO houses (house_name, status) VALUES (%s, 'Active')"
            cursor.execute(insert_query, (house_name,))
            conn.commit()
            return redirect(url_for('add_house'))
        except Exception as e:
            return "An error occurred: " + str(e)
    else:
        return render_template('add_house1.html')

# Route for viewing and updating house status
# Route for viewing and updating house status
# Route for viewing and updating house status
@app.route('/view_houses', methods=['GET', 'POST'])
def view_houses():
    if request.method == 'POST':
        house_id = request.form['house_id']
        new_name = request.form['new_name']
        status = request.form['status']
        cursor = conn.cursor()
        cursor.execute("UPDATE houses SET house_name = %s, status = %s WHERE house_id = %s", (new_name, status, house_id))
        conn.commit()
        cursor.close()
        return redirect(url_for('view_houses'))

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM houses")
    houses = cursor.fetchall()
    cursor.close()
    return render_template('view_houses.html', houses=houses)







@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('You were successfully logged out.', 'success')
    return redirect(url_for('login'))





if __name__ == "__main__":
    app.run(debug=True)

