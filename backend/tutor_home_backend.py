from .dataObjects import Tutor, Parent, Match
from .connect_with_mongo import Mongo


class TutorHomeBackend:

    __instance = None

    @staticmethod
    def getInstance():
        if TutorHomeBackend.__instance is None:
            TutorHomeBackend()

        return TutorHomeBackend.__instance

    def __init__(self):
        if TutorHomeBackend.__instance is not None:
            raise Exception("This class is a singleton!")

        else:
            TutorHomeBackend.__instance = self

    def getMatchesTutor(self, tutor: Tutor, statusOfMatch):

        query = {'tutor_id': tutor.id,
                 'status': statusOfMatch}

        mongo = Mongo.getInstance()
        print("tutor.id: ", tutor.id)
        print('query', query)
        print('query count: ', mongo.matchesData.count_documents(query))

        listOfMatches = []


        for obj in mongo.matchesData.find(query):
            print(f"parent_id: {obj['parent_id']}")
            parent_id = obj['parent_id']
            print('count', mongo.parentsData.count_documents({'_id': parent_id}))
            parentInfo = mongo.parentsData.find_one({'_id':parent_id})
            parentObj = Parent(parent_id)
            parentObj.updateInfo(parentInfo)

            matchObj = Match(parentObj, tutor)
            matchObj.id = obj['_id']
            matchObj.status = obj['status']

            listOfMatches.append(matchObj)

        return listOfMatches

    def accept(self, match: Match):

        query = {'_id':match.id}
        matchesData = Mongo.getInstance().matchesData
        matchesData.update_one(query, {'$set': {'status': Match.ACCEPTED}})

    def reject(self, match: Match):

        query = {'_id':match.id}
        matchesData = Mongo.getInstance().matchesData
        matchesData.update_one(query, {'$set': {'status': Match.ACCEPTED}})


