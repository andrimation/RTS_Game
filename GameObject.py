from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton

from Storage import Storage

class GameObject(Button):
    selected = BooleanProperty(False)
    speed = 1
    matrixPosition = []

    moveX = 0
    moveY = 0
    matrixDestination = []
    matrixPath = []


    side = "Friend"
    attack = "no"

    def on_release(self):
        if self.side == "Friend":
            if Storage.MenuButtonSelected == False:
                self.selected = not self.selected
                print(self.id,self.selected)

        else:
            Storage.enemyToAttack = self.matrixPosition
            # print(Storage.enemyToAttack)

