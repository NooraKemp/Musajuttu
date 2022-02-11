from db import db
from flask import session
from datetime import datetime

def add_message(content, user_id, thread_id):
    sql = """INSERT INTO messages (content, user_id, thread_id, send_at)
             VALUES (:content, :user_id, :thread_id, NOW())"""
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()

def remove_message(message_id):
    sql = "DELETE FROM messages WHERE id=:id"
    db.session.execute(sql, {"id":message_id})
    db.session.commit()

def edid_message(message_id, edited_content):
    if users.user_id == get_writer(message_id):
        sql = "UPDATE messages SET content:content WHERE id:id"
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
