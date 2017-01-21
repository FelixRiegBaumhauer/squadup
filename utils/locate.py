#THIS IS WHERE THE LOCATION FXNS AND SO ON WILL GO

import sqlite3, urllib, urllib2, json, utils.search
from time import gmtime, localtime, strftime

#the db location
f="data/users.db"


#return users who have a current location
def retUsers():
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('SELECT * FROM users WHERE time != "";')
    return c.fetchall()[::-1]

#print retUsers()

#return all users who have registered
def retAllUsers():
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('SELECT * FROM users;')
    return c.fetchall()[::-1]

def retAllFriends(q):
    db=sqlite3.connect(f)
    c=db.cursor()
    fList = utils.search.retFriends(q)[0]
    retList = []
    for fr in fList:
        c.execute('SELECT * FROM users WHERE time != "" AND username =="' + fr + '";')
        try:
            retList.append(c.fetchall()[0])
        except:
            pass
    return retList

#the function that updates the entry in the db that correspondes to the users location
#simplly said it is the backend fxn that updates loactions
def updateLoc(loc, user):
    db=sqlite3.connect(f)
    c=db.cursor()
    c.execute('UPDATE users SET location = "'+loc+'" WHERE username="'+user+'";')

    showtime = strftime("%Y-%m-%d %H:%M:%S", localtime())[6:-3]
    c.execute('UPDATE users SET time = "' + showtime +'" WHERE username="' + user+ '";')

    db.commit()
    db.close()
    return 0


def retCurrentLocation(user):
    db=sqlite3.connect("data/users.db")
    c=db.cursor()
    c.execute('''SELECT location FROM users WHERE username==''' +"'" +str(user)+"'" +';')
    return c.fetchall()

def maptesting(user):
    friends = utils.search.retFriends(user)[0]
    coords = []
    lat=''
    lon=''
    for f in friends:
        currLoc = str(retCurrentLocation(f)[0][0])
        #print currLoc
        if len(currLoc) > 4:
            #print utils.locate.geo_loc('345+Chambers+Street+New+York+10282')
            latlon = geo_loc(currLoc.replace(',',' ').replace(' ','+'))
            lat = latlon['lat']
            lon = latlon['lng']
            coords.append([currLoc,lat,lon])
    return [lat,lon,coords]



key = 'AIzaSyC-MUmJ4HXQBGP_je0df7IpbQWY-cYGS3I'
def geo_loc(location):
#finds the longitude and latitude of a given location parameter using Google's Geocode API
#return format is a dictionary with longitude and latitude as keys
        loc = urllib.quote_plus(location)
        googleurl = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (loc,key)
        request = urllib2.urlopen(googleurl)
        results = request.read()
        gd = json.loads(results) #dictionary
        if gd['status'] != "OK":
                return location+" is a bogus location! What are you thinking?"
        else:
                result_dic = gd['results'][0] #dictionary which is the first element in the results list
                geometry = result_dic['geometry'] #geometry is another dictionary
                loc = geometry['location'] #yet another dictionary
                return loc
