
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

    def verify(self, loginInfo):
        raise Exception("not implemented")


