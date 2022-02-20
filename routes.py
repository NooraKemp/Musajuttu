from app import app
from flask import abort, render_template, request, redirect, session
import users
import forums
import threads
import messages

@app.route("/")
def index():
    return render_template("index.html", forums=forums.get_forums(), hidden_forums=forums.get_hidden_forums(), online = users.get_users_online())

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
             return render_template("login.html", error=True, message="Virheellinen käyttäjätunnus tai salasana.")
        return redirect("/") 

@app.route("/logout")
def logout():
    username = users.username()
    users.logout(username)
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        available = users.username_available(username)
        if available > 0:
            return render_template("register.html", error=True, message="Käyttäjätunnus on jo käytössä.")
        if len(username) < 1:
            return render_template("register.html", error=True, message="Käyttäjätunnus ei voi olla tyhjä.")  
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(password1) < 5:
            return render_template("register.html", error=True, message="Salasanassa pitää olla vähintään 5 merkkiä.")
        if password1 != password2:
            return render_template("register.html", error=True, message="Salasanat eivät ole samat.")
        role = request.form["role"]
        if not  users.register(username, password1, role):
            return render_template("register.html", error=True, message="Rekisteröinti ei onnistunut, yritä uudelleen.")
        return redirect("/login")

@app.route("/forum/<int:id>")
def forum(id):
    forum_name = forums.get_forum_name(id)
    threads = forums.get_forum_threads(id)
    hidden_threads = forums.get_hidden_threads(id)
    return render_template("forum.html", forum_name=forum_name, id=id, threads=threads, hidden_threads=hidden_threads, online = users.get_users_online())

@app.route("/add_forum", methods=["post"])
def add_forum():
    users.require_role_admin(2)
    if request.method == "POST":
        forum_name = request.form["forum_name"]
        forums.add_forum(forum_name)
        return redirect("/")

@app.route("/hide_forum", methods=["post"])
def hide_forum():
    if request.method == "POST":
        users.check_csrf()
        forum_id = request.form["id"]
        forums.hide_forum(forum_id)
        return redirect("/")

@app.route("/unhide_forum", methods=["post"])
def unhide_forum():
    if request.method == "POST":
        users.check_csrf()
        forum_id = request.form["id"]
        forums.unhide_forum(forum_id)
        return redirect("/")

@app.route("/remove_forum", methods=["post"])
def remove_forum():
    if request.method == "POST":
        users.check_csrf()
        forum_id = request.form["id"]
        thread_ids = forums.get_thread_ids(forum_id)
        for id in thread_ids:
           threads.remove_thread(id[0])
        forums.remove_forum(forum_id)
        return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    thread = threads.get_thread(id)
    messages = threads.get_thread_messages(id)
    forum_id = threads.get_forum(id)
    forum_name = forums.get_forum_name(forum_id)
    starter_id = threads.get_starter(id)
    return render_template("thread.html", thread=thread, id=id, messages=messages, forum_id = forum_id, forum_name=forum_name,  starter_id = starter_id, online = users.get_users_online())

@app.route("/add_thread", methods=["get","post"])
def add_thread():
    if request.method == "POST":
        users.check_csrf()
        thread_name = request.form["thread_name"]
        content = request.form["content"]
        forum_id = request.form["forum_id"]
        thread_id = threads.add_thread(thread_name, content, users.user_id(), forum_id)
        return redirect("/forum/" + str(forum_id))

@app.route("/hide_thread", methods=["post"])
def hide_thread():
    if request.method == "POST":
        users.check_csrf()
        thread_id = request.form["id"]
        forum_id = threads.get_forum(thread_id)
        if 2 == session.get("user_role",0) or users.user_id() == threads.get_starter(thread_id):
            threads.hide_thread(thread_id)
        return redirect("/forum/" + str(forum_id))  

@app.route("/unhide_thread", methods=["post"])
def unhide_thread():
    if request.method == "POST":
        users.check_csrf()
        thread_id = request.form["id"]
        forum_id = threads.get_forum(thread_id)
        if 2 == session.get("user_role",0) or users.user_id() == threads.get_starter(thread_id):
            threads.unhide_thread(thread_id)
        return redirect("/forum/" + str(forum_id))

