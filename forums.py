from db import db
from flask import session

def get_forums():
    sql = "SELECT forum_name, id FROM forums WHERE visible=1 ORDER BY id" 
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
    sql = "UPDATE forums SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":forum_id})
    db.session.commit()

def get_forum_threads(forum_id):
   sql = "SELECT id, thread_name FROM threads WHERE visible=1 AND forum_id=:forum_id"
   result = db.session.execute(sql, {"forum_id":forum_id})
   return result.fetchall()   
