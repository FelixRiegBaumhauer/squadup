import sqlite3

from datetime import datetime

#the db location
f="data/users.db"


'''
this fxn updates the db enteries corresponding to their schedule
a list of locations (schedule) is passed in
and the fxn removes the old db entry, and makes a new one that is now relevant
'''
def createSchedule(schedule, userID):
    db=sqlite3.connect(f)
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
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('''SELECT * FROM schedule WHERE userID==''' +"'" +str(user)+"'" +';')
    hi=c.fetchall()
    return hi


'''
This function finds users that have the same classes as another user
'''
def retClassmates(user):
    db=sqlite3.connect(f)
    c=db.cursor()
    pd=1
    classes=[]
    while(pd<11):
        c.execute('SELECT pd'+str(pd)+' FROM schedule WHERE userID="'+user+'";')
        yourClass=c.fetchall()
        if(len(yourClass)!=0):
            yourClass=yourClass[0][0]
        else:
            yourClass='free'
        c.execute('SELECT userID, pd'+str(pd)+' FROM schedule;')
        usersClasses=c.fetchall()
        #print usersClasses, '\n\n'
        #print usersClasses
        classmates=[]
        for people in usersClasses:
            if(yourClass==people[1] and people[0]!=user):
                classmates.append(people[0])
        pd+=1
        classes.append(classmates)
    return classes

'''
This fxn returns the current period
'''
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
        [889,935]
    ]
    time = datetime.now()
    hour = time.strftime('%H')
    minute = time.strftime('%M')
    Tminute = 60 * int(hour) + int(minute)
    i = 0
    sched = retSchedule(user)
    while i < len(Rperiod):
        if Tminute >=Rperiod[i][0] and Tminute <= Rperiod[i][1]:
            if len(sched) > 0:
                return sched[0][i+1]
            else:
                return "outside of school"
        i+=1
    return "outside of school"
