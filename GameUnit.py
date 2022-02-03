from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton
from kivy.app import App



from Storage import Storage

class GameUnit(Button):
    selected = BooleanProperty(False)
    def __init__(self):
        super(GameUnit, self).__init__()
        self.root = ""
        self.speed = 1
        self.matrixObjectSize = 1
        self.matrixPosition = []
        self.moveEndPosition = []


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
        if self.side == "Friend":
            print(self.pos)
            if Storage.MenuButtonSelected == False:
                self.selected = not self.selected
                print(self.id,self.selected)

        else:
            self.root.click_on_map("Attack",self)
            if Storage.MenuButtonSelected == False:
                self.selected = not self.selected
            print(Storage.enemyToAttack)













class Bullet(Button):

    root = ""
    selected = BooleanProperty(False)
    speed = 400
    matrixPosition = []
    go = False

    moveX = 0
    moveY = 0

    distanceToFly = 10

    shotPower = 10
    reloadTime = 30
    reloadCounter = 0
    startPos = []
    target = []
    source = []


    def on_release(self):
        if self.side == "Friend":
            if Storage.MenuButtonSelected == False:
                self.selected = not self.selected
                print(self.id,self.selected)

        else:
            self.root.click_on_map("Attack",self)



rafineryHP = 700
powerPlantHP = 500
warFactoryHP = 700



