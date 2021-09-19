from .connect_with_mongo import Mongo
from .dataObjects import Match, Tutor, Parent
from typing import Iterator


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

    def sendLike(self, match: Match) -> None:
        mongo = Mongo.getInstance()
        id = mongo.matchesData.insert_one({'parent_id': match.parent.id,
                                           'tutor_id': match.tutor.id,
                                           'status': Match.REQUESTED})
        match.id = id

    def sendDislike(self, match: Match) -> None:
        pass

    def nextTutor(self) -> Iterator[Tutor]:

        mongo = Mongo.getInstance()

        for i in mongo.tutorsData.find({}):
            obj = Tutor(i['_id'])
            obj.updateInfo(i)
            yield obj

    def getMatchesParent(self, parent: Parent, statusOfMatch):

        query = {'parent_id': parent.id,
                 'status': statusOfMatch}

        listOfMatches = []

        mongo = Mongo.getInstance()
        for obj in mongo.matchesData.find(query):
            tutor_id = obj['tutor_id']
            tutorInfo = mongo.tutorsData.find_one({'_id':tutor_id})
            tutorObj = Tutor(tutor_id)
            tutorObj.updateInfo(tutorInfo)

            matchObj = Match(parent, tutorObj)
            matchObj.id = obj['_id']
            matchObj.status = obj['status']

            listOfMatches.append(matchObj)

        return listOfMatches