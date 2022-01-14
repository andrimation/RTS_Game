from kivy.uix.button import Button
from kivy.properties import BooleanProperty, StringProperty

from Storage import Storage

class MenuButton(Button):
    selected = BooleanProperty(False)

    def on_release(self):
        self.selected = not self.selected
        Storage.MenuButtonSelected = self.selected
        print("on release")