@app.route("/remove_thread", methods=["post"])
def remove_thread():
    if request.method == "POST":
        users.check_csrf()
        thread_id = request.form["id"]
        forum_id = threads.get_forum(thread_id)
        if 2 == session.get("user_role",0):
            threads.remove_thread(thread_id)
        return redirect("/forum/" + str(forum_id))  

@app.route("/edit_thread", methods=["get", "post"])
def edit_thread():
    users.check_csrf()
    thread_id = request.form["id"]
    thread = threads.get_thread(thread_id)
    thread_edit = True;
    return render_template("edit.html", thread=thread, thread_id=thread_id, thread_edit=thread_edit, online = users.get_users_online())

@app.route("/post_edited_thread", methods=["post"])
def post_edited_thread():
    if request.method == "POST":
        users.check_csrf()
        thread_id = request.form["id"]
        thread_name = request.form["thread_name"]
        content = request.form["content"]
        if 2 == session.get("user_role",0) or users.user_id() == threads.get_starter(thread_id):
            threads.edit_thread(thread_id, thread_name, content)
        return redirect("/thread/" + str(thread_id))

@app.route("/add_message", methods=["post"])
def add_message():
    if request.method == "POST":
        users.check_csrf()
        thread_id = request.form["thread_id"]
        content = request.form["content"]
        messages.add_message(content, users.user_id(), thread_id)
        return redirect("/thread/" + str(thread_id))

@app.route("/remove_message", methods=["post"])
def remove_message():
    users.check_csrf()
    message_id = request.form["message_id"]
    thread_id = messages.get_thread(message_id)
    if 2 == session.get("user_role",0) or users.user_id() == messages.get_writer(message_id):
        messages.remove_message(message_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/edit_message", methods=["get", "post"])
def edit_message():
    users.check_csrf()
    message_id = request.form["message_id"]
    message = messages.get_message(message_id)
    message_edit = True;
    return render_template("edit.html", message=message, message_id=message_id, message_edit=message_edit, online = users.get_users_online())

@app.route("/post_edited_message", methods=["post"])
def post_edited_message():
    users.check_csrf()
    message_id = request.form["message_id"]
    edited_content = request.form["content"]
    thread_id = messages.get_thread(message_id)
    if 2 == session.get("user_role",0) or users.user_id() == messages.get_writer(message_id):
        messages.edit_message(message_id, edited_content)
    return redirect("/thread/" + str(thread_id))

@app.route("/search", methods=["post"])
def search():
    keyword = request.form["keyword"]
    search_from = request.form["search_from"]
    threads_list = []
    search_threads = False;
    messages_list = []
    search_messages = False;
    if search_from == "from_threads" or search_from == "from_all":
       search_threads = True;
       threads_list = threads.search(keyword)
    if search_from == "from_messages" or search_from == "from_all":
       search_messages = True;
       messages_list = messages.search(keyword)
    if search_from == "from_threads" and len(threads_list) == 0:
       return render_template("results.html", error=True, message="Haulla ei löytynyt tuloksia.", keyword=keyword)
    if search_from == "from_messages" and len(messages_list) == 0:
       return render_template("results.html", error=True, message="Haulla ei löytynyt tuloksia.", keyword=keyword)
    if search_from == "from_all" and len(messages_list) == 0 and len(threads_list) == 0:
       return render_template("results.html", error=True, message="Haulla ei löytynyt tuloksia.", keyword=keyword)
    return render_template("results.html", messages=messages_list, keyword=keyword, threads=threads_list, search_threads=search_threads, 
                            search_messages=search_messages, online = users.get_users_online())

@app.route("/admin_functions")
def admin_functions():
    return render_template("admin-functions.html", users=users.get_users(), online = users.get_users_online())

@app.route("/add_admin", methods=["post"])
def add_admin():
    users.check_csrf()
    username = request.form["username"]
    users.add_admin(username)
    return redirect("/admin_functions")

@app.route("/remove_user", methods=["post"])
def remove_user():
    users.check_csrf()
    username = request.form["username"]
    users.remove_user(username)
    return redirect("/admin_functions")
