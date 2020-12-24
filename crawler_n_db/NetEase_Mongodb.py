import pymongo

class Adapter_dictToDB:
    def get_userData(user_dict, user_id):
        # del user_dict['playlists']
        # del user_dict['media']
        user_dict['introduction'] = user_dict['introduction'][5:]
        user_dict['location'] = user_dict['location'][5:]
        user_dict['age'] = user_dict['age'][3:]
        user_dict['num_created_playlist'] = len(user_dict["playlists"]["my"])
        user_dict['num_added_playlist']   = len(user_dict["playlists"]["added"])
        user_dict = {"_id" : user_id} | user_dict
        return user_dict 
    
    def get_playlistData(user_dict):
        playlists = user_dict['playlists']['my'] + user_dict['playlists']['added']
        result_list = []

        for playlist in playlists:
            playlist["_id"] = int(playlist['href'][13:])
            playlist["link"] = "http://music.163.com/" + playlist["href"]
            playlist["count"] = playlist["detail"]["meta"]["count"]
            del playlist["href"]
            creator = playlist["detail"]["creator"]
            del playlist["detail"]
            playlist["creator"] = creator["link"][14:]
            result_list.append(playlist)
        
        return result_list

class Database_Facade:
    
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        # constructor
        return None

    def start(self, clear=False, name="NetEase-Music"):
        # start client instance 
        self.db_name = name
        self.client = pymongo.MongoClient(self.host, self.port)
        self.database = self.client[self.db_name]
        if(clear):
            (self.database["user"]).drop()
            (self.database["playlist"]).drop()
            (self.database["song"]).drop()
        clear_mode_ = 'on' if clear else "off"

        print(f"\t* MongoDB:")
        print(f"\t* Client connecting to http://{self.host}:{self.port}/")
        print(f"\t* Clear DB mode: {clear_mode_}")
        print()

        return self.database

    def close(self, clear=False):
        # close client instance
        if(clear):
            (self.database["user"]).drop()
            (self.database["playlist"]).drop()
            (self.database["song"]).drop()
        clear_mode_ = 'on' if clear else "off"
        self.client.close()

        print(f"\t* MongoDB:")
        print(f"\t* Stopped connection on http://{self.host}:{self.port}/")
        print(f"\t* Clear DB mode: {clear_mode_}")
        print()

        return 


    def insert(self, parsed_dict, user_id):
        # insert user
        user_db = self.database['user']
        user_dict = Adapter_dictToDB.get_userData(parsed_dict.copy(), user_id)
        if(user_db.count_documents({"_id":user_id}) == 0): user_db.insert_one(user_dict)
        else:user_db.update_one({"_id":user_id},{"$set":user_dict})

        # insert playlist
        playlist_db = self.database['playlist']
        playlist_list = Adapter_dictToDB.get_playlistData(parsed_dict)
        for playlist in playlist_list:
            if(playlist_db.count_documents({"_id":playlist['_id']}) == 0): playlist_db.insert_one(playlist)
            else: playlist_db.update_one({"_id":playlist['_id']}, {"$set":playlist})
        
        return

    # def list_collection_names(self, ptn=True):
    #     name_s = self.database.list_collection_names()
    #     if (ptn):
    #         for name in name_s: print(name)
    #     return list(name_s)


