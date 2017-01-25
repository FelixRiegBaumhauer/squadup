#Seize The Day
#(Sachal, Kathy, Felix, Gio)


from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash, jsonify


import json, os, urllib, hashlib, utils.auth, utils.schedule, utils.search, utils.locate, utils.img2text, utils.messages


from werkzeug.utils import secure_filename

from time import gmtime, strftime





app = Flask(__name__)

app.secret_key = 'idk'#os.urandom(32)
secret=""


UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


'''
The root, has to decide if it wants to redirect you to the login or if you have the appropriate cookie it will let you in
'''
@app.route("/", methods=["GET","POST"])
def main():
    if(secret in session):
        if request.method=="GET":

            feed = utils.locate.retAllFriends(session[secret])
            feed2 = sorted(feed, key=lambda x: x[4], reverse=True) # sort users by time updated

            if utils.locate.retCurrentLocation(session[secret])[0][0].isdigit(): #check if current location is in skool (a room #)
                leave=False
                pd = utils.schedule.getPeriod(session[secret])
                utils.locate.updateLoc(str(pd), session[secret])
            else:
                leave=True
            #return redirect('display')
            mapDeets = utils.locate.maptesting(session[secret],0)
            info = []
            #friends = utils.search.retFriends(session[secret])[0]
            for f in feed:
                f = f[1]
                file_path = './static/images/' + str(f) + '.png'
                if os.path.exists(file_path):
                    info.append(file_path)
                else:
                    info.append('./static/images/default.png')
            return render_template('main.html',username=session[secret],news=feed2,leave=leave, lat=mapDeets[0], lon = mapDeets[1], coords=mapDeets[2], pfp=info)
        else:
            if request.form["submit"]=="post":
                utils.locate.updateLoc(request.form["location"], session[secret])
                return redirect(url_for('main'))
            if request.form["submit"]=="search":
                #users = utils.search.searchUsers(request.form['search'])
                q = request.form['search']
                return redirect("/profile/" + q)
            if request.form["submit"]=="Leave":
                pd = utils.schedule.getPeriod(session[secret])
                utils.locate.updateLoc(str(pd), session[secret])
                return redirect('/')
    return render_template("login.html")


'''
the login route, makes sure that your entered info can be checked so you can be let in
'''
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

@app.route("/display")
def display():
    return render_template('display.html')

@app.route("/show",methods=['GET', 'POST'])
def printit():
        feed = utils.locate.retAllFriends(session[secret])
        feed = sorted(feed, key=lambda x: x[4], reverse=True) # sort users by time updated
        return render_template('newsfeed.html',news=feed)

'''
The logout route, pops your session, and takes you out of the site
'''
@app.route("/logout")
@app.route("/logout/")
def log_user_out():
    print session
    if secret in session:
        session.pop(secret)
    #return redirect(url_for('main'))
    return render_template("login.html")##THIS IS A QUICK FIX
##THIS SHOULD BE FIXED IN THE FUTURE




'''
renders the signup page
'''
@app.route("/signup_page")
def present_signup():
    return render_template('signup.html')




'''
the route that either sends you to the login page after a successfull signup, or keeps you at the signup page if you failed
'''
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


'''
displays the profile site
uses all these complex function class to extract information that is either shown or is needed in the presentation of the profile site
'''
@app.route('/profile', methods=['POST','GET'])
def dispProfile():
    if(secret not in session):
        return render_template('login.html')

    L = [] #instantiate vars
    sched = (utils.schedule.retSchedule(session[secret]))
    classmates = (utils.schedule.retClassmates(session[secret]))
    loc = (utils.locate.retCurrentLocation(session[secret]))
    try:
        loc = loc[0][0]
    except:
        loc = ''
    if len(sched) != 0:     #listify schedule
        sched = sched[0]
        for a in sched:
            L.append(a)

    if request.method=="POST":
        if request.form["submit"]=="search":
            q = request.form['search']
            return redirect("/profile/" + q)
        if request.form["submit"]=="edit":
            status = -2
            return render_template("profile.html", username=session[secret], sch=L[1:], own=True, name=session[secret],location = loc,status=status, pfp='./static/images/'+session[secret]+'.png')
    status = -1
    return render_template("profile.html", username=session[secret], sch=zip(L[1:], classmates), own=True, name=session[secret],location = loc,status=status, pfp='./static/images/'+session[secret]+'.png')


'''
This is the route used by the search functions
If you search, the serached users profile is shown by means of this method
'''
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
    loc = (utils.locate.retCurrentLocation(query))
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
    return render_template("profile.html", username=session[secret], sch=L[1:], show=show, name=query, location = loc, status=friend_status, pfp='/static/images/' + query + '.png')


