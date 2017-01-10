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


