import sqlite3

from datetime import datetime


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

def getPeriod(user):
    Rperiod = [
        [460,521],
        [520,566],
        [565,615],
        [614,661],
        [660,707],
        [706,753],
        [752,799],
        [798,845],
        [844,890],
        [889,935],
        [934,1440],
        [934,1440],
        [0,480]
    ]
    time = datetime.now()
    hour = time.strftime('%H')
    minute = time.strftime('%M')
    Tminute = 60 * int(hour) + int(minute)
    i = 0
    while i < len(Rperiod):
        if Tminute >=Rperiod[i][0] and Tminute <= Rperiod[i][1]:
            sched = retSchedule(user)
            if len(sched) > 0:
                return sched[0][i+1]
            else:
                return -1
            #return i+1
        i+=1
    return -1
