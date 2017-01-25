import sqlite3

from datetime import datetime

#the db location
f="data/users.db"


'''
this fxn updates the db enteries corresponding to their schedule
a list of locations (schedule) is passed in
and the fxn removes the old db entry, and makes a new one that is now relevant
'''
def addCall(caller, user):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('UPDATE users SET calls = "' + user + '"WHERE username = "' + caller + '"')
    db.commit()
    db.close()
    
def deleteCall(user):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('UPDATE users SET calls = "" WHERE username = "' + user + '"')
    db.commit()
    db.close()


def retCalls(user):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('''SELECT calls FROM users WHERE username==''' +"'" +user+"'" +';')
    hi=c.fetchall()
    return hi[0]

