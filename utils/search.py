import sqlite3

def searchUsers(query):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()

    c.execute("SELECT username FROM users;")
    hold=c.fetchall()

    db.close()

    L=[]
    
    for users in hold:
        if(query in users[0]):
            L.append(users[0])
    return L

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Friending user functions
'''

#to send or accept friend request
def sa_friend(q1, q2):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()

    c.execute('INSERT INTO friends VALUES('+q1+',' + q2 + ');')

def is_friends(q1, q2):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('SELECT * FROM friend WHERE user1 == ' + q1 + ' and user2== ' + q2 + ';')
    true1 = c.fetchall()
    c.execute('SELECT * FROM friend WHERE user2 == ' + q1 + ' and user1== ' + q2 + ';')
    true2 = c.fetchall()
    return len(true1) > 0 and len(true2) > 0
    
    
