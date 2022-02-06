from app import app
from flask import abort, render_template, request, redirect, session
import users
import forums
import threads

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
        return redirect("/")

@app.route("/forum/<int:id>")
def forum(id):
    forum_name = forums.get_forum_name(id)
    return render_template("forum.html", forum_name=forum_name, id=id, threads=forums.get_forum_threads(id))

@app.route("/add_forum", methods=["get", "post"])
def add_forum():
    users.require_role_admin(2)
    if request.method == "POST":
        forum_name = request.form["forum_name"]
        forums.add_forum(forum_name)
        return redirect("/")

@app.route("/remove_forum", methods=["get", "post"])
def remove_forum():
    if request.method == "POST":
        forum_id = request.form["id"]
        forums.remove_forum(forum_id)
        return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    thread_name = threads.get_thread_name(id)
    return render_template("thread.html", thread_name=thread_name, id=id)

@app.route("/add_thread", methods=["get", "post"])
def add_thread():
    if request.method == "POST":
        thread_name = request.form["thread_name"]
        content = request.form["content"]
        forum_id = request.form["forum_id"]
        thread_id = threads.add_thread(thread_name, content, users.user_id(), forum_id)
        return redirect("/forum/" + str(forum_id))

@app.route("/remove_thread", methods=["get", "post"])
def remove_thread():
    if request.method == "POST":
        thread_id = request.form["id"]
        forum_id = threads.get_forum(thread_id)
        if 2 == session.get("user_role",0) or users.user_id() == threads.get_starter(thread_id):
            threads.remove_thread(thread_id)
            return redirect("/forum/" + str(forum_id))
        return render_template("error.html", message="Et voi poistaa tätä keskustelua.")  
