from backend import Backend, Tutor, Parent
from kivy.app import App
from kivy.base import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.config import Config
from kivy.graphics import *
from kivy.animation import *
from kivy.graphics import RoundedRectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from backend import Backend, Match, Level
import os

#Builder.load_file("kivyFiles/main.kv")
photoHeight = 550
photoWidth = 340

parent = {'username':'kelvincfleung', 'password':'hello123', 'fname':'Kelvin', 'lname':'Leung1', 'rateMin':10, 'rateMax':20, 'subject':'maths', 'level':1}
parentObj = Parent('61467ec2c2c5a2e917994d69')
parentObj.updateInfo(parent)


def getOrDefault(dictionary, key, default):
    if key in dictionary:
        return dictionary[key]
    else:
        return default


class PersonSingleTon:

    __instance = None

    @staticmethod
    def getInstance():
        if PersonSingleTon.__instance is None:
            PersonSingleTon()

        return PersonSingleTon.__instance

    def __init__(self):
        if PersonSingleTon.__instance is not None:
            raise Exception("Singleton: PersonSingleton")

        PersonSingleTon.__instance = self

        self.person = parentObj
        self.isTutor = False


def AddTextWithBack(widget, string, pos):
    if string is None or string.strip(" ") == "":
        return 0, None
    string = str(string)
    with widget.canvas:
        Color(0.95, 0.95, 0.95)
        back = RoundedRectangle(pos=pos, size=(0, 0))
    label = Label(text=string, pos=(pos[0]-40, pos[1]+3), color=(0, 0, 0), halign="left")
    label.texture_update()
    back.size = (label.texture_size[0] + 20, label.texture_size[1] + 10)
    label.size[1] = label.texture.size[1]
    label.pos = (label.pos[0] + label.texture.size[0] / 2, label.pos[1] - back.size[1])
    back.pos = (back.pos[0], back.pos[1] - back.size[1])
    widget.add_widget(label)
    return back.size[1], label


class ChangePageButton(Button):
    def __init__(self, PM, page, pos, size, source, color=(1, 1, 1), **kwargs):
        super(ChangePageButton, self).__init__(**kwargs)
        self.PM = PM
        self.page = page
        self.pos = pos
        self.size = size
        self.color = color
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.bind(on_press=self.pressed)

    def pressed(self, instance):
        self.PM.goToPage(self.page)


class FadeBetweenButton(Button):
    def __init__(self, images, pos, size, **kwargs):
        super(FadeBetweenButton, self).__init__(**kwargs)
        self.faded = 0
        self.images = images
        self.pos = pos
        self.size = size
        self.opacity = 0
        self.bind(on_press=self.pressed)
    def pressed(self, instance):
        if (self.faded == 0):
            Animation(opacity=0.5, duration=0.4).start(self.images[0])
            Animation(opacity=1, duration=0.4).start(self.images[1])
        else:
            Animation(opacity=1, duration=0.4).start(self.images[0])
            Animation(opacity=0, duration=0.4).start(self.images[1])
        self.faded = (self.faded + 1 ) % 2


class AcceptCardButton(Button):
    def __init__(self, page, source, pos, size, **kwargs):
        super(AcceptCardButton, self).__init__(**kwargs)
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.page = page
        self.pos = pos
        self.size = size
        self.bind(on_press=self.pressed)
        self.tutorObj = None
    def pressed(self, instance):
        parentObj = PersonSingleTon.getInstance().person

        match = Match(parentObj, self.tutorObj)

        Backend.sendLike(match)

        self.page.nextCard()
        # send match request

        parentObj = PersonSingleTon.getInstance()

        match = Match(parentObj, self.tutorObj)

        Backend.sendLike(match)


class RejectCardButton(Button):
    def __init__(self, page, source, pos, size, **kwargs):
        super(RejectCardButton, self).__init__(**kwargs)
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.page = page
        self.pos = pos
        self.size = size
        self.bind(on_press=self.pressed)
        self.tutorObj = None
    def pressed(self, instance):
        self.page.nextCard()


