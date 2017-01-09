import sqlite3

def createSchedule(schedule, userID):
    db=sqlite.connect("data/users.db")
    c=db.cursor()

    c.execute('INSERT INTO schedule VALUES("'+userID+'", "'+schedule[0]'", "'+schedule[1]'", "'+schedule[2]'", "'+schedule[3]'", "'+schedule[4]'", "'+schedule[5]'"'+schedule[6]'", "'+schedule[7]'", "'+schedule[8]'", "'+schedule[9]'";')

    db.commit()
    db.close()
