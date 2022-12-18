# Chat CS50
#### Video Demo:  <https://youtu.be/MpPZyOIY9ZM>
#### Description:

This is my final project to CS50x 2022 Course.

It's a chat application, one page only, using Javascript, Python and SQLite3 features.

When entering the site, you enter the chat room, with previous messages recorded. As a guest, you can send messages. A registration area allows you to register and select an avatar for your user. Then you can login to the site and continue the conversation. The messages are saved in the database and are reopened in a future access. A procedure in the Python program allows the exchange of messages in real time between several independent users.

In the [app.py] file are the python routines, using the flask, cs50 & werkzeug.security libraries.
In the initial access, in the root of the site (/) the DB is accessed, the previous messages are returned and the [layout.html] page is rendered.

The msg() function receives the parameters coming from the JS, which can be a new message sent by a user (a=msg) *action = new message, or a client request waiting to receive new messages (a=updt) * action = update message history.
```
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
```

The login() function receives a call from the client and validates the data to perform the login and returns success or failure.
```
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
```

Finally, the register() function receives the registration data, validate and registers the user.
```

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
```

In the [layout.html] page, resources from the bootstrap and jquery library are used, which facilitate some JS routines, and the Jinja template for the page. A (UL) tag is the main element, where messages are loaded and updated.
Below the messages, there is the menu, with the login, registration and field options to send a new message.
All functionalities, open in modal mode, inside the page, without the need to refresh all.
Receiving new messages and updating the list depends on the asynchronous function updtMsg(), which sends the request to Python and waits for the return with the new message, then call the function includeMsg() and display it on the screen.
```
    async function updtMsg() {
        // passa o horario da ultima mensagem para o servidor e aguarda nova mensagem
        let sender = document.querySelector(`#lbl_id`).innerText
        let response = await fetch(`/msg?a=updt&last=${last}`)
        let loaded = await response.json()
        // se vier nova mensagem, prepara e aciona incluiMsg para mostrar na tela
        if (loaded.message != '__none__') {
            last = loaded.created_at
            //console.log('Incluindo... ' + JSON.stringify(loaded))
            incluirMsg(loaded)
            // depois de incluir na tela, faz nova chamada para aguardar mensagem
            updtMsg()
        }
    }
```

The [chat.db] database contains the (users) and (msgs) tables to record registered users and sent messages.

[sql_cmd/create.sql] was used to create the chat.db tables.
```
-- SQLite

CREATE TABLE msgs (
	id INTEGER PRIMARY KEY,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	sender TEXT NOT NULL,
	message TEXT NOT NULL
);

CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	registered DATETIME DEFAULT CURRENT_TIMESTAMP,
	username TEXT NOT NULL,
	hash TEXT NOT NULL,
	avatar INT DEFAULT 0
);
```
[static/styles.css] was used to keep the message list responsive and some avatar effects.

