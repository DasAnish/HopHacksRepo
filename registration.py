import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
import numpy as np
from kivy.core.window import Window


# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()


# class to build GUI for a popup window
class P(FloatLayout):
    pass


# function that displays the content
def popFun():
    show = P()
    window = Popup(title="Warning", content=show,
                   size_hint=(None, None), size=(300, 150))
    window.open()


# class to accept user info and validate it
class loginWindow(Screen):
    username = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):

        # validating if the username already exists
        if self.username.text not in users['Username'].unique():
            popFun()
        else:

            # switching the current screen to display validation result
            sm.current = 'logdata'

            # reset TextInput widget
            self.username.text = ""
            self.pwd.text = ""

# class to accept sign up info
class signupWindow(Screen):
    username = ObjectProperty(None)
    pwd = ObjectProperty(None)
    phone = ObjectProperty(None)
    fname = ObjectProperty(None)
    lname = ObjectProperty(None)

    def signup(self):

        # creating a DataFrame of the info
        user = pd.DataFrame([[self.username.text, self.pwd.text, self.phone.text, self.fname.text, self.lname.text]],
                            columns=['Username', 'Password', 'Phone', 'FirstName', 'LastName'])
        user = user.replace(r'^\s*$', np.NAN, regex=True)
        if user.isnull().sum().sum() == 0:
            if self.username.text not in users['Username'].unique():
                # if username does not exist already then append to the csv file
                # change current screen to log in the user now
                user.to_csv('login.csv', mode='a', header=False, index=False)
                sm.current = 'login'
                self.username.text = ""
                self.pwd.text = ""
        else:
            # if values are empty or invalid show pop up
            popFun()


# class to display validation result
class logDataWindow(Screen):
    pass


# class for managing screens
class windowManager(ScreenManager):
    pass


Window.clearcolor = (0.95, 0.95, 0.95, 1)
# kv file
kv = Builder.load_file('registration.kv')
sm = windowManager()

# reading all the data stored
users = pd.read_csv('login.csv')

# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))


# class that builds gui
class loginMain(App):
    def build(self):
        return sm


# driver function
if __name__ == "__main__":
    loginMain().run()
