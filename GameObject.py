from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton

from Storage import Storage

class GameObject(Button):
    selected = BooleanProperty(False)
    speed = 1

    def on_release(self):
        if Storage.MenuButtonSelected == False:
            self.selected = not self.selected
            print(self.id,self.selected)
        else:
            print("MenuButtonSelected == True -> cant select object on map, just add.")
            pass
