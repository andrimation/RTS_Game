from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton
from kivy.core.window import Window
from kivy.app import App

import MarsPathfinder_setup
import math

from Storage import Storage

class GameUnit(Button):
    selected = BooleanProperty(False)
    def __init__(self,root,unitType,side,player):
        super(GameUnit, self).__init__()
        self.root = root
        self.player = player
        self.speed = 10
        self.matrixObjectSize = 1
        self.matrixPosition = []
        self.moveEndPosition = []
        self.unitType = unitType
        self.minimapUnit = None

        self.moveX = 0
        self.moveY = 0

        self.wait = 0

        self.buildCost = 0
        self.side = side
        self.health = 100
        self.shotDistance = 5
        self.firePower = 10
        self.reloadTime = 30
        self.reloadCounter = 0
        self.attack = False
        self.startPos = []
        self.target = []


    def create_unit(self):
        if self.unitType == "Tank":
            return Tank(self.root,self.unitType,self.side,self.player)
        elif self.unitType == "RocketLauncher":
            return RocketLauncher(self.root,self.unitType,self.side,self.player)

    def on_release(self):
        if self.side == "Friend":
            self.selected = not self.selected
        else:
            self.root.click_on_map("Attack",self)
            self.selected = not self.selected

    def build_unit_in_factory(self):
        for building in self.root.buildings:
            if building.buildingType == "WarFactory" and building.side == self.side:
                self.root.updateGameMatrix()
                origin = building.matrixPosition[0]
                self.matrixPosition = MarsPathfinder_setup.find_Closesd_Free_NoRandom(self.root.numpyMapMatrix,origin)
                posX = self.root.gameMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]][0]+self.root.positionX
                posY = self.root.gameMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]][1]+self.root.positionY
                self.pos = (posX,posY)
                self.add_on_minimap()
                self.root.humanPlayer.money -= self.buildCost
                self.root.movableObjects.append(self)
                self.root.gameMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]][2] = True
                self.root.add_widget(self, self.root.obj_add_index)
                self.root.onMapObjectsToShift.append(self)
                self.root.obj_add_index += 1
                self.root.ids["SidePanelWidget"].index = 0

    def add_unit_to_build_queue(self):
        if self.player.money >= self.buildCost:
            self.player.buildUnitsQueue.append(self)

    def compute_minimapXY(self):
        imageX, imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size
        zeroX, zeroY = ((Window.size[0] * 0.1) * 0.025, self.root.ids["SidePanelWidget"].height * 0.83)
        posX = int((self.matrixPosition[1] * ((Window.size[0] * 0.1) * 0.95)) / len(self.root.gameMapMatrix[0]))
        posY = math.ceil((abs((self.matrixPosition[0] - (len(self.root.gameMapMatrix)))) * ( imageY * (Window.size[0] * 0.1)) / imageX) / len(self.root.gameMapMatrix[0]))
        return zeroX,zeroY,posX,posY

    def add_on_minimap(self):
        self.minimapUnit = Image()
        zeroX,zeroY,posX,posY = self.compute_minimapXY()
        self.root.miniMapUnits[str(self)+"Mini"] = self.minimapUnit
        self.minimapUnit.size_hint = (None,None)
        self.minimapUnit.size = (2,2)
        self.minimapUnit.pos = (zeroX + posX, zeroY + posY)
        self.root.minimapObject.add_widget(self.minimapUnit)
        self.root.ids["SidePanelWidget"].index = 0

    def updade_minimapPos(self):
        miniobjectToUpdate =  self.root.miniMapUnits[str(self)+"Mini"]
        zeroX,zeroY,posX,posY = self.compute_minimapXY()
        self.minimapUnit.pos = (zeroX + posX, zeroY + posY)
        self.root.miniMapUnits[str(self) + "Mini"] = miniobjectToUpdate
        self.root.ids["SidePanelWidget"].index = 0


class Tank(GameUnit):
    def __init__(self,root,unitType,side,player):
        super(Tank,self).__init__(root,unitType,side,player)

        self.buildCost = 250
        self.buildTime = 100
        self.speed = 1

        self.size_hint = (None,None)
        self.size = (60,60)



class RocketLauncher(GameUnit):
    def __init__(self,root,unitType,side,player):
        super(RocketLauncher, self).__init__(root,unitType,side,player)

        self.buildCost = 2500
        self.buildTime = 300
        self.speed = 1

        self.size_hint = (None, None)
        self.size = (60, 60)







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





