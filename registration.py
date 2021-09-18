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
    is_tutor = ObjectProperty(None)

    def checkbox_click(self, instance, value):
        if value == True:
            self.is_tutor = True
        else:
            self.is_tutor = False

    def validate(self):

        # validating if the username already exists
        if self.username.text not in users['username'].unique():
            print(self.username.text)
            print(users['username'].unique())
            popFun()
        # elif self.username.text in users['username'].unique() and self.pwd.text != users:
        #     raise Exception('Not Implemented')
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
    is_tutor = ObjectProperty(None)

    def checkbox_click(self, instance, value):
        if value == True:
            self.is_tutor = True
        else:
            self.is_tutor = False

    def signup(self):

        # creating a DataFrame of the info
        user = pd.DataFrame([[self.username.text, self.pwd.text, self.phone.text, self.fname.text, self.lname.text]],
                            columns=['username', 'password', 'phoneNum', 'fname', 'lname'])
        user = user.replace(r'^\s*$', np.NAN, regex=True)
        if user.isnull().sum().sum() == 0:
            if self.username.text not in users['username'].unique():
                # change password to hash
                tempdict = user.to_dict('list')
                for key in tempdict:
                    tempdict[key] = tempdict[key][0]
                tempdict['password'] = passwordHash(tempdict['password']).hex()
                tempdict['is_tutor'] = self.is_tutor is not None
                '''need to complete, verification '''
                print(tempdict)
                sm.current = 'login'
                self.username.text = ""
                self.pwd.text = ""
                self.phone.text = ""
                self.fname.text = ""
                self.lname.text = ""
        else:
            # if values are empty or invalid show pop up
            popFun()


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
