#THIS IS WHERE THE LOCATION FXNS AND SO ON WILL GO

import sqlite3, urllib, urllib2, json, utils.search, random
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
        c.execute('SELECT * FROM users WHERE username =="' + fr + '";')
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
    c.execute('SELECT location FROM users WHERE username="' + user+ '";')
    return c.fetchall()

#t : 0 is for friends only
#t : 1 is for all users

def maptesting(user, t):
    randcoordArray = [[40.76727216, -73.99392888], [40.71911552, -74.00666661], [40.71117416, -74.00016545], [40.68382604, -73.97632328], [40.74177603, -74.00149746], [40.69608941, -73.97803415], [40.68676793, -73.95928168], [40.73172428, -74.00674436], [40.72710258, -74.00297088], [40.761628, -73.972924], [40.69239502, -73.99337909], [40.69839895, -73.98068914], [40.71625008, -74.0091059], [40.71542197, -74.01121978], [40.7208736, -73.98085795], [40.722103786686034, -73.99724900722504], [40.71473993, -74.00910627], [40.752062307, -73.9816324043], [40.69089272, -73.99612349], [40.72917025, -73.99810231], [40.75323098, -73.97032517], [40.7489006, -73.97604882], [40.73971301, -73.99456405], [40.76068327096592, -73.9845272898674], [40.7381765, -73.97738662], [40.70905623, -74.01043382], [40.74334935, -74.00681753], [40.70037867, -73.99548059], [40.70277159, -73.99383605], [40.73781509, -73.99994661], [40.71146364, -74.00552427], [40.74195138, -74.00803013], [40.7546011026, -73.971878855], [40.72743423, -73.99379025], [40.69597683, -73.99014892], [40.7284186, -73.98713956], [40.73047309, -73.98672378], [40.7361967, -74.00859207], [40.69196566, -73.9813018], [40.68981035, -73.97493121], [40.697787, -73.973736], [40.688226, -73.979382], [40.69196035, -73.96536851], [40.69327018, -73.97703874], [40.73535398, -74.00483091], [40.72185379, -74.00771779], [40.71870987, -74.0090009], [40.72456089, -73.99565293], [40.72317958, -73.99480012], [40.73226398, -73.99852205]]
    llen = len(randcoordArray)
    if t == 0:
        friends = retAllFriends(user)#utils.search.retFriends(user)[0]
    else:
        friends = retAllUsers()
    coords = []
    lat=''
    lon=''
    for f in friends:
        if t==0:
            currLoc = str(retCurrentLocation(f[1])[0][0])
            if len(currLoc) > 4:
                latlon = geo_loc(currLoc.replace(',',' ').replace(' ','+'))
                lat = latlon['lat']
                lon = latlon['lng']
                coords.append([currLoc,lat,lon])
            else:
                place = utils.schedule.getPeriod(f[1])
                updateLoc(str(place), f[1])
                coords.append(['Stuyvesant', 40.7179464, -74.0139052])
        else:
            currLoc = f[3]
            if len(currLoc) > 4:
                latlon = geo_loc(currLoc.replace(',',' ').replace(' ','+'))
                lat = latlon['lat']
                lon = latlon['lng']
                coords.append([currLoc,lat,lon])
            else:
                i = int(random.random() * llen)
                coords.append(['randplace', randcoordArray[i][0], randcoordArray[i][1]])
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
