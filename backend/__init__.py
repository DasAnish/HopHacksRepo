from .parents_home_backend import ParentsHomeBackend
from .parents_profile_backend import ParentsProfileBackend
from .tutor_profile_backend import TutorProfileBackend
from .tutor_home_backend import TutorHomeBackend
from .sign_in_backend import SignInBackend
from .connect_with_mongo import Mongo
from .dataObjects import *


class Backend:

    @staticmethod
    def sendLike(match):
        ParentsHomeBackend.getInstance().sendLike(match)

    @staticmethod
    def sendDislike(match):
        ParentsHomeBackend.getInstance().sendDislike(match)

    @staticmethod
    def updateParentInfo(info):
        ParentsProfileBackend.getInstance().updateInfo(info)

    @staticmethod
    def updateTutorInfo(info):
        TutorProfileBackend.getInstance().updateInfo(info)

    @staticmethod
    def signUpVerification(loginInfo):
        SignInBackend.getInstance().signUpVerification(loginInfo)

    @staticmethod
    def signInVerification(loginInfo):
        SignInBackend.getInstance().signInVerification(loginInfo)

    @staticmethod
    def accept(match):
        TutorHomeBackend.getInstance().accept(match)

    @staticmethod
    def reject(match):
        TutorHomeBackend.getInstance().reject(match)
