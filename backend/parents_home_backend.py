

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

    def sendLike(self, matches):
        raise Exception("not implemented")

    def sendDislike(self, matches):
        raise Exception("not implemented")