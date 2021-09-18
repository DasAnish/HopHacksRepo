from backend import Backend
from kivy.app import App
from kivy.base import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.image import Image

Builder.load_file("kivyFiles/main.kv")

class ChangePageButton(Button):
    def __init__(self, page, pos, size, color, text, **kwargs):
        super(ChangePageButton, self).__init__(**kwargs)
        self.page = page
        self.pos = pos
        self.size = size
        self.background_color = color
        self.text = text
        self.bind(on_press=self.pressed)
    def pressed(self, instance):
        app = App.get_running_app()
        PM = app.root
        PM.goToPage(self.page)

class SignInPage(Widget):
    def __init__(self, **kwargs):
        super(SignInPage, self).__init__(**kwargs)

class ParentHomePage(Widget):
    def __init__(self, **kwargs):
        super(ParentHomePage, self).__init__(**kwargs)
        self.add_widget(Image(source="images/kelvin1.png", allow_stretch=True, pos=(10, 70),
                              size=(Window.width-20, Window.height - 80)))

class TutorHomePage(Widget):
    def __init__(self, **kwargs):
        super(TutorHomePage, self).__init__(**kwargs)

class ParentProfile(Widget):
    def __init__(self, **kwargs):
        super(ParentProfile, self).__init__(**kwargs)
        self.add_widget(Image(source="images/kelvin2.png", allow_stretch=True, pos=(10, 70),
                              size=(Window.width - 20, Window.height - 80)))

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
        self.currentPage = 1
        self.pages = [SignInPage(), ParentHomePage(), TutorHomePage(), ParentProfile(), TutorProfile()]
        self.add_widget(self.pages[self.currentPage])

        self.homeButton = ChangePageButton(PageManager.HOME, (10, 10), (50, 50), (1, 0, 0, 1), "HOME")
        self.add_widget(self.homeButton)

        self.profileButton = ChangePageButton(PageManager.PROFILE, (self.width - 60, 10), (50, 50), (1, 0, 1, 1), "PROFILE")
        self.add_widget(self.profileButton)

    def goToPage(self, page):
        self.remove_widget(self.pages[self.currentPage])
        self.currentPage = page
        self.add_widget(self.pages[self.currentPage])

class MainApp(App):
    def build(self):
        return PageManager()


Window.size = (360, 640)
MainApp().run()