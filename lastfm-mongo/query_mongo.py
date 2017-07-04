from pymongo import MongoClient
from bson.son import SON
import sys
import operator
import time

#   Query Names & Its arguments
#
#   ARTISTS_OF_FRIENDS_OF_USER - userID
#   RECENT_10_TAGS_OF_ARTIST - artist_name
#   TOP_10_USERS_BY_WEIGHT - artist_name
#   RECENT_10_ARTISTS_TAGGED - userID
#
#   TOP_5_ARTISTS_BY_NUM_USERS - None
#   TOP_20_TAGS_BY_NUM_ASSIGNS - artists_name
#   TOP_5_ARTISTS_OF_HIS_FRIENDS - userID
#   TOP_5_SIMILAR_ARTISTS - artistName
#

help_text = """
******************* Help for Running the script **************************
The Syntax of runnig of the queries...
    python query_mongo.py ARTISTS_OF_FRIENDS_OF_USER "<userID>"
        Ex: python query_mongo.py ARTISTS_OF_FRIENDS_OF_USER "52"

    python query_mongo.py RECENT_10_TAGS_OF_ARTIST "<artist_name>"
        Ex: python query_mongo.py RECENT_10_TAGS_OF_ARTIST "Diary of Dreams"

    python query_mongo.py TOP_10_USERS_BY_WEIGHT "<artist_name>"
        Ex: python query_mongo.py TOP_10_USERS_BY_WEIGHT "Diary of Dreams"

    python query_mongo.py RECENT_10_ARTISTS_TAGGED "userID"
        Ex: python query_mongo.py RECENT_10_ARTISTS_TAGGED "52"

    python query_mongo.py TOP_5_ARTISTS_BY_NUM_USERS

    python query_mongo.py TOP_20_TAGS_BY_NUM_ASSIGNS "<artists_name>"
        Ex: python query_mongo.py TOP_20_TAGS_BY_NUM_ASSIGNS "Diary of Dreams"

    python query_mongo.py TOP_5_ARTISTS_OF_HIS_FRIENDS "userID"
        Ex: python query_mongo.py TOP_5_ARTISTS_OF_HIS_FRIENDS "52"

    python query_mongo.py TOP_5_SIMILAR_ARTISTS "<artists_name>"
        Ex:python query_mongo.py TOP_5_SIMILAR_ARTISTS "London After Midnight"

**************************************************************************

"""
def exec_time(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print "\n\n{} took {} milliseconds".format(method.__name__, (te-ts))
        return result
    return timed
    
def log(msg):
    msg = str(msg)
    print msg

@exec_time
def top_5_artists_by_no_of_users(db):
    coll = db["artists"]
    pipeline = [
            {"$sort" : SON([("no_of_users",-1)])},
            {"$limit" : 5}
        ]
    res = coll.aggregate(pipeline)
    for doc in res:
        artist_name = unicode(doc["name"]).encode("utf8")
        artist_id = doc["artistID"]
        no_of_user = doc["no_of_users"]
        log("no_of_users : " + str(no_of_user) + ", artistsID : " + str(artist_id) + ", artist_name : " + artist_name )

@exec_time
def top_20_tags_by_num_assigns(db,artist_name):
    coll = db["artists"]
    res = coll.find_one({"name":artist_name})
    if res is None:
        return None
    tags = res["tags"]
    tags_count = {}
    for tag in tags:
        tagID = tag["tagID"]
        if tagID in tags_count:
            tags_count[tagID] += 1
        else:
            tags_count[tagID] = 1
    sorted_tags = sorted(tags_count.items(), key=operator.itemgetter(1))
    for tag in sorted_tags[:-21:-1]:
        tagID,count = tag
        coll = db["tags"]
        res = coll.find_one({"tagID":tagID})
        if res is None:
            log("TagID : " + tagID )
        else:
            log("TagID : " + tagID + ",  tagValue : " + res["tagValue"])

@exec_time
def top_5_artists_of_his_friends(db,userID):
    coll = db["users"]
    res = coll.find_one({"userID":userID})
    if res is None:
        return
    friends = res["friends"]
    user_artists = res["artists"]
    friends_artists = {}
    for f_ID in friends:
        res1 = coll.find_one({"userID":f_ID})
        for artist in res1["artists"]:
            a_id = artist["artistID"]
            a_weight = artist["weight"]
            if a_id in friends_artists:
                friends_artists[a_id] += int(a_weight)
            else:
                friends_artists[a_id] = int(a_weight)
    friends_artists = dict(friends_artists)
    for a in user_artists:
        if a["artistID"] in friends_artists:
            del friends_artists[a["artistID"]]
    sorted_artists = sorted(friends_artists.items(), key=operator.itemgetter(1))
    coll = db["artists"]
    for artist in sorted_artists[:-6:-1]:
        id_, weight = artist
        res = coll.find_one({"artistID":id_})
        if res is not None:
            print "artistID : " + id_ + ", name : ",  res["name"]
    
@exec_time
def top_5_similar_artists(db,artist_name):
    coll = db["artists"]
    res = coll.find_one({"name":artist_name})
    if res is None:
        return
    given_artist_id = res["artistID"]
    unique_users = []
    for user in res["users"]:
        userID = user["userID"]
        if userID not in unique_users:
            unique_users.append(userID)
    artists_of_users = []
    artists_to_users = {}
    for user in unique_users:
        ret = coll.find({"users.userID":userID})
        for doc in ret:
            if doc["artistID"] not in artists_of_users:
                artists_of_users.append(doc["artistID"])
                artists_to_users[doc["artistID"]] = doc["users"]
    artist_common_users_no = {}
    unique_users = set(unique_users)
    for artist_id in artists_of_users:
        users = set()
        for user in artists_to_users[artist_id]:
            users.add(user["userID"])
        artist_common_users_no[artist_id] = len(users.intersection(unique_users))
    if given_artist_id in artist_common_users_no:
        del artist_common_users_no[given_artist_id]
    sorted_artists_common_nos = sorted(artist_common_users_no.items(), key=operator.itemgetter(1))
    for artistID , _ in sorted_artists_common_nos[:-6:-1]:
        res = coll.find_one({"artistID":artistID})
        name = unicode(res["name"]).encode("utf-8")
        print "artistID : " + artistID + ", name : ", name

@exec_time
def artists_of_friends_of_user(db, userID):
    coll = db["users"]
    ret = coll.find_one({"userID":userID})
    if ret is None:
        return
    friends = ret["friends"]
    friends_artists = []
    for fr_ID in friends:
        res = coll.find_one({"userID":userID})
        for artist in res["artists"]:
            if artist["artistID"] not in friends_artists:
                friends_artists.append(int(artist["artistID"]))
    coll = db["artists"]
    for artist in friends_artists:
        res = coll.find_one({"artistID" :str(artist) })
        if res is not None:
            print "artistID : " + str(artist) + ", name : ", unicode(res["name"]).encode("utf8")
        else:
            log("artistID : " + str(artist) )

@exec_time
def recent_10_tags_of_artist(db, artist_name):
    coll = db["artists"]
    ret = coll.find_one({"name":artist_name})
    if ret is None:
        return
    tags_time = {}
    for tag in ret["tags"]:
        tagID = tag["tagID"]
        ts = tag["timestamp"]
        tags_time[tagID] = int(ts)
    sorted_tags = sorted(tags_time.items(), key=operator.itemgetter(1))
    coll = db["tags"]
    for tag,_ in sorted_tags[:-11:-1]:
        res = coll.find_one({"tagID":tag})
        log("tagID : " + tagID + ", tag_value : " + res["tagValue"])

@exec_time
def top_10_users_weight(db,artist_name):
    coll = db["artists"]
    ret = coll.find_one({"name":artist_name})
    if ret is None:
        return
    users_weight = {}
    for user in ret["users"]:
        users_weight[user["userID"]] = int(user["weight"])
    sorted_weights = sorted(users_weight.items(), key=operator.itemgetter(1))
    for userID, w in sorted_weights[:-11:-1]:
        log("userId: " + userID + ",  weight: " + str(w))

@exec_time
def recent_10_artists_tagged(db,userID):
    coll = db["users"]
    ret = coll.find_one({"userID":userID})
    if ret is None:
        return
    artists = ret["artists"]
    artists_ts = {}
    for artist in artists:
        tags_ts = []
        for tag in artist["tags"]:
            tags_ts.append(int(tag["timestamp"]))
        tags_ts = sorted(tags_ts)
        if len(tags_ts) > 0:
            artists_ts[artist["artistID"]] = tags_ts[-1]
    sorted_ts = sorted(artists_ts.items(), key = operator.itemgetter(1))
    coll = db["artists"]
    for artist, _ in sorted_ts:
        res = coll.find_one({"artistID":artist})
        if res is not None:
            print "artistID : " + artist + ", name : " , unicode(res["name"]).encode("utf-8")


ARTISTS_OF_FRIENDS_OF_USER = "ARTISTS_OF_FRIENDS_OF_USER"
RECENT_10_TAGS_OF_ARTIST = "RECENT_10_TAGS_OF_ARTIST"
TOP_10_USERS_BY_WEIGHT = "TOP_10_USERS_BY_WEIGHT"
RECENT_10_ARTISTS_TAGGED = "RECENT_10_ARTISTS_TAGGED"

TOP_5_ARTISTS_BY_NUM_USERS = "TOP_5_ARTISTS_BY_NUM_USERS"
TOP_20_TAGS_BY_NUM_ASSIGNS = "TOP_20_TAGS_BY_NUM_ASSIGNS"
TOP_5_ARTISTS_OF_HIS_FRIENDS = "TOP_5_ARTISTS_OF_HIS_FRIENDS"
TOP_5_SIMILAR_ARTISTS = "TOP_5_SIMILAR_ARTISTS"

FUNC_NAMES = {}

FUNC_NAMES[ARTISTS_OF_FRIENDS_OF_USER] = artists_of_friends_of_user
FUNC_NAMES[RECENT_10_TAGS_OF_ARTIST] = recent_10_tags_of_artist
FUNC_NAMES[TOP_10_USERS_BY_WEIGHT] = top_10_users_weight
FUNC_NAMES[RECENT_10_ARTISTS_TAGGED] = recent_10_artists_tagged

FUNC_NAMES[TOP_5_ARTISTS_BY_NUM_USERS] = top_5_artists_by_no_of_users
FUNC_NAMES[TOP_20_TAGS_BY_NUM_ASSIGNS] = top_20_tags_by_num_assigns
FUNC_NAMES[TOP_5_ARTISTS_OF_HIS_FRIENDS] = top_5_artists_of_his_friends
FUNC_NAMES[TOP_5_SIMILAR_ARTISTS] = top_5_similar_artists

if __name__ == "__main__":
    log(help_text)
    args = sys.argv
    log("INFO - Query Passed:    " + " ".join(args))
    if len(args) <= 1:
        log("Less no of arguments provided")
        sys.exit(0)
    client = MongoClient()
    db = client["lastfm"]
    query_name = args[1].upper()
    log("*** RESULTS ***\n")
    if query_name == TOP_5_ARTISTS_BY_NUM_USERS:
        FUNC_NAMES[query_name](db)
    elif query_name == TOP_20_TAGS_BY_NUM_ASSIGNS:
        try:
            arg_2 = args[2]
        except:
            log("ERROR: Invalid no of arguments for " + query_name)
            sys.exit(0)
        FUNC_NAMES[query_name](db,arg_2)
    elif query_name == TOP_5_ARTISTS_OF_HIS_FRIENDS:
        try:
            arg_2 = args[2]
        except:
            log("ERROR: Invalid no of arguments for " + query_name)
            sys.exit(0)
        FUNC_NAMES[query_name](db,arg_2)
    elif query_name == TOP_5_SIMILAR_ARTISTS:
        try:
            arg_2 = args[2]
        except:
            log("ERROR: Invalid no of arguments for " + query_name)
            sys.exit(0)
        FUNC_NAMES[query_name](db,arg_2)
    elif query_name == ARTISTS_OF_FRIENDS_OF_USER:
        try:
            arg_2 = args[2]
        except:
            log("ERROR: Invalid no of arguments for " + query_name)
            sys.exit(0)
        FUNC_NAMES[query_name](db,arg_2)       
    elif query_name == RECENT_10_TAGS_OF_ARTIST:
        try:
            arg_2 = args[2]
        except:
            log("ERROR: Invalid no of arguments for " + query_name)
            sys.exit(0)
        FUNC_NAMES[query_name](db,arg_2)
    elif query_name == TOP_10_USERS_BY_WEIGHT:
        try:
            arg_2 = args[2]
        except:
            log("ERROR: Invalid no of arguments for " + query_name)
            sys.exit(0)
        FUNC_NAMES[query_name](db,arg_2)
    elif query_name == RECENT_10_ARTISTS_TAGGED:
        try:
            arg_2 = args[2]
        except:
            log("ERROR: Invalid no of arguments for " + query_name)
            sys.exit(0)
        FUNC_NAMES[query_name](db,arg_2)
    else:
        log("ERROR: Invalid Query Name")
    log("\n")







