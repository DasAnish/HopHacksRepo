from .connect_with_mongo import Mongo
from .dataObjects import Match


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

        self.cursor = None

    def sendLike(self, match: Match):
        mongo = Mongo.getInstance()
        id = mongo.matchesData.insert_one({'parent_id': match.parent.id,
                                           'tutor_id': match.tutor.id,
                                           'status': Match.REQUESTED})
        match.id = id

    def sendDislike(self, match: Match):
        pass

    def nextTutor(self):

        if self.cursor is None:
            mongo = Mongo.getInstance()
            self.cursor = mongo.tutorsData.find({})

        if self.cursor.alive():
            return self.cursor.next()
        else:
            return False
