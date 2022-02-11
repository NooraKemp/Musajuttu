from app import app
from flask import abort, render_template, request, redirect, session
import users
import forums
import threads
import messages

@app.route("/")
def index():
    return render_template("index.html", forums=forums.get_forums())

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
             return render_template("error.html", message="Virheellinen käyttäjätunnus tai salasana.")
        return redirect("/") 

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1:
            return render_template("error.html", message="Käyttäjätunnus ei voi olla tyhjä.") 
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät ole samat.")
        role = request.form["role"]
        if not  users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut, yritä uudelleen.")
        return redirect("/login")

@app.route("/forum/<int:id>")
def forum(id):
    forum_name = forums.get_forum_name(id)
    return render_template("forum.html", forum_name=forum_name, id=id, threads=forums.get_forum_threads(id))

@app.route("/add_forum", methods=["post"])
def add_forum():
    users.require_role_admin(2)
    if request.method == "POST":
        forum_name = request.form["forum_name"]
        forums.add_forum(forum_name)
        return redirect("/")

@app.route("/remove_forum", methods=["post"])
def remove_forum():
    if request.method == "POST":
        forum_id = request.form["id"]
        forums.remove_forum(forum_id)
        return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    return render_template("thread.html", thread=threads.get_thread(id), id=id, messages=threads.get_thread_messages(id))

@app.route("/add_thread", methods=["get","post"])
def add_thread():
    if request.method == "POST":
        thread_name = request.form["thread_name"]
        content = request.form["content"]
        forum_id = request.form["forum_id"]
        thread_id = threads.add_thread(thread_name, content, users.user_id(), forum_id)
        return redirect("/thread/" + str(thread_id))

@app.route("/remove_thread", methods=["post"])
def remove_thread():
    if request.method == "POST":
        thread_id = request.form["id"]
        forum_id = threads.get_forum(thread_id)
        if 2 == session.get("user_role",0) or users.user_id() == threads.get_starter(thread_id):
            threads.remove_thread(thread_id)
            return redirect("/forum/" + str(forum_id))
        return render_template("error.html", message="Et voi poistaa tätä keskustelua.")  

@app.route("/edit_thread", methods=["post"])
def edit_thread():
    if request.method == "POST":
        thread_id = request.form["id"]
        content = request.form["content"]
        if 2 == session.get("user_role",0) or users.user_id() == threads.get_starter(thread_id):
            threads.edit_thread(thread_id, content)
            return redirct("/thread/" + str(thread_id))

@app.route("/add_message", methods=["post"])
def add_message():
    if request.method == "POST":
        thread_id = request.form["thread_id"]
        content = request.form["content"]
        messages.add_message(content, users.user_id(), thread_id)
        return redirect("/thread/" + str(thread_id))

@app.route("/remove_message", methods=["post"])
def remove_message():
    message_id = request.form["message_id"]
    thread_id = messages.get_thread(message_id)
    if 2 == session.get("user_role",0) or users.user_id() == messages.get_writer(message_id):
        messages.remove_message(message_id)
        return redirect("/thread/" + str(thread_id))
    return render_template("error.html", message="Et voi poistaa tätä viestiä.")

@app.route("/edit_message", methods=["post"])
def edit_message():
    message_id = request.form["message_id"]
    edited_content = request.form["edited_content"]
    thread_id = messages.get_thread(message_id)
    if 2 == session.get("user_role",0) or users.user_id() == messages.get_writer(message_id):
        messages.edit_message(message_id, edited_content)
        return redirect("/thread/" + str(thread_id))
    return render_template("error.html", message="Et voi muokata tätä viestiä.")


