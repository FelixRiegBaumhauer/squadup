import sqlite3

def createSchedule(schedule, userID):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('SELECT userID from schedule')

    hold=c.fetchall()
    for users in hold):
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
#print retSchedule('qwerty')[-1]
