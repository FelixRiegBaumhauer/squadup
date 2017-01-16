#THIS IS WHERE THE LOCATION FXNS AND SO ON WILL GO

import sqlite3
from time import gmtime, localtime, strftime

#the db location
f="data/users.db"


#return users who have a current location
def retUsers():
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('SELECT * FROM users WHERE time != "";')
    return c.fetchall()[::-1]

#print retUsers()

#return all users who have registered
def retAllUsers():
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('SELECT * FROM users;')
    return c.fetchall()[::-1]

#the function that updates the entry in the db that correspondes to the users location
#simplly said it is the backend fxn that updates loactions
def updateLoc(loc, user):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('UPDATE users SET location = "'+loc+'" WHERE username="'+user+'";')

    showtime = strftime("%Y-%m-%d %H:%M:%S", localtime())[6:-3]
    c.execute('UPDATE users SET time = "' + showtime +'" WHERE username="' + user+ '";')
    
    db.commit()
    db.close()
    return 0
