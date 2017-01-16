import hashlib, sqlite3

#the db location
f="data/users.db"


'''
This fxn uses the given username and password to confirm if the info is in our db
If it is, and everything matches up, we permit the user to enter the site
'''
def login(g_username, g_password):
    #===========OPENING THE DB=============
    db = sqlite3.connect(f)
    c = db.cursor()
    #=================================================
    
    c.execute("SELECT password FROM users WHERE username="+"'"+g_username+"'"+";")
    pass_hold = c.fetchall()

    #the for loops only fire if there is something in pass_hold,
    #thus, if there is no account for that user, then pass_hold is empty
    #and as a result the for never fires and False is retuned
    #False is also returned if the password doesn't match the one in the db

    #=================CLOSE DB
    db.commit()
    db.close()
    #==============================
    
    for line in pass_hold:
        for entry in line:
            if(g_password == entry):
                #you can be logged in
                return True
    #NO LOGIN FOR YOU
    return False

'''
Makes entries in the db if all the given info makes sense:
i.e, if the 2 passwords match and the username is not allready taken
'''
def make_account(g_username, g_password1, g_password2):
    
    if(g_password1 != g_password2):
        return False
    if(g_username == "" or g_password1 == ""):
        return False

    
    #===========OPENING THE DB=============
    #f="data/users.db"
    db = sqlite3.connect(f);
    c = db.cursor()
    #=================================================
    c.execute("SELECT username FROM users WHERE username="+"'"+g_username+"'"+";")
    hold = c.fetchall()

    #=============CLOSE DB
    db.commit()
    db.close()
    #=========================
    
    #the for loop only fires if there is something in hold, meaning double users
    for x in hold:
        return False

    #==============OPEN DB
    db = sqlite3.connect(f);
    c = db.cursor()
    #===============
    c.execute('SELECT id from users;');
    hold=c.fetchall()

    if(len(hold)==0):
        c.execute('INSERT INTO users VALUES(0,"'+g_username+'"'+','+'"'+g_password1+'"'+', "", "");')
    else:
        c.execute('INSERT INTO users VALUES('+str(hold[len(hold)-1][0]+1)+',"'+g_username+'"'+','+'"'+g_password1+'"'+', "", "");')

    #===============CLOSE
    db.commit()
    db.close()
    #======================

    return True

