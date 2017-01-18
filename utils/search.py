import sqlite3

#the db location
f="data/users.db"


'''
This fxn uses a querry to search all of our existing users
This allows the serch functionallity to work
'''
def searchUsers(query):
    db=sqlite3.connect(f)
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
This fxn updates the db friend table
'''

#to send or accept friend request
def sa_friend(q1, q2):
    db=sqlite3.connect(f)
    c=db.cursor()

    c.execute('INSERT INTO friend VALUES(' + "'" + q1+"'," + "'"+q2 + "');")
    db.commit()
    db.close()


'''
This fxn is used to determine the friendship status of two users
'''
# returns 0 if user 1 sent friend request to user 2
# returns 1 if user 2 sent friend request to user 1
# return 2 if both users have added each other !
# return 3 if both users have not added each other
def is_friends(q1, q2):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('SELECT * FROM friend WHERE user1 == ' + "'" + q1 + "' and user2== '" + q2 + "';")
    true1 = c.fetchall()
    c.execute('SELECT * FROM friend WHERE user2 == ' + "'" + q1 + "' and user1== '" + q2 + "';")
    true2 = c.fetchall()
    if len(true1) > 0 and len(true2) > 0:
        return 2
    if len(true1) > 0:
        return 0
    if len(true2) > 0:
        return 1
    if len(true1) == 0 and len(true2) == 0:
        return 3


'''
This fxn returns a list of friends for a given user
'''
def retFriends(user):
    db=sqlite3.connect(f)
    c=db.cursor()
    #c.execute("SELECT * FROM friend where user1 ==" + "'" + user +  "';")
    c.execute("SELECT * FROM friend;")
    tmp = c.fetchall()
    friendList = []
    friendRequestedList = []
    for a in tmp:
        #print a[0], a[1], is_friends(a[0],a[1])
        if a[1]==user and is_friends(a[0], a[1])==2:
            friendList.append(a[0])
        elif a[1]==user and is_friends(a[0],a[1])==0:
            friendRequestedList.append(a[0])
    return [friendList, friendRequestedList]
