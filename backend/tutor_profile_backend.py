from .dataObjects import Tutor
from .connect_with_mongo import Mongo
from typing import Dict


class TutorProfileBackend:

    __instance = None

    @staticmethod
    def getInstance():
        if TutorProfileBackend.__instance is None:
            TutorProfileBackend()

        return TutorProfileBackend.__instance

    def __init__(self):
        if TutorProfileBackend.__instance is not None:
            raise Exception("This class is a singleton!")

        else:
            TutorProfileBackend.__instance = self

    def updateInfo(self, tutorObj: Tutor, info: Dict):
        mongo = Mongo.getInstance()
        query = {'_id': tutorObj.id}
        tutorsData = mongo.tutorsData.find_one(query)[0]
        tutorObj.updateInfo(info)
        temp = tutorObj.toDict()
        del temp['_id']

        tutorsData.update_one(query, {'$set': temp})

    def getImageKey(self, imagePath):
        with open(imagePath, 'rb') as f:
            output = f.read()

        mongo = Mongo.getInstance().imagesData
        return mongo.put(output)

    def getImageBytes(self, imageKey):

        mongo = Mongo.getInstance().imagesData
        return mongo.get(imageKey).read()


