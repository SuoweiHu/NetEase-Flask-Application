import pymongo


class Adapter_dictToDB:
    def get_userData(user_dict, user_id):
        del user_dict['playlists']
        del user_dict['media']
        user_dict['introduction'] = user_dict['introduction'][5:]
        user_dict['location'] = user_dict['location'][5:]
        user_dict['age'] = user_dict['age'][3:]
        user_dict = {"_id" : user_id} | user_dict
        return user_dict 
    
    def get_playlistData(user_dict):
        my_playlist = user_dict['playlists']['my']
        added_playlist = user_dict['playlists']['added']
        result_list = []
        for playlist in my_playlist:
            playlist["_id"] = int(playlist['href'][13:])
            playlist["link"] = "http://music.163.com/" + playlist["href"]
            playlist["count"] = playlist["detail"]["meta"]["count"]
            del playlist["href"]
            creator = playlist["detail"]["creator"]
            del playlist["detail"]
            playlist["creator"] = creator["link"][14:]
            result_list.append(playlist)
        return result_list

class Database_Utils:
    host = 'localhost'
    port = 27017
    client = None
    db_name = None
    database = None
    collection = None
    
    def __init__(self, database_name="NetEase-Music"):
        self.db_name = database_name
        return

    def start(self):
        self.client = pymongo.MongoClient(self.host, self.port)
        self.database = self.client[self.db_name]
        return self.database

    def collection(self,collection_name):
        return self.database[collection_name]
    
    def switch_collection(self, collection_name):
        self.collection = self.database[collection_name]
        return self
    
    def close(self):
        self.client.close()
        return 

    def list_collection_names(self, ptn=True):
        name_s = self.database.list_collection_names()
        if (ptn):
            for name in name_s: print(name)
        return list(name_s)

    def dump_user(self, parsed_dict, user_id):
        user_db = self.database['user']
        user_dict = Adapter_dictToDB.get_userData(parsed_dict.copy(), user_id)
        if(user_db.count_documents({"_id":user_id}) == 0): user_db.insert_one(user_dict)
        else:user_db.update_one({"_id":user_id},{"$set":user_dict})

        playlist_db = self.database['playlist']
        playlist_list = Adapter_dictToDB.get_playlistData(parsed_dict)
        for playlist in playlist_list:
            if(playlist_db.count_documents({"_id":playlist['_id']}) == 0): playlist_db.insert_one(playlist)
            else: playlist_db.update_one({"_id":playlist['_id']}, {"$set":playlist})
        
        return

def database_factory(clear=True):
    database = Database_Utils()
    database.start()
    if(clear):
        (database.collection("user")).drop()
        (database.collection("playlist")).drop()
        (database.collection("song")).drop()
    return database

__database_util__ = database_factory(clear=False) # 初始化数据库

def insert(result, id):
    __database_util__.dump_user(result, id)
    return 

def start(clear=False):
    __database_util__ = database_factory(clear=clear) # 初始化数据库
    return __database_util__

def close():
    __database_util__.close()


