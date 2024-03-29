from db import db
from flask import session
from datetime import datetime

def add_message(content, user_id, thread_id):
    sql = """INSERT INTO messages (content, user_id, thread_id, send_at)
             VALUES (:content, :user_id, :thread_id, NOW())"""
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()

def get_message(message_id):
    sql = "SELECT content FROM messages WHERE id=:id"
    result= db.session.execute(sql, {"id":message_id})
    return result.fetchone()[0] 

def remove_message(message_id):
    sql = "DELETE FROM messages WHERE id=:id"
    db.session.execute(sql, {"id":message_id})
    db.session.commit()

def edit_message(message_id, edited_content):
    sql = "UPDATE messages SET content=:content WHERE id=:id"
    db.session.execute(sql, {"content":edited_content, "id":message_id})
    db.session.commit()

def get_writer(message_id):
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    return result.fetchone()[0]

def get_thread(message_id):
    sql = "SELECT thread_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    return result.fetchone()[0]

def search(keyword):
    sql = """SELECT T.id, M.id, M.content, M.sent_at, T.thread_name, M.user_id, U.username FROM threads T INNER JOIN messages M ON T.id=M.thread_id 
             INNER JOIN users U ON M.user_id=U.id WHERE LOWER(M.content) LIKE LOWER(:keyword) AND T.visible=1 ORDER BY M.id DESC"""
    result = db.session.execute(sql, {"keyword":"%"+keyword+"%"})
    return result.fetchall()

