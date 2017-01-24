import sqlite3

#the location of the db
f = "data/users.db"

'''
This only exits for initializing, for some reason te database does not exist and we need to make it. 
This file should not be used by the site, as it means that we somehow lost all the users ino that was stored in the db
'''


db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#------------------------create tables---------------------------------------
q = "CREATE TABLE users (id INTEGER, username TEXT, password TEXT, location TEXT, time TIMESTAMP)"
c.execute(q)

q="CREATE TABLE schedule (userID TEXT, pd1 TEXT, pd2 TEXT, pd3 TEXT, pd4 TEXT, pd5 TEXT, pd6 TEXT, pd7 TEXT, pd8 TEXT, pd9 TEXT, pd10 TEXT)"
c.execute(q)

q="CREATE TABLE friend (user1 TEXT, user2 TEXT)"
c.execute(q)

q="CREATE TABLE messages (user1 TEXT, user2 TEXT, msg TEXT, time TEXT)"
c.execute(q)

db.commit()
db.close()
