import pymongo



class Logger():
    def __init__(self, config):
        self.mongoclient = pymongo.MongoClient(config.LOG_DB_CONNECTION)
        self.db = self.mongoclient.ESM_VirtualAgent

    def list_collections(self):
        return self.db.list_collection_names()

    def log_turn(self, activity):
        logDict = self.create_log_dict(activity)
        try:
            self.db.logs.insert_one(logDict)
        except Exception as e:
            print(e)

    def clear_logs(self):
        return self.db.logs.delete_many({})



    def log_skill_recommendations(self, user, timestamp, description):
        logDict = {
            'user': user,
            'timestamp': timestamp,
            'description': description
        }
        try:
            self.db.skillrecommendations.insert_one(logDict)
        except Exception as e:
            pass

    def create_log_dict(self, activity):
        logDict = {}
        logDict['channel_id'] = activity.channel_id
        logDict['conversation_id'] = activity.conversation.id
        logDict['timestamp'] = activity.timestamp,
        logDict['turn_messages'] = activity.additional_properties,
        logDict['intent_detected'] = activity.intent,
        entities = [[entity.type, entity.entity] for entity in activity.entities]
        logDict['entities'] = entities
        return logDict
















