from db import db
from flask import session

def add_thread(thread_name, content, user_id, forum_id):
    sql = """INSERT INTO threads (thread_name, content, visible, user_id, forum_id)
             VALUES (:thread_name, :content, 1, :user_id, :forum_id) RETURNING id"""
    result = db.session.execute(sql, {"thread_name":thread_name, "content":content, "user_id":user_id, "forum_id":forum_id})
    db.session.commit()
    return result

def get_thread_name(thread_id):
    sql = "SELECT thread_name FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()[0]
    
def remove_thread(thread_id):
    sql = "UPDATE threads SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def get_starter(thread_id):
    sql = "SELECT user_id  FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()[0]

def get_forum(thread_id):
    sql = "SELECT forum_id FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()[0]
