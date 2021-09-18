

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

    def updateInfo(self, info):
        raise Exception("not implemented")