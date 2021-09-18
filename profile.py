from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

Builder.load_file('profile.kv')

class P(FloatLayout):
    pass

def popFun():
    show = P()
    window = Popup(title="Save", content=show,
                   size_hint=(None, None), size=(300, 150))
    window.open()

class ProfilePicture(Button):
    def selected(self, filename):
        try:
            self.ids.pic.background_normal = filename[0]
        except:
            pass
        return

    def pop(self):
        popFun()

class Bullshit(App):
    def build(self):
        return ProfilePicture()

Bullshit().run()