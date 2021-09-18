
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

    def accept(self, match):
        raise Exception("not implemented")

    def reject(self, match):
        raise Exception("not implemented")


