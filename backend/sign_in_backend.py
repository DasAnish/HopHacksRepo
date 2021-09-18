from backend import Mongo
from backend import Parent, Tutor


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

    def signUpVerification(self, loginInfo):
        username = loginInfo['username']
        isTutor = loginInfo['isTutor']

        mongo = Mongo.getInstance()

        if isTutor:
            collection = mongo.tutorsData
            creator = Tutor
        else:
            collection = mongo.parentsData
            creator = Parent

        # checking that the username does not exists
        query = {"username": username}
        output = collection.find(query)

        if output.count_documents() != 0:
            return False

        del loginInfo['isTutor']

        _id = collection.insert_one(loginInfo)

        obj = creator(_id)
        obj.updateInfo(loginInfo)

        return True

    def signInVerification(self, loginInfo):
        username = loginInfo['username']
        password = loginInfo['password']
        isTutor = loginInfo['isTutor']

        mongo = Mongo.getInstance()

        query = {"username": username}
        if isTutor:
            output = mongo.tutorsData.find(query)
        else:
            output = mongo.parentsData.find(query)

        if not output.count_documents():
            return False

        output = output[0]

        return output['password'] == password


