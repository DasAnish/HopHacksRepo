from backend import Backend, Tutor
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


Builder.load_file("kivyFiles/main.kv")
photoHeight = 550
photoWidth = 340


def AddTextWithBack(widget, str, pos):
    with widget.canvas:
        Color(0.95, 0.95, 0.95)
        back = RoundedRectangle(pos=pos, size=(0, 0))
    label = Label(text=str, pos=(pos[0]-40, pos[1]+3), color=(0, 0, 0), halign="left")
    label.texture_update()
    back.size = (label.texture_size[0] + 20, label.texture_size[1] + 10)
    label.size[1] = label.texture.size[1]
    label.pos = (label.pos[0] + label.texture.size[0] / 2, label.pos[1] - back.size[1])
    back.pos = (back.pos[0], back.pos[1] - back.size[1])
    widget.add_widget(label)
    return back.size[1], label


class ChangePageButton(Button):
    def __init__(self, page, pos, size, source, color=(1, 1, 1), **kwargs):
        super(ChangePageButton, self).__init__(**kwargs)
        self.page = page
        self.pos = pos
        self.size = size
        self.color = color
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.bind(on_press=self.pressed)

    def pressed(self, instance):
        app = App.get_running_app()
        PM = app.root
        PM.goToPage(self.page)


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
    def pressed(self, instance):
        self.page.nextCard()
        # TODO send match request

class RejectCardButton(Button):
    def __init__(self, page, source, pos, size, **kwargs):
        super(RejectCardButton, self).__init__(**kwargs)
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.page = page
        self.pos = pos
        self.size = size
        self.bind(on_press=self.pressed)
    def pressed(self, instance):
        self.page.nextCard()


class AcceptRequestButton(Button):
    def __init__(self, page, request, label, source, pos, size, **kwargs):
        super(AcceptRequestButton, self).__init__(**kwargs)
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.pos = pos
        self.size = size
        self.bind(on_press=self.pressed)
        self.request = request
        self.page = page
        self.label = label
    def pressed(self, instance):
        self.page.remove_widget(self.request)
        self.page.requestInfo.remove(self.label.text)
        self.page.updateRequests()
        # Confirm tutoring
        # TODO accept match


class RejectRequestButton(Button):
    def __init__(self, page, request, label, source, pos, size, **kwargs):
        super(RejectRequestButton, self).__init__(**kwargs)
        self.background_normal = source
        self.background_down = source.replace(".png", "") + "Down" + ".png"
        self.pos = pos
        self.size = size
        self.bind(on_press=self.pressed)
        self.request = request
        self.label = label
        self.page = page
    def pressed(self, instance):
        self.page.remove_widget(self.request)
        self.page.requestInfo.remove(self.label.text)
        self.page.updateRequests()
        # Reject tutoring
        # TODO reject match


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
        self.cards = [["images/kelvin1.png", ["Kelvin Leung", "BA Mathematics, Cambridge",
                                               "Tutors in:\n- Maths,\n- Physics,\n- Computer science",
                                               "For GCSE & A-Level students", "£30+/hr"]],
                      ["images/businessMan.png", ["Coolvin Leung", "PhD Mathematics, Cambridge",
                                              "Tutors in: \n- Nothing", "£'a lot'/hr"]]]
        self.card = None

        # Yes/no buttons
        self.noButton = RejectCardButton(self, "images/noButton.png", (20, 100), (70, 70))
        self.yesButton = RejectCardButton(self, "images/yesButton.png", (Window.width-90, 100), (70, 70))

        #self.noButton = Button(pos=(20, 100), size=(70, 70), background_normal="images/noButton.png",
        #                  background_down="images/noButtonDown.png")
        #self.yesButton = Button(pos=(Window.width-90, 100), size=(70, 70), background_normal="images/yesButton.png",
        #                  background_down="images/yesButtonDown.png")

        self.card = self.nextCard()

    def nextCard(self):
        # TODO next tutor function
        nextCardInfo = self.cards.pop(0)

        image = nextCardInfo[0]
        info = nextCardInfo[1]

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
        self.add_widget(Label(text="Requests", color=(0, 0, 0), pos=(60, 550), font_size="40sp"))
        self.requests = []
        # TODO: get requested matched
        self.requestInfo = ["Villar\nKS3 Mathematics, £5/hr", "Kiln\nKS2 English, £600/hr", "Das\nGCSE Spanish, £60/hr",
                            "Samuels\nA-Level Chemistry, £30/hr"]
        self.updateRequests()
    def updateRequests(self):
        for request in self.requests:
            self.remove_widget(request)
        pad = 10
        startPos = (20, 550)
        for i in range(0, len(self.requestInfo)):
            self.requests.append(Widget(pos=(0, 0)))
            height, label = AddTextWithBack(self.requests[i], self.requestInfo[i], startPos)
            self.requests[i].add_widget(AcceptRequestButton(self, self.requests[i], label, "images/smallYesButton.png",
                                                            (Window.width - 115, startPos[1] - 50), (50, 50)))
            self.requests[i].add_widget(RejectRequestButton(self, self.requests[i], label, "images/smallNoButton.png",
                                                            (Window.width - 60, startPos[1] - 50), (50, 50)))
            startPos = (startPos[0], startPos[1] - height - pad)
            self.add_widget(self.requests[i])

