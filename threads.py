from db import db
from flask import session

def add_thread(thread_name, content, user_id, forum_id):
    sql = """INSERT INTO threads (thread_name, content, visible, user_id, forum_id, created_at)
             VALUES (:thread_name, :content, 1, :user_id, :forum_id, NOW()) RETURNING id"""
    result = db.session.execute(sql, {"thread_name":thread_name, "content":content, "user_id":user_id, "forum_id":forum_id}).fetchone()[0]
    db.session.commit()
    return result

def get_thread(thread_id):
    sql = "SELECT T.thread_name, T.content, T.user_id, U.username, T.created_at FROM threads T, users U WHERE T.id=:id AND T.user_id=U.id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall() 

def hide_thread(thread_id):
    sql = "UPDATE threads SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def unhide_thread(thread_id):
    sql = "UPDATE threads SET visible=1 WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def remove_thread(thread_id):
    sql = "DELETE FROM messages WHERE thread_id=:thread_id"
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
    sql = "DELETE FROM threads WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def edit_thread(thread_id, thread_name, edited_content):
    sql = "UPDATE threads SET thread_name=:thread_name, content=:content WHERE id=:id"
    db.session.execute(sql, {"thread_name":thread_name, "content":edited_content, "id":thread_id})
    db.session.commit()

def get_starter(thread_id):
    sql = "SELECT user_id  FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()[0]

def get_forum(thread_id):
    sql = "SELECT forum_id FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()[0]

def get_thread_messages(thread_id):
   sql = "SELECT M.id, M.content, M.user_id, U.username, M.send_at FROM messages M, users U WHERE M.thread_id=:thread_id AND M.user_id=U.id ORDER BY M.id"
   result = db.session.execute(sql, {"thread_id":thread_id})
   return result.fetchall() 

def search(keyword):
    sql = """SELECT T.id, T.thread_name, T.content, T.created_at, T.user_id, U.username FROM threads T, users U WHERE (LOWER(T.thread_name) LIKE LOWER(:keyword) 
             OR LOWER(T.content) LIKE LOWER(:keyword)) AND visible=1 AND T.user_id=U.id ORDER BY T.id DESC"""
    result = db.session.execute(sql, {"keyword":"%"+keyword+"%"})
    return result.fetchall()
