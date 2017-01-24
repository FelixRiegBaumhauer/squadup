import sqlite3
from time import gmtime, localtime, strftime

#the db location
f="data/users.db"

def sendmsg(q1, q2, msg):
    db=sqlite3.connect(f)
    c=db.cursor()
    showtime = strftime("%Y-%m-%d %H:%M:%S", localtime())[6:-3]
    c.execute('INSERT INTO messages VALUES(' + "'" + q1+"'," + "'"+q2 +"'," + "'" + msg +"'," + "'"  + showtime + "'" + ");")
    #===============CLOSE
    db.commit()
    db.close()
    #======================

'''
This fxn returns a list of messages for a given user
'''
def retMessages(q1, q2):
    db=sqlite3.connect(f)
    c=db.cursor()
    #c.execute("SELECT * FROM friend where user1 ==" + "'" + user +  "';")
    c.execute("SELECT * FROM messages WHERE user1==" + "'" + q1 + "'AND user2==" + "'" + q2 +"';")
    fro = c.fetchall()
    c.execute("SELECT * FROM messages WHERE user1==" + "'" + q2 + "'AND user2==" + "'" + q1 +"';")
    to = c.fetchall()
    tmpL = fro + to
    retL = sorted(tmpL, key=lambda x: x[3], reverse=True)
    return retL
