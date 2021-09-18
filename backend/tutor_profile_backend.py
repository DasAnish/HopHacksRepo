
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

    def updateInfo(self, info):
        raise Exception("not implemented")