# KELVIN GO HERE
class ParentProfile(Widget):
    def __init__(self, **kwargs):
        super(ParentProfile, self).__init__(**kwargs)

class TutorProfile(Widget):
    def __init__(self, **kwargs):
        super(TutorProfile, self).__init__(**kwargs)

class ParentMatches(Widget):
    def __init__(self, **kwargs):
        super(ParentMatches, self).__init__(**kwargs)
        self.add_widget(Label(text="Tutors", color=(0, 0, 0), pos=(40, 550), font_size="40sp"))
        self.matches = []
        # TODO: get matched parents
        self.matchInfo = [
            "Kelvin Leung\nBA Mathematics, Cambridge\nTutors in:\n- Maths,\n- Physics,\n- Computer science"
            "\n£30+/hr\n\nContact at:\n077777888999, leung@gmail.com"]
        self.updateMatches()

    def updateMatches(self):
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
        self.add_widget(Label(text="Tutees", color=(0, 0, 0), pos=(40, 550), font_size="40sp"))
        self.matches = []
        # TODO: get matched parents
        self.matchInfo = ["Villar\nKS3 Mathematics, £5/hr\n\nContact at:\n077777888999, villar@gmail.com", "Kiln\nKS2 English, £600/hr\n\nContact at:\n077777888999, kiln@gmail.com",
                          "Das\nGCSE Spanish, £60/hr\n\nContact at:\n077777888999, das@gmail.com", "Samuels\nA-Level Chemistry, £30/hr\n\nContact at:\n077777888999, samuels@gmail.com"]
        self.updateMatches()

    def updateMatches(self):
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
        self.isTutor = False#isinstance(person, Tutor)
        self.size = (360, 640)
        self.currentPage = 0 + self.isTutor
        self.pages = [ParentHomePage(), TutorHomePage(), ParentProfile(), TutorProfile(), ParentMatches(), TutorMatches()]

        with self.canvas:
            self.bgCanvas = Rectangle(pos=(0, 0), size=(self.width, self.height))#70))

        self.add_widget(self.pages[self.currentPage])

        self.homeButton = ChangePageButton(PageManager.HOME + self.isTutor, (10, 15), (50, 50), "images/homeButton.png")
        self.add_widget(self.homeButton)

        self.matchesButton = ChangePageButton(PageManager.MATCHES + self.isTutor, (Window.width/2 - 25, 15), (50, 50), "images/starButton.png")
        self.add_widget(self.matchesButton)

        self.profileButton = ChangePageButton(PageManager.PROFILE + self.isTutor, (self.width - 60, 15), (50, 50), "images/profileButton.png")
        self.add_widget(self.profileButton)

    def goToPage(self, page):
        self.remove_widget(self.pages[self.currentPage])
        self.currentPage = page
        self.add_widget(self.pages[self.currentPage])


class MainApp(App):
    def build(self):
        return PageManager()


if __name__ == '__main__':
    Window.size = (360, 640)
    Config.set('graphics', 'resizable', False)
    MainApp().run()