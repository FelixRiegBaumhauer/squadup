#Seize The Day
#(Sachal, Kathy, Felix, Gio)


from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash, jsonify
import json, os, urllib, hashlib, utils.auth, utils.schedule, utils.search, utils.locate
from werkzeug.utils import secure_filename
from time import gmtime, strftime

app = Flask(__name__)

app.secret_key = 'seizetheday' #maybe this os.urandom(32)
secret=""


UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET","POST"])
def main():
    if(secret in session):
        if request.method=="GET":
            feed = utils.locate.retUsers()
            feed = sorted(feed, key=lambda x: x[4], reverse=True)
            return render_template('main.html',username=session[secret],news=feed)
        else:
            if request.form["submit"]=="post":
                utils.locate.updateLoc(request.form["location"], session[secret])
                return redirect(url_for('main'))
            if request.form["submit"]=="search":
                #users = utils.search.searchUsers(request.form['search'])
                q = request.form['search']
                return redirect("/profile/" + q)
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


@app.route('/profile', methods=['POST','GET'])
def dispProfile():
    if(secret not in session):
        return render_template('login.html')

    L = [] #instantiate vars
    sched = (utils.schedule.retSchedule(session[secret]))
    loc = (utils.schedule.retCurrentLocation(session[secret]))
    try:
        loc = loc[0][0]
    except:
        loc = ''
    if request.method=="POST":
        if request.form["submit"]=="search":
            q = request.form['search']
            return redirect("/profile/" + q)
        if request.form["submit"]=="edit":
            show = False
            status = -2
            return render_template("profile.html", username=session[secret], sch=L, show=show, own=True, name=session[secret],location = loc,status=status)
    status = -1
    if len(sched) != 0:     #if GET request
        show=True
        sched = sched[-1]
        for a in sched:
            L.append(a)
    else:
        show=False
    return render_template("profile.html", username=session[secret], sch=L, show=show, own=True, name=session[secret],location = loc,status=status)


@app.route('/profile/<query>', methods=['POST','GET'])
def dispFriendProfile(query):
    if len(utils.search.searchUsers(query))<1:
                return 'User not found'
    if query == session[secret]:
        return redirect("/profile")
    if request.method=="POST":
        if request.form["submit"]=="add_friend":
            utils.search.sa_friend(session[secret], query)
            return redirect('/profile/' + query)
        if request.form["submit"]=="search":
            q = request.form['search']
            return redirect("/profile/" + q)
    loc = (utils.schedule.retCurrentLocation(query))
    try:
        loc = loc[0][0]
    except:
        loc = ''
    sched = (utils.schedule.retSchedule(query))
    L = []
    if len(sched) != 0:
        show=True
        sched = sched[-1]
        for a in sched:
            L.append(a)
    else:
        show=True
    friend_status = utils.search.is_friends(session[secret], query)
    return render_template("profile.html", username=session[secret], sch=L, show=show, name=query, location = loc, status=friend_status)

@app.route('/schedule', methods=['POST'])
def inputSchedule():
    schdl=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    x=0
    while(x<10):
        schdl[x]=request.form["pd"+str(x+1)]
        x+=1
    utils.schedule.createSchedule(schdl,session[secret])
    return redirect(url_for('main'))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method=='GET':
        return render_template('upload.html')
    else:
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
'''
@app.route('/updateloc', methods=['POST'])
def updateLocation():
    utils.locate.updateLoc(request.form["location"],session[secret])
    return render_template('profiles.html')
'''

'''
@app.route('/main')
def main():
    return render_template("main.html")
'''



if __name__ == '__main__':
    app.debug=True
    app.run()
    #app.run()
    #app.run('127.0.0.1', port=5000)
