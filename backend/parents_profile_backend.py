from .dataObjects import Parent
from .connect_with_mongo import Mongo


class ParentsProfileBackend:

    __instance = None

    @staticmethod
    def getInstance():
        if ParentsProfileBackend.__instance is None:
            ParentsProfileBackend()

        return ParentsProfileBackend.__instance

    def __init__(self):
        if ParentsProfileBackend.__instance is not None:
            raise Exception("This class is a singleton!")

        else:
            ParentsProfileBackend.__instance = self

    def updateInfo(self, parentObj: Parent, info):
        mongo = Mongo.getInstance()
        query = {'_id': parentObj.id}
        parentsData = mongo.parentsData.find_one(query)[0]
        parentObj.updateInfo(info)
        temp = parentObj.toDict()
        del temp['_id']

        parentsData.update_one(query, {'$set': temp})
