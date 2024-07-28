from flask import Flask, render_template, request, redirect, url_for,session
from database import TempleDatabase
import re;
app = Flask(__name__)
app.secret_key = 'your_secret_key'
db = TempleDatabase()
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user's session data
    session.clear()
    # Redirect to the main page or login page
    return redirect(url_for('main'))

@app.route('/role_selection', methods=['POST'])
def role_selection():
    role = request.form['role']
    if role == 'user':
        return redirect(url_for('index'))
    elif role == 'admin':
        return redirect(url_for('admin_login'))  # You need to define this route for admin login
    else:
        return "Invalid role selection"
@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.is_registered(username, password):
            session['username'] = username
            return redirect(url_for('user'))
        else:
            return render_template('login.html', error=True)

    return render_template('login.html', error=False)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.is_admin(username, password):
            session['username'] = username
            return redirect(url_for('admin_functionalities'))
        else:
            return render_template('admin_login.html', error=True)
    
    return render_template('admin_login.html', error=False)

@app.route('/admin-functionalities')
def admin_functionalities():
    if 'username' in session:
        return render_template('admin_functionalities.html')
    else:
        return redirect(url_for('admin_login'))
@app.route('/select_table', methods=['GET', 'POST'])
def select_table():
    if request.method == 'POST':
        table_name = request.form['table_name']
        db.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        attributes = [row[0] for row in db.cursor.fetchall()]
        return render_template('form.html', table_name=table_name, attributes=attributes)
    return render_template('select_table.html')

@app.route('/insert', methods=['POST'])
def insert():
    table_name = request.form['table_name']
    attribute_values = [request.form[attr] for attr in request.form if attr != 'table_name']
    db.cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(attribute_values))})", attribute_values)
    return render_template('messagein.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_row():
    if request.method == 'POST':
        table_name = request.form['table_name']
        column_name = request.form['column_name']
        column_value = request.form['column_value']

        # Assuming you have an instance of DatabaseHandler named db_handler
        db.delete_row(table_name, column_name, column_value)
        return render_template('meeout.html')
    else:
        return render_template('delete_form.html')





@app.route('/view-details', methods=['GET', 'POST'])
def view_details():
    records=[]
    columns = [] 
    if request.method == 'POST':
        table_name = request.form['table_name']
        records = db.view_details(table_name)
        columns = db.column(table_name)
        return render_template('view_details.html', table_name=table_name, columns=columns, records=records)
    return render_template('view_details_form.html')



from flask import render_template

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None  # Initialize error message
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate username
        if not re.match("^[a-zA-Z]+$", username):
            error_message = 'Username should contain only alphabets (A-Z or a-z).'
        # Validate password
        elif (len(password) < 8 or 
              not any(char.isdigit() for char in password) or 
              not any(char.isalpha() for char in password) or 
              not any(char in '!@#$%^&*()-_=+{}[]|;:,.<>?`~' for char in password)):
            error_message = 'Password should contain at least 8 characters, including alphabets, numbers, and special characters.'
        else:
            # If both username and password are valid, proceed with registration
            db.register_user(username, password)
            
            return redirect(url_for('login'))
    
    return render_template('register.html', error_message=error_message)


@app.route('/user')
def user():
    
    if 'username' in session:
        return render_template('user.html')
    else:
        return redirect(url_for('login'))


@app.route('/view-temple-details')
def view_temple_details():
    temple = db.view_temple_details()
    return render_template('view_temple_details.html', temple_details=temple)

@app.route('/view-donation-details')
def view_donation_details():
    donation_details = db.view_donation_details()
    return render_template('view_donation_details.html', donation_details=donation_details)
@app.route('/view_Visitor_details')
def view_Visitor_details():
    Visitor = db.view_Visitor_details()
    return render_template('new.html', Visitor_details=Visitor)


@app.route('/view-visits')
def view_visits():
    visit_details = db.view_visits()
    return render_template('view_visits.html', visit_details=visit_details)

@app.route('/temple-most-visits')
def temple_most_visits():
    temple_details = db.temple_most_visits()
    return render_template('temple_most_visits.html', temple_details=temple_details)

@app.route('/visitor-most-visits-each-temple')
def visitor_most_visits_each_temple():
    visitor_details = db.visitor_most_visits_each_temple()
    return render_template('visitor_most_visits_each_temple.html', visitor_details=visitor_details)

@app.route('/view-visitors-based-on-purpose')
def view_visitors_based_on_purpose():
    purpose_details = db.view_visitors_based_on_purpose()
    return render_template('view_visitors_based_on_purpose.html', purpose_details=purpose_details)

@app.route('/view-visitors-based-on-gender')
def view_visitors_based_on_gender():
    gender_details = db.view_visitors_based_on_gender()
    return render_template('view_visitors_based_on_gender.html', gender_details=gender_details)

@app.route('/highest-donations')
def highest_donations():
    donation_details = db.highest_donations()
    return render_template('highest_donations.html', donation_details=donation_details)



if __name__ == '__main__':
    app.run(debug=True)
