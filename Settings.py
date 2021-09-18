from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.settings import SettingsWithNoMenu
import json

settings_json = json.dumps([
    {'type': 'string',
     'title': 'First Name',
     'desc': 'Boolean description text',
     'section': 'example',
     'key': 'first'},
    {'type': 'string',
     'title': 'Last Name',
     'desc': 'Numeric description text',
     'section': 'example',
     'key': 'last'},
    {'type': 'options',
     'title': 'An options setting',
     'desc': 'Options description text',
     'section': 'example',
     'key': 'optionsexample',
     'options': ['option1', 'option2', 'option3']},
    {'type': 'string',
     'title': 'A string setting',
     'desc': 'String description text',
     'section': 'example',
     'key': 'stringexample'},
    {'type': 'path',
     'title': 'A path setting',
     'desc': 'Path description text',
     'section': 'example',
     'key': 'pathexample'}])


# Builder.load_string('''
# <Interface>:
#     orientation: 'vertical'
#     app.open_settings()
# ''')
#
# class Interface(BoxLayout):
#     pass

class SettingsApp(App):
    def on_start(self):
        self.open_settings()
        
    def build(self):
        self.settings_cls = SettingsWithNoMenu
        self.use_kivy_settings = False
        return

    def build_config(self, config):
        config.setdefaults('settings', {
            'first': 'Kelvin',
            'last': 'Leung',
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': '/some/path'})

    def build_settings(self, settings):
        settings.add_json_panel('Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print(config, section, key, value)


if __name__ == '__main__':
    SettingsApp().run()
