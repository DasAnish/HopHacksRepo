from .connect_with_mongo import Mongo
from .dataObjects import Parent, Tutor
from typing import Dict


class SignInBackend:

    __instance = None

    @staticmethod
    def getInstance():
        if SignInBackend.__instance is None:
            SignInBackend()

        return SignInBackend.__instance

    def __init__(self):
        if SignInBackend.__instance is not None:
            raise Exception("This class is a singleton!")

        else:
            SignInBackend.__instance = self

    def signUpVerification(self, loginInfo: Dict):
        print('signup', loginInfo)
        username = loginInfo['username']
        isTutor = loginInfo['isTutor']

        mongo = Mongo.getInstance()
        query = {"username": username}

        if mongo.tutorsData.count_documents(query) != 0:
            return False
        if mongo.parentsData.count_documents(query) != 0:
            return False

        if isTutor:
            collection = mongo.tutorsData
            creator = Tutor
        else:
            collection = mongo.parentsData
            creator = Parent

        del loginInfo['isTutor']

        _id = collection.insert_one(loginInfo)

        obj = creator(_id)
        obj.updateInfo(loginInfo)

        return True

    def signInVerification(self, loginInfo: Dict):
        username = loginInfo['username']
        password = loginInfo['password']
        isTutor = loginInfo['isTutor']

        mongo = Mongo.getInstance()

        query = {"username": username}
        if isTutor:
            if mongo.tutorsData.count_documents(query) == 0:
                return
            output = mongo.tutorsData.find(query)[0]
            creator = Tutor

        else:
            if mongo.parentsData.count_documents(query) == 0:
                return
            output = mongo.parentsData.find(query)[0]
            creator = Parent

        if output['password'] != password:
            return

        obj = creator(output['_id'])
        obj.updateInfo(output)

        return obj





