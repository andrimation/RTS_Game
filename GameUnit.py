from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label

import MarsPathfinder_setup
import math
import random
import copy

from Storage import Storage

class GameUnit(Button):
    selected = BooleanProperty(False)
    def __init__(self,root,unitType,side,player,combatTeam):
        super(GameUnit, self).__init__()
        self.root = root
        self.player = player
        self.speed = 2
        self.matrixObjectSize = 1
        self.matrixPosition = []
        self.moveType =    None
        self.matrixPath      = []
        self.moveEndPosition = []
        self.unitType = unitType
        self.minimapUnit = None
        self.minimapName = None
        self.selected = False
        self.combatTeam = combatTeam
        self.auto_attack_distance = 5



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
            return Tank(self.root,self.unitType,self.side,self.player,self.combatTeam)
        elif self.unitType == "RocketLauncher":
            return RocketLauncher(self.root,self.unitType,self.side,self.player,self.combatTeam)


    def build_unit_in_factory(self):
        # Dodać sprawdzenie czy dany gracz ma war factory !! że np jak je zniszczymy to żeby komp dalej nie produkował
        if self.player.WarFactory != None and self.player.power > 0:
            currentWarFactory = self.player.WarFactory
            self.root.updateGameMatrix()
            origin = currentWarFactory.matrixPosition[0]
            self.matrixPosition = MarsPathfinder_setup.find_Closesd_Free_NoRandom(self.root.numpyMapMatrix,origin)
            posX = self.root.gameMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]][0]+self.root.positionX
            posY = self.root.gameMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]][1]+self.root.positionY
            self.player.money -= self.buildCost
            self.pos = (posX,posY)
            self.add_on_minimap()
            self.root.update_money()
            self.root.movableObjects.append(self)
            self.root.numpyMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]] = 1
            self.root.obj_add_index += 1
            self.root.add_widget(self,index=self.root.ids["SidePanelWidget"].index+1)
            self.player.units.append(self)

            self.root.onMapObjectsToShift.append(self)
            self.root.ids["SidePanelWidget"].index = 0
        else:
            self.player.buildUnitsQueue = []

    def on_release(self):
        if self.player == self.root.humanPlayer:
            self.selected = not self.selected
            for unit in self.root.movableObjects:
                if unit.combatTeam == self.combatTeam and unit.side == self.side:
                    unit.selected = self.selected
        else:
            self.root.click_on_map("Attack",self)

    def add_unit_to_build_queue(self):
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
        self.root.miniMapUnits[self.minimapName] = self.minimapUnit
        self.minimapUnit.size_hint = (None,None)
        self.minimapUnit.size = (2,2)
        self.minimapUnit.pos = (zeroX + posX, zeroY + posY)
        self.root.minimapObject.add_widget(self.minimapUnit)
        self.root.ids["SidePanelWidget"].index = 0

    def updade_minimapPos(self):
        try:
            miniobjectToUpdate =  self.root.miniMapUnits[self.minimapName]
            zeroX,zeroY,posX,posY = self.compute_minimapXY()
            self.minimapUnit.pos = (zeroX + posX, zeroY + posY)
            self.root.miniMapUnits[str(self) + "Mini"] = miniobjectToUpdate
            self.root.ids["SidePanelWidget"].index = 0
        except:
            pass

    # Z jakiegoś powodu, gdy zostaje zniszczonych kilka jednostek, minimapa przestaje sie dla innych updejtować ;0
    def remove_object(self):

        for unit in self.root.movableObjects:
            if unit.target == self:
                unit.target = []
                unit.attack = False

        try:
            self.player.units.remove(self)
        except:
            pass
        try:
            self.root.remove_widget(self)
        except:
            pass
        try:
            self.root.movableObjects.remove(self)
        except:
            pass
        try:
            self.root.onMapObjectsToShift.remove(self)
        except:
            pass
        try:
            self.root.minimapObject.remove_widget(self.minimapUnit)
            self.root.miniMapUnits.remove(self.minimapName)
            self.minimapName = None
            self.minimapUnit = None
        except:
            pass

    def find_attack_target(self):
        if self.combatTeam in [4,3,2]:
            if self.root.humanPlayer.units:
                target = random.choice(self.root.humanPlayer.units)
                return target
            elif self.root.humanPlayer.buildings:
                target = random.choice(self.root.humanPlayer.buildings)
                return target
        else:
            if self.root.humanPlayer.buildings:
                target = random.choice(self.root.humanPlayer.buildings)
                return target
            elif self.root.humanPlayer.units:
                target = random.choice(self.root.humanPlayer.units)
                return target

    def attack_human(self):
        if self.movingToTarget == False:
            self.movingToTarget = True

            for unit in self.root.humanPlayer.units:
                self.root.updateGameMatrix()
                if unit.matrixPosition != []:
                    self.root.orders_destinations.append([self,unit.matrixPosition,"Attack",unit,list(unit.matrixPosition.copy())])

    def auto_attack(self):

        for destination in self.root.orders_destinations:
            if destination[0] == self:
                return
        for order in self.root.move_queue:
            if order[0] == self:
                return

        if isinstance(self,Tank) or isinstance(self,RocketLauncher):
            if self.target == [] and self.attack == False:
                self.root.movableObjects.sort(key=lambda x: math.dist(x.matrixPosition, self.matrixPosition))
                for unit in self.root.movableObjects:
                    if self.player == self.root.computerPlayer:
                        self.auto_attack_distance = 200
                    if unit.player != self.player and math.dist(self.matrixPosition,unit.matrixPosition) <= self.auto_attack_distance:
                        auto_attack = [self, unit.matrixPosition, "Attack", unit,list(unit.matrixPosition.copy())]
                        self.root.orders_destinations.append(auto_attack)
                        # Add attack order to all units in combat team
                        for subUnit in self.root.movableObjects:
                            if self.side == subUnit.side and self.combatTeam == subUnit.combatTeam and self != subUnit:
                                            auto_attack = [subUnit, unit.matrixPosition, "Attack", unit, list(unit.matrixPosition.copy())]
                                            self.root.orders_destinations.append(auto_attack)
                        return
        else:
            return


