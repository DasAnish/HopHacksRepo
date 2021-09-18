from backend import Backend
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


#fadeInFull = Animation(opacity = 1, duration = 0.4)
#fadeOut = Animation(opacity = 0, duration = 0.4)

def AddTextWithBack(widget, str, pos):
    print(pos)
    with widget.canvas:
        Color(0.95, 0.95, 0.95)
        back = RoundedRectangle(pos=pos, size=(0, 0))
    text = Label(text=str, pos=(pos[0]-40, pos[1]+3), color=(0, 0, 0), halign="left")
    text.texture_update()
    back.size = (text.texture_size[0] + 20, text.texture_size[1] + 10)
    text.size[1] = text.texture.size[1]
    text.pos = (text.pos[0] + text.texture.size[0] / 2, text.pos[1] - back.size[1])
    back.pos = (back.pos[0], back.pos[1] - back.size[1])
    widget.add_widget(text)
    return back.size[1]

class ChangePageButton(Button):
    def __init__(self, page, pos, size, source, **kwargs):
        super(ChangePageButton, self).__init__(**kwargs)
        self.page = page
        self.pos = pos
        self.size = size
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


class SignInPage(Widget):
    def __init__(self, **kwargs):
        super(SignInPage, self).__init__(**kwargs)


class ParentHomePage(Widget):
    def __init__(self, **kwargs):
        super(ParentHomePage, self).__init__(**kwargs)

        # Image formatting
        img = Image(source="images/kelvin1.png", allow_stretch=True, pos=(10, 80),
                              size=(340, 550))
        img.texture = img.texture.get_region(0, 0, img.texture_size[0], img.texture_size[0] * 550/340)
        self.add_widget(img)
        self.add_widget(Image(source="images/gradient.png", pos=(10, 80), size=(340, 550)))

        # Info formatting
        info = Widget(pos=(0, 0))
        startPos = (20, 600)
        pad = 20
        infoToDisplay = ["Kelvin Leung", "BA Mathematics, Cambridge", "Tutors in:\n- Maths,\n- Physics,\n- Computer science",
                         "For GCSE & A-Level students", "£30+/hr"]
        for string in infoToDisplay:
            print(string)
            startPos = (startPos[0], startPos[1] - AddTextWithBack(info, string, startPos) - pad)
        info.opacity = 0
        self.add_widget(info)

        # Tap to fade
        fadeButton = FadeBetweenButton([img, info], img.pos, img.size)
        self.add_widget(fadeButton)

        # Yes/no buttons
        noButton = Button(pos=(20, 100), size=(70, 70), background_normal="images/noButton.png",
                          background_down="images/noButtonDown.png")
        self.add_widget(noButton)
        yesButton = Button(pos=(Window.width-90, 100), size=(70, 70), background_normal="images/yesButton.png",
                          background_down="images/yesButtonDown.png")
        self.add_widget(yesButton)



class TutorHomePage(Widget):
    def __init__(self, **kwargs):
        super(TutorHomePage, self).__init__(**kwargs)
        requests = []
        infoToDisplay = ["Villar\nKS3 Mathematics, £5/hr", "Kiln\nKS2 English, £600/hr"]
        pad = 10
        startPos = (20, 600)
        for i in range(0, len(infoToDisplay)):
            requests.append(Widget(pos=(0, 0)))
            startPos = (startPos[0], startPos[1] - AddTextWithBack(requests[i], infoToDisplay[i], startPos) - pad)
            self.add_widget(requests[i])


class ParentProfile(Widget):
    def __init__(self, **kwargs):
        super(ParentProfile, self).__init__(**kwargs)
        img = Image(source="images/kelvin2.png", allow_stretch=True, pos=(10, 80),
                              size=(Window.width - 20, Window.height - 90))
        img.texture = img.texture.get_region(0, 0, img.texture_size[0], img.texture_size[0] * 550 / 340)
        self.add_widget(img)


class TutorProfile(Widget):
    def __init__(self, **kwargs):
        super(TutorProfile, self).__init__(**kwargs)


class PageManager(Widget):
    SIGNIN = 0
    HOME = 1
    PROFILE = 3

    def __init__(self, **kwargs):
        super(PageManager, self).__init__(**kwargs)
        self.size = (360, 640)
        self.currentPage = 2
        self.pages = [SignInPage(), ParentHomePage(), TutorHomePage(), ParentProfile(), TutorProfile()]

        with self.canvas:
            self.bgCanvas = Rectangle(pos=(0, 0), size=(self.width, self.height))#70))

        self.add_widget(self.pages[self.currentPage])

        self.homeButton = ChangePageButton(PageManager.HOME, (10, 15), (50, 50), "images/homeButton.png")
        self.add_widget(self.homeButton)

        self.profileButton = ChangePageButton(PageManager.PROFILE, (self.width - 60, 15), (50, 50), "images/profileButton.png")
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