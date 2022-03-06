import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    online = is_online(username);
    if online == 0:
        sql = """INSERT INTO onlineUsers (username)
             VALUES (:username)"""
    db.session.execute(sql, {"username":username})
    db.session.commit()
    return True

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username, password, role)
                 VALUES (:username, :password, :role)"""
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return True

def logout(username):
    sql = "DELETE FROM onlineUsers WHERE username=:username"
    db.session.execute(sql, {"username":username})
    db.session.commit()
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def get_users():
     sql = "SELECT id, username, role FROM users"
     return db.session.execute(sql).fetchall()

def get_users_online():
     sql = "SELECT username FROM onlineUsers"
     return db.session.execute(sql).fetchall()

def is_online(username):
    sql = "SELECT COUNT(*) FROM onlineUsers WHERE username=:username"
    result= db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def user_id():
    return session.get("user_id",0)

def username():
    return session.get("user_name")

def add_admin(username):
    sql = "UPDATE users SET role=2 WHERE username=:username"
    db.session.execute(sql, {"username":username})
    db.session.commit()

def remove_user(username):
    sql = "DELETE FROM users WHERE username=:username"
    db.session.execute(sql, {"username":username})
    db.session.commit()

def username_available(username):
    sql = "SELECT COUNT(*) FROM users WHERE username=:username"
    result= db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def require_role_admin(role):
    if role > session.get("user_role",0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
