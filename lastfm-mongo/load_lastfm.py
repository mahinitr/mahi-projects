from pymongo import MongoClient
import bson

lastfm = "lastfm"

tags = "tags"
artists = "artists"
users = "users"

tags_file = "inputs/tags.dat"
users_file = "inputs/user_artists.dat"
artists_file = "inputs/artists.dat"
tagged_file = "inputs/user_taggedartists.dat"
tagged_timestamp_file = "inputs/user_taggedartists-timestamps.dat"
friends_file = "inputs/user_friends.dat"

def log(msg):
    print "-> " + str(msg)

class MongoDB(object):
    def __init__(self,host,port,db_name):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]


    def get_coll(self,coll_name):
        return self.db[coll_name]


def load_tags_collection(db):
    tags_coll = db.get_coll(tags)
    with open(tags_file, "r") as fp:
        lines = fp.readlines()
    docs = []
    for i in range(1,len(lines)):
        line = lines[i].strip("\n")
        tag_id,tag_val = line.split("\t")
        tag_doc = {"tagID":tag_id, "tagValue":bson.Binary(str(tag_val))}
        docs.append(tag_doc)

    ret = tags_coll.insert_many(docs)
    log("Done loading tags collection..." + str(len(ret.inserted_ids)) + " records")

def load_artists_users_collection(db):
    artists_coll = db.get_coll(artists)
    users_coll = db.get_coll(users)

    artists_dict = {}
    users_dict = {}
    tagged_dict = {}

    with open(artists_file, "r") as fp:
        lines = fp.readlines()
    for i in range(1, len(lines)):
        line = lines[i].strip("\n")
        #id, name, url, pictureURL
        artistID, name, url, pictureURL = line.split("\t")
        doc = {"artistID":artistID, "name":name, "url":url, "pictureURL":pictureURL,"users":[],"tags":[], "no_of_users":0}
        artists_dict[artistID] = doc

    with open(users_file, "r") as fp:
        lines = fp.readlines()
    for i in range(1, len(lines)):
        line = lines[i].strip("\n")
        #userID  artistID    weight
        userID, artistID, weight = line.split("\t")
        artists_dict[artistID]["no_of_users"] += 1
        artists_dict[artistID]["users"].append({"userID":userID,"weight":weight})
        artistDOC = {"artistID":artistID,"weight":weight,"tags":[]}
        if userID in users_dict:
            users_dict[userID]["artists"].append(artistDOC)
        else:
            users_dict[userID] = {"userID":userID, "artists":[artistDOC],"friends":[]}

    with open(tagged_file, "r") as fp:
        lines = fp.readlines()
    for i in range(1, len(lines)):
        line = lines[i].strip("\n")
        #userID artistID    tagID   day month   year
        userID, artistID, tagID, day, month, year = line.split("\t")
        tagged_dict[userID + "-" + artistID + "-" + tagID] = (userID, artistID, tagID, day, month, year)

    not_found_atrists = []
    with open(tagged_timestamp_file, "r") as fp:
        lines = fp.readlines()
    for i in range(1, len(lines)):
        line = lines[i].strip("\n")
        #userID artistID    tagID   day month   year
        userID, artistID, tagID, timestamp = line.split("\t")
        userID, artistID, tagID, day, month, year = tagged_dict[userID + "-" + artistID + "-" + tagID]
        tagged_dict[userID + "-" + artistID + "-" + tagID] = (userID, artistID, tagID, day, month, year, timestamp)
        if artistID in artists_dict:
            artists_dict[artistID]["tags"].append({"userID":userID,"tagID":tagID,"day":day,"month":month,"year":year,"timestamp":timestamp})
        else:
            if artistID not in not_found_atrists:
                not_found_atrists.append(artistID)
        user_artists = users_dict[userID]["artists"]
        for doc in user_artists:
            if artistID == doc["artistID"]:
                doc["tags"].append({"tagID":tagID,"day":day,"month":month,"year":year,"timestamp":timestamp})

    with open(friends_file, "r") as fp:
        lines = fp.readlines()
    for i in range(1, len(lines)):
        line = lines[i].strip("\n")
        #userID, friendID
        userID, friendID = line.split("\t")
        users_dict[userID]["friends"].append(friendID)

    artists_docs = []
    for _ , artist_doc in artists_dict.items():
        artists_docs.append(artist_doc)

    users_docs = []
    for _ , user_doc in users_dict.items():
        users_docs.append(user_doc)

    ret = artists_coll.insert_many(artists_docs)
    log("Done loading artists data, loaded " + str(len(ret.inserted_ids)) + " records")
    
    ret = users_coll.insert_many(users_docs)
    log("Done loading users data, loaded " + str(len(ret.inserted_ids)) + " records")

    
if __name__ == "__main__":
    db = MongoDB('localhost',27017, lastfm)
    load_tags_collection(db)
    load_artists_users_collection(db)



