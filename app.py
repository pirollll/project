import time

from cs50 import SQL
from flask import Flask, render_template, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///chat.db")


@app.route("/")
def index():

    messages = db.execute('SELECT created_at, message, sender, avatar FROM msgs INNER JOIN users ON msgs.sender = users.username OR msgs.sender LIKE "Guest%" GROUP BY created_at ORDER BY created_at')
    return render_template("layout.html", messages=messages)


@app.route("/msg", methods=["GET", "POST"])
def msg():

    if (request.args.get("a") == "msg"):
        msg = {
            "sender": request.args.get("sender"),
            "message": request.args.get("message"),
        }
        newMessage = db.execute("INSERT INTO msgs (sender, message) VALUES (?, ?)", msg["sender"], msg["message"])
        return msg

    elif (request.args.get("a") == "updt"):
        msgNova = False
        msg = {
            "sender": '__none__',
            "message": '__none__',
        }
        while(msgNova == False):
            nonew = db.execute('SELECT EXISTS (SELECT 1 FROM msgs)')
            if 1 in nonew[0].values():
                check = db.execute('SELECT created_at, message, sender, avatar FROM msgs INNER JOIN users on msgs.sender = users.username OR msgs.sender LIKE "Guest%" ORDER BY created_at DESC LIMIT 1')
                if request.args.get('last') != check[0]['created_at']:
                    if not str(check[0]['avatar']).isnumeric():
                        check[0]['avatar'] = 0
                    msgNova = True    
                    return check[0]
                if msgNova == False:
                    time.sleep(1) 
                    #return msg
            else:
                time.sleep(1)
                

@app.route("/login", methods=["GET", "POST"])
def login():

    reqdata = request.get_json()
    user_login = {
        "username": reqdata['username'], 
        "password": reqdata['password'], 
    }

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not user_login['username']:
            user_login['status'] = "verify username"
            return user_login

        # Ensure password was submitted
        elif not user_login['password']:
            user_login['status'] = "verify password"
            return user_login

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", user_login['username'])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], user_login['password']):
            user_login['status'] = "wrong user or password"
            return user_login

        user_login = {
            "user_id": rows[0]["id"],
            "username": reqdata['username'],
            "status": 'Success',
        }
    
    return user_login


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    reqdata = request.get_json()
    user_reg = {
        "username": reqdata['username'], 
        "password": reqdata['password'],
        "confirmation": reqdata['confirmation'],
        "avatar": reqdata['avatar'],
        "status": "__none__"
    }

    if request.method == "POST":
        if not reqdata['username']:
            user_reg['status'] = "username"
            return user_reg
        elif not reqdata['password']:
            user_reg['status'] = "password"
            return user_reg
        elif reqdata['password'] != reqdata['confirmation']:
            user_reg['status'] = "wrong password"
            return user_reg

        user_exists = db.execute("SELECT * FROM users WHERE username = ?", reqdata['username'])
        if len(user_exists) != 0:
            user_reg['status'] = "choose another user"
            return user_reg

        db.execute("INSERT INTO users (username, hash, avatar) VALUES (?, ?, ?)", reqdata['username'], generate_password_hash(reqdata['password']), reqdata['avatar'])
        user_reg['status'] = "Success"
    
    return user_reg

