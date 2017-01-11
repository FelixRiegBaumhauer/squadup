import sqlite3

f = "data/users.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#------------------------create tables---------------------------------------
q = "CREATE TABLE users (id INTEGER, username TEXT, password TEXT, currLoc TEXT, time TIMESTAMP)"
c.execute(q)

q="CREATE TABLE schedule (userID TEXT, pd1 TEXT, pd2 TEXT, pd3 TEXT, pd4 TEXT, pd5 TEXT, pd6 TEXT, pd7 TEXT, pd8 TEXT, pd9 TEXT, TEXT)"
c.execute(q)

q="CREATE TABLE friend (user1 TEXT, user2 TEXT)"
c.execute(q)

db.commit()
db.close()
