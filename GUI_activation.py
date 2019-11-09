#iQuant3D 0.1.11 (Nov.7, 2019)
#Development Code = OTTER
#-*- coding: utf8 -*-

from iquant3d import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
#from kivy.garden.animlabel import AnimLabel
from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')

sm = ScreenManager()

class MainScreenWidget(Widget):
    pass

class ButtonWidget(Widget):
    text = StringProperty()
    message = StringProperty()
    std_element = StringProperty()
    view_element = StringProperty()
    color = ListProperty([1,1,1,1])

    def __init__(self, **kwargs):
        super(ButtonWidget, self).__init__(**kwargs)
        self.text = 'iQuant3D : Software for quantitative multi-element 3D imaging using LA-ICP-MS'
        self.message = 'iQuant3D'
        self.std_element = 'init'
        self.view_element = 'init'

    def loadData(self):
        self.message = 'LoadData'
        self.color = [1,1,1,1]

    def buttonClicked1(self):
        self.message = 'Peak-Detection'
        #self.color = [1,0,0,1]

    def buttonClicked2(self):
        self.message = 'Sectioning'
        #self.color = [0,1,0,1]

    def buttonClicked3(self):
        self.message = 'Analysis'
        #self.color = [0,0,1,1]

    def notAvailable(self):
        self.message = 'Not available now.'

class iQuant3DApp(App):
    def __init__(self, **kwargs):
        super(iQuant3DApp, self).__init__(**kwargs)
        self.title='iQuant3D'

    def build(self):
        #allscn = FrontScn()
        #sm.add_widget(ButtonWidget)
        return ButtonWidget()

class iQuant3D():
    def __init__(self):
        pass

if __name__=='__main__':
    iQuant3DApp().run()