'''
This is the schedule route, which is used in harvesting the inputs to be used in a schedule
'''
@app.route('/schedule', methods=['POST'])
def inputSchedule():
    schdl=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    x=0
    while(x<10):
        schdl[x]=request.form["pd"+str(x+1)]
        x+=1
    utils.schedule.createSchedule(schdl,session[secret])
    return redirect(url_for('main'))


'''
this route is used to faciliate the friend button
'''
@app.route('/friends', methods=['GET', 'POST'])
def friends():
    searchFriends = utils.search.retFriends(session[secret])
    friends = searchFriends[0]
    friendsRequested = searchFriends[1]
    return render_template("friends.html", username=session[secret], friends=friends, friendsR=friendsRequested)

#@app.route("/idek/<imgname>")
def idek(imgname):
    #test_file = ocr_space_file(filename='example_image.png', language='pol')
    url = utils.img2text.ocr_space_file(filename='./static/images/' + imgname, language='eng')#['ParsedResults'][0]#['ParsedText']
    url = url[url.find('ParsedText')+13:url.find('"ErrorMessage')-1]
    url=url.replace(r"\r\n", r"")
    url=url.replace('...','<br>')
    #url = url[url.find('Room')+4:]
    pds = url[url.find('Period')+8:url.find("Room")-1]
    rooms=url[url.find("Room")+4:-1]
    return [pds, rooms]

'''
this route is used by the search functionallity
'''
@app.route("/search/<string:box>")
def process(box):
    query = request.args.get('query')
    suggestions = []
    tmpList = utils.locate.retAllUsers()
    for t in tmpList:
        suggestions.append({'value':t[1]})
    if box == 'names':
        # do some stuff to open your names text file
        # do some other stuff to filter
        return jsonify({"suggestions":suggestions})

'''messaging page'''
@app.route("/messages")
def messages():
    searchFriends = utils.search.retFriends(session[secret])
    friends = searchFriends[0]
    return render_template('messages.html', friends=friends)

'''messaging page'''
@app.route("/messages/<user>", methods=['GET', 'POST'])
def messagesfriends(user):
    if request.method=="POST":
        if request.form["submit"]=="send":
            msg = request.form["msg"]
            utils.messages.sendmsg(session[secret], user, msg)
            return redirect('/messages/' + user)
    else:
        feed = utils.messages.retMessages(session[secret], user)[-5:]
        return render_template('messages.html',msgs=feed, friend=user,t=True)


'''messaging page'''
@app.route("/showmsgs/<user>", methods=['GET', 'POST'])
def showmsgs(user):
    feed = utils.messages.retMessages(session[secret], user)[-5:]
    #feed = sorted(feed, key=lambda x: x[3], reverse=False) # sort users by time updated
    return render_template('msgfeed.html',msgs=feed, friend=user)


'''
This is used by the until now not in use file upload functionallity
'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


'''
This is used by the until now not in use file upload functionallity
'''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

'''
used by the upload functionallity
for schedules
'''
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method=='GET':
        return render_template('upload.html')
    else:
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            info = idek(filename)
            os.remove(UPLOAD_FOLDER + filename) # remove file after parsing imge
            pd = info[0].split()[1:]
            rooms = info[1].split()
            rooms = rooms[1:]
            x=1
            while(x<11):
                if str(x) not in pd:
                    rooms.insert(x,'free')
                x+=1
            utils.schedule.createSchedule(rooms[1:],session[secret])
            return redirect(url_for('main'))


'''for profile pictures'''

@app.route('/uploadPFP', methods=['GET', 'POST'])
def upload_PFP():
    if request.method=='GET':
        return render_template('upload.html')
    else:
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            try:
                os.rename(UPLOAD_FOLDER + filename, UPLOAD_FOLDER+session[secret]+'.png')
            except:
                os.remove(UPLOAD_FOLDER + session[secret]+'.png')
                os.rename(UPLOAD_FOLDER + filename, UPLOAD_FOLDER+session[secret]+'.png')
            return redirect(url_for('main'))

@app.route('/geo')
def geo():

    tmpcoords = utils.locate.maptesting(session[secret],1)[2]
    realcoords = []
    for t in tmpcoords:
        realcoords.append(str(t[1]) +',' + str(t[2]))
    return render_template("geoguesser.html", coord=realcoords)

'''
DEBUG and RUN
'''


if __name__ == '__main__':
    app.debug=True
    app.run(threaded=True)
