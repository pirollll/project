# Chat CS50
#### Video Demo:  <URL HERE>
#### Description:

This is my final project to CS50x 2022 Course.

It's a chat application, one page only, using Javascript, Python and SQLite3 features.

When entering the site, you enter the chat room, with previous messages recorded. As a guest, you can send messages. A registration area allows you to register and select an avatar for your user. Then you can login to the site and continue the conversation. The messages are saved in the database and are reopened in a future access. A procedure in the Python program allows the exchange of messages in real time between several independent users.

In the [app.py] file are the python routines, using the flask, cs50 & werkzeug.security libraries.
In the initial access, in the root of the site (/) the DB is accessed, the previous messages are returned and the [layout.html] page is rendered.
The msg() function receives the parameters coming from the JS, which can be a new message sent by a user (a=msg) *action = new message, or a client request waiting to receive new messages (a=updt) * action = update message history.
The login() function receives a call from the client and validates the data to perform the login and returns success or failure.
Finally, the register() function receives the registration data, validate and registers the user.

In the [layout.html] page, resources from the bootstrap and jquery library are used, which facilitate some JS routines, and the Jinja template for the page. A (UL) tag is the main element, where messages are loaded and updated.
Below the messages, there is the menu, with the login, registration and field options to send a new message.
All functionalities, open in modal mode, inside the page, without the need to refresh all.
Receiving new messages and updating the list depends on the asynchronous function updtMsg(), which sends the request to Python and waits for the return with the new message, then call the function includeMsg() and display it on the screen.

The [chat.db] database contains the (users) and (msgs) tables to record registered users and sent messages.

[sql_cmd/create.sql] was used to create the chat.db tables.

[static/styles.css] was used to keep the message list responsive and some avatar effects.
