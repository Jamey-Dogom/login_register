from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
import re
import os
from flask_bcrypt import Bcrypt  

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
    
@app.route("/")
def index():
    if not session.get('loggedIn'):
        session['loggedIn'] = False
    print(session)
    # mysql = connectToMySQL('site_users')	        # call the function, passing in the name of our db
    # mysql.query_db('SELECT * FROM site_user;')  # call the query_db function, pass in the query as a string
    return render_template("/index.html")

@app.route("/create_user", methods = ["POST"])
def create_user():

    if len(request.form['first_name']) < 2:
        flash("First name must contain at least two letters")  

    if len(request.form['last_name']) < 2:
        flash("Last name must contain at least two letters")  

    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Email is not valid!")

    if request.form['password'] != request.form['confirm']:
        flash("Passwords don't match")


    if not '_flashes' in session.keys():
        pw_hash1 = bcrypt.generate_password_hash(request.form['password']) 
        mysql = connectToMySQL('site_users')
        query = "INSERT INTO site_user (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(mail)s, %(pw)s);"

        data = {
            "fn": request.form['first_name'],
            "ln": request.form['last_name'],
            "mail": request.form['email'],
            "pw": pw_hash1
        }

        for key, values in data.items():
            session[key] = values
        
        session['loggedIn'] = True

        print(session)

        mysql.query_db(query, data)
        return render_template("/success.html")

    return redirect("/")

@app.route("/login", methods = ["POST"])
def login():
    mysql = connectToMySQL('site_users')
    query = "SELECT * from site_user WHERE email= %(mail)s"
    data  = {
        "mail": request.form['username'],
    }
    verify = mysql.query_db(query, data)
    if(verify):
        if bcrypt.check_password_hash(verify[0]['password'], request.form['password']):
            session["fn"] = verify[0]['first_name']
            session['loggedIn'] = True
            return render_template("/success.html")
    else:
        flash("You could not be logged in")
        print("error")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)