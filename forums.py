from db import db
from flask import session

def get_forums():
    sql = """SELECT F.id, F.forum_name, (SELECT COUNT(*) FROM threads T WHERE visible=1 AND T.forum_id=F.id),
             (SELECT COUNT(M.id) FROM messages M INNER JOIN threads T ON M.thread_id=T.id WHERE T.forum_id=F.id) FROM forums F WHERE visible=1 ORDER BY F.id"""
    return db.session.execute(sql).fetchall()

def get_hidden_forums():
    sql = """SELECT F.id, F.forum_name, (SELECT COUNT(*) FROM threads T WHERE visible=1 AND T.forum_id=F.id),
             (SELECT COUNT(M.id) FROM messages M INNER JOIN threads T ON M.thread_id=T.id WHERE T.forum_id=F.id) FROM forums F WHERE visible=0 ORDER BY F.id""" 
    return db.session.execute(sql).fetchall()

def add_forum(forum_name):
    sql = """INSERT INTO forums (forum_name, visible) VALUES (:forum_name, 1)"""
    db.session.execute(sql, {"forum_name":forum_name})
    db.session.commit()

def get_forum_name(forum_id):
    sql = "SELECT forum_name FROM forums WHERE id=:id"
    result = db.session.execute(sql, {"id":forum_id})
    return result.fetchone()[0]
    
def remove_forum(forum_id):
    sql = "DELETE FROM forums WHERE id=:id"
    db.session.execute(sql, {"id":forum_id})
    db.session.commit()

def hide_forum(forum_id):
    sql = "UPDATE threads SET visible=0 WHERE forum_id=:forum_id"
    db.session.execute(sql, {"forum_id":forum_id})
    db.session.commit()
    sql = "UPDATE forums SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":forum_id})
    db.session.commit()

def unhide_forum(forum_id):
    sql = "UPDATE forums SET visible=1 WHERE id=:id"
    db.session.execute(sql, {"id":forum_id})
    db.session.commit()

def get_forum_threads(forum_id):
    sql = """SELECT T.id, T.thread_name, T.created_at, T.user_id, U.username, (SELECT COUNT(*) FROM messages M WHERE M.thread_id=T.id), 
             (SELECT MAX(M.sent_at) FROM messages M WHERE M.thread_id=T.id) FROM threads T INNER JOIN users U ON T.user_id=U.id
             WHERE visible=1 AND T.forum_id=:forum_id ORDER BY T.id DESC"""
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchall()   

def get_hidden_threads(forum_id):
    sql = """SELECT T.id, T.thread_name, T.created_at, T.user_id, U.username, (SELECT COUNT(*) FROM messages M WHERE M.thread_id=T.id), 
             (SELECT MAX(M.sent_at) FROM messages M WHERE M.thread_id=T.id) FROM threads T INNER JOIN users U ON T.user_id=U.id
             WHERE visible=0 AND T.forum_id=:forum_id ORDER BY T.id DESC"""
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchall() 

def get_thread_ids(forum_id):
    sql = "SELECT id FROM threads WHERE forum_id=:forum_id"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchall() 