class Tank(GameUnit):
    def __init__(self,root,unitType,side,player,combatTeam):
        super(Tank,self).__init__(root,unitType,side,player,combatTeam)

        self.buildCost = 650
        self.buildTime = 10
        self.speed = 2
        self.auto_attack_distance = 5

        self.size_hint = (None,None)
        self.size = (60,60)

class RocketLauncher(GameUnit):
    def __init__(self,root,unitType,side,player,combatTeam):
        super(RocketLauncher, self).__init__(root,unitType,side,player,combatTeam)

        self.shotDistance = 12
        self.buildCost = 2500
        self.buildTime = 5
        self.speed = 6
        self.auto_attack_distance = 12

        self.size_hint = (None, None)
        self.size = (60, 60)

class Bullet(GameUnit):
    def __init__(self):
        super(GameUnit, self).__init__()

        self.root = ""
        self.selected = BooleanProperty(False)
        self.speed = 1000
        self.matrixPosition = []
        self.go = False

        self.targetMatrix = 0
        self.absoluteBulletStartX = 0

        self.absoluteTargetX = 0
        self.absoluteTargetY = 0


        self.moveX = 0
        self.moveY = 0

        self.distanceToFly = 10

        self.shotPower = 10
        self.reloadTime = 30
        self.reloadCounter = 0
        self.startPos = []
        self.target = []
        self.source = []


    # def on_release(self):
    #     if self.side == "Friend":
    #         if Storage.MenuButtonSelected == False:
    #             self.selected = not self.selected
    #             print(self.id,self.selected)
    #
    #     else:
    #         self.root.click_on_map("Attack",self)





