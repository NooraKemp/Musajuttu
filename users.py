from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["user_name"] = username
            session["user_role"] = user[2]
            session["csrf_token"] = secrets.token_hex(16)
        else:
            return False

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role)"
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db,session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def user_id():
    return session.get("user_id",0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)