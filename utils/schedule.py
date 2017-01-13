import sqlite3

def createSchedule(schedule, userID):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('SELECT userID from schedule')

    hold=c.fetchall()
    for users in hold:
        if(users[0]==userID):
            c.execute('DELETE FROM schedule WHERE userID=="'+userID+'";')

    c.execute('INSERT INTO schedule VALUES("'+userID+'", "'+schedule[0]+'", "'+schedule[1]+'", "'+schedule[2]+'", "'+schedule[3]+'", "'+schedule[4]+'", "'+schedule[5]+'", "'+schedule[6]+'", "'+schedule[7]+'", "'+schedule[8]+'", "'+schedule[9]+'");')

    db.commit()
    db.close()

def retSchedule(user):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('''SELECT * FROM schedule WHERE userID==''' +"'" +str(user)+"'" +';')
    return c.fetchall()

def retCurrentLocation(user):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('''SELECT location FROM users WHERE username==''' +"'" +str(user)+"'" +';')
    return c.fetchall()

def retClassmates(user):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    pd=1
    classes=[]
    while(pd<11):
        c.execute('SELECT pd'+str(pd)+' FROM schedule WHERE userID="'+user+'";')
        yourClass=c.fetchall()[0][0]
        print yourClass
        c.execute('SELECT userID, pd'+str(pd)+' FROM schedule;')
        usersClasses=c.fetchall()
        classmates=[]
        for people in usersClasses:
            if(yourClass==people[1] and people[0]!=user):
                classmates.append(people[0])
        pd+=1
        classes.append(classmates)
    return classes
