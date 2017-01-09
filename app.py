#Seize The Day
#(Sachal, Kathy, Felix, Gio)


from flask import Flask, render_template, request, session, redirect, url_for
import json, os, urllib, hashlib, utils.auth

app = Flask(__name__)

app.secret_key = 'seizetheday' #maybe this os.urandom(32)
secret=""

@app.route("/")
def main():
    if(secret in session):
        return render_template('main.html')
    return render_template("login.html")




@app.route("/login", methods=["POST"])
def verify_login():
    given_user = request.form["username"]
    given_pass = request.form["password"]

    hashPassObj = hashlib.sha1()
    hashPassObj.update(given_pass)
    hashed_pass = hashPassObj.hexdigest()

    permission = utils.auth.login(given_user, hashed_pass)
    
    if(permission == True):
        session[secret]=given_user
        return redirect(url_for('main'))
    
    return render_template('login.html')




@app.route("/logout")
def log_user_out():
    print session
    session.pop(secret)
    #return redirect(url_for('main'))
    return render_template("login.html")##THIS IS A QUICK FIX
##THIS SHOULD BE FIXED IN THE FUTURE





@app.route("/signup_page")
def present_signup():
    return render_template('signup.html')





@app.route("/signup", methods=["POST"])
def verify_signup():
    given_user = request.form["username"]
    given_pass1 = request.form["password1"]
    given_pass2 = request.form["password2"]
    
    hashPassObj = hashlib.sha1()
    hashPassObj.update(given_pass1)
    hashed_pass1 = hashPassObj.hexdigest()

    hashPassObj = hashlib.sha1()
    hashPassObj.update(given_pass2)
    hashed_pass2 = hashPassObj.hexdigest()
    
    permission = utils.auth.make_account(given_user, hashed_pass1, hashed_pass2)
    
    if(permission == True):
        return redirect(url_for('main'))
    
    return redirect(url_for('present_signup'))

@app.route('/profile')
def dispProfile():
    return render_template("profile.html", username=session[secret])

@app.route('/schedule', methods=['POST'])
def inputeSchedule():
    schdl=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    x=0
    while(x<10):
        schdl[x]=request.form[str(x+1)]
        x+=1
    createSchedule()
    return redirect(url_for('main'))

'''
@app.route('/main')
def main():
    return render_template("main.html")
'''    



if __name__ == '__main__':
    debug=True
    app.run()
    #app.run()
    #app.run('127.0.0.1', port=5000)
