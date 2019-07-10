from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
    
@app.route("/")
def index():
    mysql = connectToMySQL('emails')	        # call the function, passing in the name of our db
    all_emails = mysql.query_db('SELECT * FROM email_table;')  # call the query_db function, pass in the query as a string
    return render_template("/index.html", all_emails = all_emails)

@app.route("/create_email", methods = ["POST"])
def create_user():
    session['result'] = []
    if not EMAIL_REGEX.match(request.form['user_email']):    # test whether a field matches the pattern
        flash("Email is not valid!")
        return redirect("/")

    mysql = connectToMySQL('emails')
    query = "INSERT INTO email_table (email) VALUES (%(mail)s);"

    data = {
        "mail": request.form['user_email']
    }

    ent = request.form['user_email']

    new_player = mysql.query_db(query, data)
    mysql = connectToMySQL('emails')
    all_emails = mysql.query_db('SELECT * FROM email_table;')  
    return render_template("/success.html", all_emails = all_emails, ent = ent)

if __name__ == "__main__":
    app.run(debug=True)