class AcceptRequestButton(Button):
    def __init__(self, page, request, label, source, pos, size, match, **kwargs):
        super(AcceptRequestButton, self).__init__(**kwargs)
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.pos = pos
        self.size = size
        self.bind(on_press=self.pressed)
        self.request = request
        self.page = page
        self.label = label
        self.match = match
    def pressed(self, instance):
        self.page.remove_widget(self.request)
        self.page.requestInfo.remove(self.label.text)
        self.page.updateRequests()
        # Confirm tutoring
        Backend.accept(self.match)
        # accept match
        tutorMatchesPage.updateMatches()


class RejectRequestButton(Button):
    def __init__(self, page, request, label, source, pos, size, match, **kwargs):
        super(RejectRequestButton, self).__init__(**kwargs)
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.pos = pos
        self.size = size
        self.bind(on_press=self.pressed)
        self.request = request
        self.label = label
        self.page = page
        self.match = match
    def pressed(self, instance):
        self.page.remove_widget(self.request)
        self.page.requestInfo.remove(self.label.text)
        self.page.updateRequests()
        # Reject tutoring
        # reject match
        Backend.reject(self.match)
        tutorMatchesPage.updateMatches()


class Card(Widget):
    def __init__(self, image, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.image = image



class SignInPage(Widget):
    def __init__(self, **kwargs):
        super(SignInPage, self).__init__(**kwargs)


class ParentHomePage(Widget):
    def __init__(self, **kwargs):
        super(ParentHomePage, self).__init__(**kwargs)
        #self.cards = [["images/kelvin1.png", ["Kelvin Leung", "BA Mathematics, Cambridge",
        #                                       "Tutors in:\n- Maths,\n- Physics,\n- Computer science",
        #                                       "For GCSE & A-Level students", "£30+/hr"]],
        #              ["images/businessMan.png", ["Coolvin Leung", "PhD Mathematics, Cambridge",
        #                                      "Tutors in: \n- Nothing", "£'a lot'/hr"]]]
        self.card = None

        # Yes/no buttons
        self.noButton = RejectCardButton(self, "images/noButton.png", (20, 100), (70, 70))
        self.yesButton = AcceptCardButton(self, "images/yesButton.png", (Window.width-90, 100), (70, 70))

        #self.noButton = Button(pos=(20, 100), size=(70, 70), background_normal="images/noButton.png",
        #                  background_down="images/noButtonDown.png")
        #self.yesButton = Button(pos=(Window.width-90, 100), size=(70, 70), background_normal="images/yesButton.png",
        #                  background_down="images/yesButtonDown.png")

        self.nextTutor = Backend.nextTutor()
        self.card = self.nextCard()

    def nextCard(self):
        # next tutor function
        nextItem = next(self.nextTutor, None)
        self.yesButton.tutorObj = nextItem
        self.noButton.tutorObj = nextItem
        print(nextItem.id, nextItem.fname)

        showYesNo = True

        if not nextItem:
            #: Handle end of cards
            info = []
            image = "images/businessMan.png"
            print("no cards left")
            showYesNo = False
            #pass
        else:
            info = [f"{nextItem.fname} {nextItem.lname}",
                    nextItem.qualification,
                    f"Tutors in:\n" +'\n'.join(nextItem.subject),
                    f"£{nextItem.rateMin}+/hr"]
            image = "images/kelvin1.png"

        # Image formatting
        img = Image(source=image, allow_stretch=True, pos=(10, 80),
                              size=(photoWidth, photoHeight))
        if img.texture_size[1]/img.texture_size[0] >  photoHeight/photoWidth:
            img.texture = img.texture.get_region(0, (img.texture_size[1] - img.texture_size[0] * photoHeight/photoWidth)/2, img.texture_size[0], img.texture_size[0] * photoHeight/photoWidth)
        else:
            img.texture = img.texture.get_region((img.texture_size[0] - img.texture_size[1] * photoWidth/photoHeight) / 2, 0, img.texture_size[1] * photoWidth/photoHeight, img.texture_size[1])
        card = Card(img)
        if (self.card != None):
            card.pos = (Window.width - photoWidth, self.card.pos[1])
        else:
            card.pos = (0, 0)
        card.add_widget(img)
        card.add_widget(Image(source="images/gradient.png", pos=(10, 80), size=(photoWidth, photoHeight)))
        card.add_widget(Image(source="images/border.png", pos=(10, 80), size=(photoWidth, photoHeight)))

        # Info formatting
        infoLabels = Widget(pos=(0, 0))
        startPos = (20, 600)
        pad = 20
        for string in info:
            height, label = AddTextWithBack(infoLabels, string, startPos)
            if (label is not None):
                startPos = (startPos[0], startPos[1] - height - pad)
        infoLabels.opacity = 0
        card.add_widget(infoLabels)

        # Tap to fade
        fadeButton = FadeBetweenButton([img, infoLabels], img.pos, img.size)
        card.add_widget(fadeButton)

        self.add_widget(card)
        self.remove_widget(self.card)

        #if (self.card != None):
            #print("hello")
            #Animation(pos=(self.card.pos[0], self.card.pos[1]), duration=0.4).start(card)
            #Animation(size=(0, 0), duration=0.4).start(self.card)

        #self.remove_widget(self.card)

        self.remove_widget(self.noButton)
        self.add_widget(self.noButton)
        self.remove_widget(self.yesButton)
        self.add_widget(self.yesButton)
        return card


class TutorHomePage(Widget):
    def __init__(self, **kwargs):
        super(TutorHomePage, self).__init__(**kwargs)
        global tutorHomePage
        tutorHomePage = self
        self.add_widget(Label(text="Requests", color=(0, 0, 0), pos=(60, 550), font_size="40sp"))
        self.requests = []
        #: get requested matched
        self.requestInfo = []
        self.listOfMatches = []
            #["Villar\nKS3 Mathematics, 5/hr", "Kiln\nKS2 English, £600/hr", "Das\nGCSE Spanish, £60/hr",
            #               "Samuels\nA-Level Chemistry, £30/hr"]
        self.updateRequests()

    def updateRequestsInfo(self):

        personObj = PersonSingleTon.getInstance()
        self.listOfMatches = Backend.getMatchesTutor(personObj.person, Match.REQUESTED)

        def convertMatchToString(match):
            output = ''
            parent = match.parent
            output += parent.lname + "\n"

            if parent.level == Level.ALEVEL:
                output += 'A-Level, '
            elif parent.level == Level.GCSE:
                output += 'GCSE, '
            elif parent.level == Level.KS3:
                output += 'KS3, '
            elif parent.level == Level.KS2:
                output += 'KS2, '

            output += f"£{parent.rateMax}/hr"

            return output

        self.requestInfo = [convertMatchToString(i) for i in self.listOfMatches]
        print(self.requestInfo)

    def updateRequests(self):
        self.updateRequestsInfo()
        for request in self.requests:
            self.remove_widget(request)
        pad = 10
        startPos = (20, 550)
        for i in range(0, len(self.requestInfo)):
            self.requests.append(Widget(pos=(0, 0)))
            height, label = AddTextWithBack(self.requests[i], self.requestInfo[i], startPos)
            self.requests[i].add_widget(AcceptRequestButton(self, self.requests[i], label, "images/smallYesButton.png",
                                                            (Window.width - 115, startPos[1] - 50), (50, 50),
                                                            self.listOfMatches[i]))
            self.requests[i].add_widget(RejectRequestButton(self, self.requests[i], label, "images/smallNoButton.png",
                                                            (Window.width - 60, startPos[1] - 50), (50, 50),
                                                            self.listOfMatches[i]))
            startPos = (startPos[0], startPos[1] - height - pad)
            self.add_widget(self.requests[i])


# KELVIN GO HERE
#360*640
class ParentProfile(Widget):
    def __init__(self, **kwargs):
        person = PersonSingleTon.getInstance().person

        super(ParentProfile, self).__init__(**kwargs)
        self.grid = GridLayout(cols=2, pos=(0,80), size=(360,520), spacing=(0,10), padding=(0,0,20,0))

        self.profileLabel = Label(text="Profile Picture:", color=(0, 0, 0), font_size="18sp",width=90, size_hint_y=6)
        self.profilepicture = Button(background_normal='images/kelvin1.png')
        self.profilepicture.bind(on_press=self.pictureChanger)

        self.usernameLabel = Label(text="Username:", color=(0, 0, 0), font_size="18sp",width=90)
        self.usernameText = TextInput(text=person.username,background_color=(.95, .95, .95, 1))

        self.passwordLabel = Label(text="Password:", color=(0, 0, 0), font_size="18sp",width=90)
        self.passwordText = TextInput(text=person.password, background_color=(.95, .95, .95, 1))

        self.phoneNumLabel = Label(text="Phone:", color=(0, 0, 0),  font_size="18sp",width=90)
        self.phoneNumText = TextInput(text=str(person.phoneNum), background_color=(.95, .95, .95, 1))

        self.fnameLabel = Label(text="First Name:", color=(0, 0, 0), font_size="18sp",width=90)
        self.fnameText = TextInput(text=person.fname, background_color=(.95, .95, .95, 1))

        self.lnameLabel = Label(text="Last Name:", color=(0, 0, 0), font_size="18sp",width=90)
        self.lnameText = TextInput(text=person.lname, background_color=(.95, .95, .95, 1))

        self.subjectLabel = Label(text="Subject:", color=(0, 0, 0), font_size="18sp",width=90)
        self.subjectText = GridLayout(cols=2)
        self.subjectbtn1 = ToggleButton(text='Maths', group='subject', )
        self.subjectbtn2 = ToggleButton(text='English', group='subject', state='down')

        self.rateMinLabel = Label(text="Minimum Rate:", color=(0, 0, 0),  font_size="18sp",width=90)
        self.rateMinText = GridLayout(cols=1)
        self.rateMinTextSlider = Slider(value_track= True, min=0, max=100, step=1, value=person.rateMin,
                                        value_track_color=(0,0.5,0.5,0.7))
        self.rateMinTextSlider.bind(value=self.onValueMin)
        self.rateMinTextText = Label(text='£'+str(self.rateMinTextSlider.value), color=(0, 0, 0), font_size="18sp")

        self.rateMaxLabel = Label(text="Maximum Rate:", color=(0, 0, 0),  font_size="18sp",width=90)
        self.rateMaxText = GridLayout(cols=1)
        self.rateMaxTextSlider = Slider(value_track= True, min=0, max=100, step=1, value=person.rateMax,
                                        value_track_color=(0,0.5,0.5,0.7))
        self.rateMaxTextText = Label(text='£'+str(self.rateMaxTextSlider.value), color=(0, 0, 0),  font_size="18sp")
        self.rateMaxTextSlider.bind(value=self.onValueMax)

        self.levelLabel = Label(text="Tutee Level:", color=(0, 0, 0), font_size="18sp",width=90)
        self.levelText = GridLayout(cols=2)
        self.levelbtn1 = ToggleButton(text='GCSE', group='level', )
        self.levelbtn2 = ToggleButton(text='A-LEVEL', group='level', state='down')

        self.add_widget(self.grid)
        self.grid.add_widget(self.profileLabel)
        self.grid.add_widget(self.profilepicture)
        self.grid.add_widget(self.usernameLabel)
        self.grid.add_widget(self.usernameText)
        self.grid.add_widget(self.passwordLabel)
        self.grid.add_widget(self.passwordText)
        self.grid.add_widget(self.phoneNumLabel)
        self.grid.add_widget(self.phoneNumText)
        self.grid.add_widget(self.fnameLabel)
        self.grid.add_widget(self.fnameText)
        self.grid.add_widget(self.lnameLabel)
        self.grid.add_widget(self.lnameText)
        self.grid.add_widget(self.subjectLabel)
        self.grid.add_widget(self.subjectText)
        self.subjectText.add_widget(self.subjectbtn1)
        self.subjectText.add_widget(self.subjectbtn2)
        self.grid.add_widget(self.rateMinLabel)
        self.grid.add_widget(self.rateMinText)
        self.rateMinText.add_widget(self.rateMinTextSlider)
        self.rateMinText.add_widget(self.rateMinTextText)
        self.grid.add_widget(self.rateMaxLabel)
        self.grid.add_widget(self.rateMaxText)
        self.rateMaxText.add_widget(self.rateMaxTextSlider)
        self.rateMaxText.add_widget(self.rateMaxTextText)
        self.grid.add_widget(self.levelLabel)
        self.grid.add_widget(self.levelText)
        self.levelText.add_widget(self.levelbtn1)
        self.levelText.add_widget(self.levelbtn2)

    def pictureChanger(self, popup):
        popup = Popup(title='Change your profile', size_hint=(None, None), size=(300, 400), auto_dismiss=False)
        temp_cont = GridLayout(cols=1,spacing=(0,20), padding=(5,0,5,0))
        text = Label(text='Please enter the path of your new picture.')
        text_input = TextInput(text='')
        btn_choice = GridLayout(cols=2,size_hint_y=0.4)
        btn1 = Button(text='Confirm')
        btn2 = Button(text='Cancel')
        btn_choice.add_widget(btn1)
        btn_choice.add_widget(btn2)
        temp_cont.add_widget(text)
        temp_cont.add_widget(text_input)
        temp_cont.add_widget(btn_choice)
        btn1.bind(on_press=self.pictureChangerCheck(popup, text_input))
        btn2.bind(on_press=popup.dismiss)
        popup.content = temp_cont
        popup.open()

    @staticmethod
    def pictureChangerCheck(popup, check):
        if os.path.exists(check.text):
            imageKey = Backend.getImageKey(check.text)
            tutor: Tutor = PersonSingleTon.getInstance().person
            tutor.picture = imageKey

            imageBytes = Backend.getImageBytes(imageKey)
            with open('images/temp.png', 'wb') as f:
                f.write(imageBytes)
        popup.dismiss()

    def onValueMin(self, instance, value):
        self.rateMinTextText.text = '£' + str(int(value))

    def onValueMax(self, instance, value):
        self.rateMaxTextText.text = '£' + str(int(value))


class TutorProfile(Widget):
    def __init__(self, **kwargs):
        super(TutorProfile, self).__init__(**kwargs)

class ParentMatches(Widget):
    def __init__(self, **kwargs):
        super(ParentMatches, self).__init__(**kwargs)
        global parentMatchesPage
        parentMatchesPage = self
        self.add_widget(Label(text="Tutors", color=(0, 0, 0), pos=(40, 550), font_size="40sp"))
        self.matches = []
        # TODO: get matched parents

        # self.matchInfo = [
        #     "Kelvin Leung\nBA Mathematics, Cambridge\nTutors in:\n- Maths,\n- Physics,\n- Computer science"
        #     "\n£30+/hr\n\nContact at:\n077777888999, leung@gmail.com"]
        self.updateMatches()

    def updateMatchInfo(self):
        parent = PersonSingleTon.getInstance().person
        listOfMatches = Backend.getMatchesParent(parent, Match.ACCEPTED)

        def matchToString(match: Match):
            tutor = match.tutor
            subjects = '-' + '\n-'.join(tutor.subject)
            output = (f"{tutor.fname} {tutor.lname}\n"
                      f"{tutor.qualification}\n"
                      f"Tutors in:\n{subjects}\n"
                      f"£{tutor.rateMin}+/hr\n\n"
                      f"Contact at:\n{tutor.phoneNum}")
            return output

        self.matchInfo = [matchToString(m) for m in listOfMatches]
        print(self.matchInfo)

    def updateMatches(self):
        self.updateMatchInfo()
        for match in self.matches:
            self.remove_widget(self.matches)
        pad = 10
        startPos = (20, 550)
        for i in range(0, len(self.matchInfo)):
            self.matches.append(Widget(pos=(0, 0)))
            height, label = AddTextWithBack(self.matches[i], self.matchInfo[i], startPos)
            # self.matches[i].add_widget(AcceptRequestButton(self, self.matches[i], label, "images/smallYesButton.png",
            #                                                (Window.width - 115, startPos[1] - 50), (50, 50)))
            # self.matches[i].add_widget(RejectRequestButton(self, self.matches[i], label, "images/smallNoButton.png",
            #                                                (Window.width - 60, startPos[1] - 50), (50, 50)))
            startPos = (startPos[0], startPos[1] - height - pad)
            self.add_widget(self.matches[i])

class TutorMatches(Widget):
    def __init__(self, **kwargs):
        super(TutorMatches, self).__init__(**kwargs)
        global tutorMatchesPage
        tutorMatchesPage = self
        self.add_widget(Label(text="Tutees", color=(0, 0, 0), pos=(40, 550), font_size="40sp"))
        self.matches = []
        # TODO: get matched tutors


        self.matchInfo = ["Villar\nKS3 Mathematics, £5/hr\n\nContact at:\n077777888999, villar@gmail.com", "Kiln\nKS2 English, £600/hr\n\nContact at:\n077777888999, kiln@gmail.com",
                          "Das\nGCSE Spanish, £60/hr\n\nContact at:\n077777888999, das@gmail.com", "Samuels\nA-Level Chemistry, £30/hr\n\nContact at:\n077777888999, samuels@gmail.com"]
        self.updateMatches()

    def updateMatchInfo(self):
        tutor = PersonSingleTon.getInstance().person
        listOfMatches = Backend.getMatchesTutor(tutor, Match.ACCEPTED)

        def matchToString(match):
            parent = match.parent

            if parent.level == Level.ALEVEL:
                level = 'A-Level'
            elif parent.level == Level.GCSE:
                level = 'GCSE'
            elif parent.level == Level.KS3:
                level = 'KS3'
            else:
                level = 'KS2'

            output = (f"{parent.lname}\n"
                      f"{level} {parent.subject}, £{parent.rateMax}/hr\n\n"
                      f"Contact at:\n"
                      f"{parent.phoneNum}")

            return output

        self.matchInfo = [matchToString(m) for m in listOfMatches]
        print(self.matchInfo)

    def updateMatches(self):
        self.updateMatchInfo()
        print("match info: ", self.matchInfo)
        for match in self.matches:
            self.remove_widget(self.matches)
        pad = 10
        startPos = (20, 550)
        for i in range(0, len(self.matchInfo)):
            self.matches.append(Widget(pos=(0, 0)))
            height, label = AddTextWithBack(self.matches[i], self.matchInfo[i], startPos)
            #self.matches[i].add_widget(AcceptRequestButton(self, self.matches[i], label, "images/smallYesButton.png",
            #                                                (Window.width - 115, startPos[1] - 50), (50, 50)))
            #self.matches[i].add_widget(RejectRequestButton(self, self.matches[i], label, "images/smallNoButton.png",
            #                                                (Window.width - 60, startPos[1] - 50), (50, 50)))
            startPos = (startPos[0], startPos[1] - height - pad)
            self.add_widget(self.matches[i])


class PageManager(Widget):
    HOME = 0
    PROFILE = 2
    MATCHES = 4

    def __init__(self, **kwargs):
        super(PageManager, self).__init__(**kwargs)
        Window.size = (360, 640)
        self.isTutor = False#isinstance(person, Tutor)
        self.size = (360, 640)
        self.currentPage = 0 + self.isTutor
        self.pages = [ParentHomePage(), TutorHomePage(), ParentProfile(), TutorProfile(), ParentMatches(), TutorMatches()]

        with self.canvas:
            self.bgCanvas = Rectangle(pos=(0, 0), size=(self.width, self.height))#70))

        self.add_widget(self.pages[self.currentPage])

        self.homeButton = ChangePageButton(self, PageManager.HOME + self.isTutor, (10, 15), (50, 50), "images/homeButton.png")
        self.add_widget(self.homeButton)

        self.matchesButton = ChangePageButton(self, PageManager.MATCHES + self.isTutor, (Window.width/2 - 25, 15), (50, 50), "images/starButton.png")
        self.add_widget(self.matchesButton)

        self.profileButton = ChangePageButton(self, PageManager.PROFILE + self.isTutor, (self.width - 60, 15), (50, 50), "images/profileButton.png")
        self.add_widget(self.profileButton)

    def goToPage(self, page):
        self.remove_widget(self.pages[self.currentPage])
        self.currentPage = page + self.isTutor
        self.add_widget(self.pages[self.currentPage])

    def updateUser(self, person):
        PersonSingleTon.getInstance().person = person
        self.isTutor = isinstance(person, Tutor)
        self.goToPage(0)
        tutorHomePage.updateRequests()
        tutorMatchesPage.updateMatches()
        parentMatchesPage.updateMatches()
        #self.currentPage += self.isTutor


class MainApp(App):
    def build(self):
        return PageManager()


if __name__ == '__main__':
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')
    Config.set('graphics', 'resizable', False)
    MainApp().run()