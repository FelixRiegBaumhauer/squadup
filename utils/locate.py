#THIS IS WHERE THE LOACTION FXNS AND SO ON WILL GO
#making this show all locations for now

import sqlite3
from time import gmtime, strftime

def retUsers():
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('SELECT * FROM users;')
    return c.fetchall()[::-1]

def updateLoc(loc, user):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('UPDATE users SET location = "'+loc+'" WHERE username="'+user+'";')

    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())[6:]
    c.execute('UPDATE users SET time = "' + showtime +'" WHERE username="' + user+ '";')
    
    db.commit()
    db.close()
    return 0
