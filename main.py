#-*- coding: utf8 -*-

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')

class TextWidget(Widget):
    text = StringProperty()
    color = ListProperty([1,1,1,1])

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = 'iQuant3D'

    def buttonClicked1(self):
        self.text = 'Peak-Detection'
        self.color = [1,0,0,1]

    def buttonClicked2(self):
        self.text = 'Sectioning'
        self.color = [0,1,0,1]

    def buttonClicked3(self):
        self.text = 'Analysis'
        self.color = [0,0,1,1]

class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title='greeting'

    def build(self):
        return TextWidget()

if __name__=='__main__':
    TestApp().run()
