import os
import datetime
import pytz
import re
from hashlib import md5
from peewee import IntegrityError
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, emit
from lib.message import Message
from lib.database_tables import create_tables
from helpers import (
    auth_user,
    get_current_user,
    login_required,
    object_list,
    get_object_or_404,
)
from lib.base_model import database
from lib.user import User

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    messages = Message.select().order_by(Message.pub_date.desc())
    return object_list("index.html", messages, "message_list")


@socketio.on("message")
def handle_message(message):
    user = get_current_user()
    if message:
        new_message = Message.create(
            user=user,
            content=message,
            pub_date=datetime.datetime.now(pytz.timezone("Europe/London")),
        )
        emit(
            "new_message",
            {
                "content": new_message.content,
                "username": new_message.user.username,
                "pub_date": new_message.pub_date.strftime("%dth %B %Y, %H:%M"),
            },
            broadcast=True,
        )

        at_usernames = re.findall(r"@\w+", message)
        emails_to_notify = []
        for at_username in at_usernames:
            # Remove the @ symbol
            username = at_username[1:]
            if check_username_exists(username):
                email = get_user_email(username)
                if email:
                    emails_to_notify.append(email)

        print(emails_to_notify)


def get_user_email(username):
    try:
        user = User.get(User.username == username)
        return user.email
    except User.DoesNotExist:
        return None


def check_username_exists(username):
    return User.get_or_none(User.username == username)


@app.route("/sign_in/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST" and request.form["username"]:
        try:
            pw_hash = md5(request.form["password"].encode("utf-8")).hexdigest()
            user = User.get(
                (User.username == request.form["username"]) & (User.password == pw_hash)
            )
        except User.DoesNotExist:
            flash("The password entered is incorrect")
        else:
            auth_user(user)
            return redirect(url_for("index"))

    return render_template("users/sign_in.html")


@app.route("/sign_out/")
def sign_out():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("index"))


@app.route("/sign_up/", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST" and request.form["username"]:
        try:
            with database.atomic():
                user = User.create(
                    username=request.form["username"],
                    password=md5(
                        (request.form["password"]).encode("utf-8")
                    ).hexdigest(),
                    email=request.form["email"],
                    join_date=datetime.datetime.now(),
                )

            auth_user(user)
            return redirect(url_for("index"))

        except IntegrityError:
            flash("That username is already taken")

    return render_template("users/sign_up.html")


if __name__ == "__main__":
    create_tables()
    socketio.run(app, debug=True, port=int(os.environ.get("PORT", 5000)))
