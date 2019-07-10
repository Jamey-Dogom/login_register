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
    session = []
    # mysql = connectToMySQL('site_users')	        # call the function, passing in the name of our db
    # mysql.query_db('SELECT * FROM site_user;')  # call the query_db function, pass in the query as a string
    return render_template("/index.html")

@app.route("/create_user", methods = ["POST"])
def create_user():
    session['result'] = []
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Email is not valid!")
        return redirect("/")

    mysql = connectToMySQL('site_users')
    query = "INSERT INTO site_user (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(mail)s, %(pw)s);"

    data = {
        "fn": request.form['first_name'],
        "ln": request.form['last_name'],
        "mail": request.form['email'],
        "pw": request.form['password']
    }

    print(data)

    mysql.query_db(query, data)
    return render_template("/success.html")

if __name__ == "__main__":
    app.run(debug=True)