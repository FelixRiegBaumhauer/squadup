import sqlite3

def createSchedule(schedule, userID):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()

    c.execute('INSERT INTO schedule VALUES("'+userID+'", "'+str(schedule[0])+'", "'+str(schedule[1])+'", "'+str(schedule[2])+'", "'+str(schedule[3])+'", "'+str(schedule[4])+'", "'+str(schedule[5])+'", "'+str(schedule[6])+'", "'+str(schedule[7])+'", "'+str(schedule[8])+'", "'+str(schedule[9])+'");')

    db.commit()
    db.close()

def retSchedule(user):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('''SELECT * FROM schedule WHERE userID==''' +"'" +str(user)+"'" +';')
    return c.fetchall()
#print retSchedule('qwerty')[-1]
