from .connect_with_mongo import Mongo
from .dataObjects import Match, Tutor


class ParentsHomeBackend:

    __instance = None

    @staticmethod
    def getInstance():
        if ParentsHomeBackend.__instance is None:
            ParentsHomeBackend()

        return ParentsHomeBackend.__instance

    def __init__(self):
        if ParentsHomeBackend.__instance is not None:
            raise Exception("This class is a singleton!")

        else:
            ParentsHomeBackend.__instance = self

    def sendLike(self, match: Match):
        mongo = Mongo.getInstance()
        id = mongo.matchesData.insert_one({'parent_id': match.parent.id,
                                           'tutor_id': match.tutor.id,
                                           'status': Match.REQUESTED})
        match.id = id

    def sendDislike(self, match: Match):
        pass

    def nextTutor(self):

        mongo = Mongo.getInstance()

        for i in mongo.tutorsData.find({}):
            obj = Tutor(i['_id'])
            obj.updateInfo(i)
            yield obj