from .parents_home_backend import ParentsHomeBackend
from .parents_profile_backend import ParentsProfileBackend
from .tutor_profile_backend import TutorProfileBackend
from .tutor_home_backend import TutorHomeBackend
from .sign_in_backend import SignInBackend
from .connect_with_mongo import Mongo
from .dataObjects import *


class Backend:

    @staticmethod
    def getMatchesParent(parent, statusOfMatch):
        return ParentsHomeBackend.getInstance().getMatchesParent(parent, statusOfMatch)

    @staticmethod
    def getMatchesTutor(tutor, statusOfMatch):
        return TutorHomeBackend.getInstance().getMatchesTutor(tutor, statusOfMatch)

    @staticmethod
    def nextTutor():
        return ParentsHomeBackend.getInstance().nextTutor()

    @staticmethod
    def sendLike(match):
        ParentsHomeBackend.getInstance().sendLike(match)

    @staticmethod
    def sendDislike(match):
        ParentsHomeBackend.getInstance().sendDislike(match)

    @staticmethod
    def updateParentInfo(parentObj, info):
        ParentsProfileBackend.getInstance().updateInfo(parentObj, info)

    @staticmethod
    def updateTutorInfo(tutorObj, info):
        TutorProfileBackend.getInstance().updateInfo(tutorObj, info)

    @staticmethod
    def signUpVerification(loginInfo):
        return SignInBackend.getInstance().signUpVerification(loginInfo)

    @staticmethod
    def signInVerification(loginInfo):
        return SignInBackend.getInstance().signInVerification(loginInfo)

    @staticmethod
    def accept(match):
        TutorHomeBackend.getInstance().accept(match)

    @staticmethod
    def reject(match):
        TutorHomeBackend.getInstance().reject(match)

    @staticmethod
    def getImageKey(imagePath: str):
        return TutorProfileBackend.getInstance().getImageKey(imagePath)

    @staticmethod
    def getImageBytes(imageKey):
        return TutorProfileBackend.getInstance().getImageBytes(imageKey)
