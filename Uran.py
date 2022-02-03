from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton
from kivy.app import App



from Storage import Storage
import random

class Uran(Button):
    def __init__(self):
        super(Uran, self).__init__()
        self.root = ""
        self.matrixPosition = []
        self.size_hint = (None,None)
        self.size = (60,60)

    moveX = 0
    moveY = 0

    wait = 0

    buildCost = 0
    side = "Friend"
    health = 100
    shotDistance = 5
    firePower = 10
    reloadTime = 30
    reloadCounter = 0
    attack = False
    startPos = []
    target = []

    def on_release(self):
        print(self.matrixPosition,"Uran")
        print(self.root.gameMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]])
        print(self.pos)




