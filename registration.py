import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy.core.window import Window
import hashlib
from kivy.uix.checkbox import CheckBox
from backend import Backend



# class to build GUI for a popup window
class P(FloatLayout):
    pass

class P1(FloatLayout):
    pass

class P2(FloatLayout):
    pass

def popFun(message):
    show = message()
    window = Popup(title="Warning", content=show,
                   size_hint=(None, None), size=(300, 150))
    window.open()


# hash password
def passwordHash(password):
    pw = password
    key = hashlib.pbkdf2_hmac('sha256',  # The hash digest algorithm for HMAC
        pw.encode(),  # Convert the password to bytes
        iterations=100000,
        salt=b'0',
        dklen=128)
    return key


class ChooseWindow(Screen):
    pass


# class to accept user info and validate it
class LoginWindow(Screen):
    username = ObjectProperty(None)
    pwd = ObjectProperty(None)
    isTutor = ObjectProperty(None)

    def checkbox_click(self, instance, value):
        if value == True:
            self.isTutor = True
        else:
            self.isTutor = False

    def validate(self):
        # validating if the username already exists
        tempdict = {"username": self.username.text, "password": self.pwd.text, "isTutor": self.isTutor is not None}
        if not Backend.signInVerification(tempdict):
            popFun(P2)
        else:
            # switching the current screen to display validation result
            sm.current = 'logdata'
            # reset TextInput widget
            self.username.text = ""
            self.pwd.text = ""

# class to accept sign up info
class SignupWindow(Screen):
    username = ObjectProperty(None)
    pwd = ObjectProperty(None)
    phone = ObjectProperty(None)
    fname = ObjectProperty(None)
    lname = ObjectProperty(None)
    isTutor = ObjectProperty(None)

    def checkbox_click(self, instance, value):
        if value == True:
            self.isTutor = True
        else:
            self.isTutor = False

    def signup(self):

        # creating a DataFrame of the info
        user = pd.DataFrame([[self.username.text, self.pwd.text, self.phone.text, self.fname.text, self.lname.text]],
                            columns=['username', 'password', 'phoneNum', 'fname', 'lname'])
        user = user.replace(r'^\s*$', np.NAN, regex=True)
        if user.isnull().sum().sum() == 0:
            # change password to hash
            tempdict = user.to_dict('list')
            for key in tempdict:
                tempdict[key] = tempdict[key][0]
            tempdict['password'] = passwordHash(tempdict['password']).hex()
            tempdict['isTutor'] = self.isTutor is not None
            if Backend.signUpVerification(tempdict):
                sm.current = 'login'
                self.username.text = ""
                self.pwd.text = ""
                self.phone.text = ""
                self.fname.text = ""
                self.lname.text = ""
            else:
                popFun(P1)
        else:
            # if values are empty or invalid show pop up
            popFun(P)

    def clearup(self):
        sm.current = 'login'
        self.username.text = ""
        self.pwd.text = ""
        self.phone.text = ""
        self.fname.text = ""
        self.lname.text = ""



# class to display validation result
class LogDataWindow(Screen):
    pass


# class for managing screens
class WindowManager(ScreenManager):
    pass


Window.clearcolor = (0.95, 0.95, 0.95, 1)
# kv file
kv = Builder.load_file('registration.kv')
sm = WindowManager()

# reading all the data stored
users = pd.read_csv('login.csv')

# adding screens
sm.add_widget(LoginWindow(name='login'))
sm.add_widget(SignupWindow(name='signup'))
sm.add_widget(LogDataWindow(name='logdata'))


# class that builds gui
class LoginMain(App):
    def build(self):
        return sm


# driver function
if __name__ == "__main__":
    LoginMain().run()
