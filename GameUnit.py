from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.graphics import Rectangle


import MarsPathfinder_setup
import math
import random
import copy
import os
from Storage import Storage

class GameUnit(Button):
    selected = BooleanProperty(False)
    def __init__(self,root,unitType,side,player,combatTeam):
        super(Button,self).__init__()
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

        self.angle_ = 0
        self.angle_to_rotate = 0
        self.rotate_finish = False
        self.source_rectangle = None
        self.find_source_rectangle()
        self.set_unit_image()

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


    def find_source_rectangle(self):
        for element in self.canvas.before.children:
            if isinstance(element,Rectangle):
                self.source_rectangle = element

    def set_unit_image(self):
        if self.player == self.root.humanPlayer:
            if self.unitType == "Tank":
                dictionary = self.root.tank_friend_animation
            elif self.unitType == "RocketLauncher":
                dictionary = self.root.rocketLauncher_friend_animation
            elif self.unitType == "UranMiner":
                dictionary = self.root.uran_miner_friend
        else:
            if self.unitType == "Tank":
                dictionary = self.root.tank_enemy_animation
            elif self.unitType == "RocketLauncher":
                dictionary = self.root.rocketLauncher_enemy_animation
            elif self.unitType == "UranMiner":
                dictionary = self.root.uran_miner_enemy

        if self.angle_ >= 0:
            self.source_rectangle.texture = dictionary[str(self.angle_)]
        else:
            self.source_rectangle.texture = dictionary[str(360 + self.angle_)]

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
            origin = currentWarFactory.matrixPosition
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

    def remove_object(self):

        self.reset_attack()

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

        for order in self.root.orders_destinations:
            if order[0] == self:
                try:
                    self.root.orders_destinations.remove(order)
                except:
                    pass
            elif order[3] == self:
                try:
                    self.root.orders_destinations.remove(order)
                except:
                    pass

        for order in self.root.move_queue:
            if order[0] == self:
                try:
                    self.root.move_queue.remove(order)
                except:
                    pass
            elif order[4] == self:
                try:
                    order[0].reset_attack()
                    self.root.move_queue.remove(order)
                except:
                    pass


    def reset_attack(self):
        self.attack = False
        self.target = []

    def auto_attack(self):
        if isinstance(self, Tank) or isinstance(self, RocketLauncher) and self.target == [] and self.attack == False:
            for destination in self.root.orders_destinations:
                if destination[0] == self:
                    return
            for order in self.root.move_queue:
                if order[0] == self:
                    return
    # Rozkminić jak atakować budynki ?!!?!?!
    # W pewnym momencie komp przestaje grać ??
            targets = self.root.movableObjects + self.root.buildings
            targets.sort(key=lambda x: math.dist(x.matrixPosition, self.matrixPosition))  # Tu sortować tylko human playera units zamiast wszystko
            for unit in targets:
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



class Tank(GameUnit):
    def __init__(self,root,unitType,side,player,combatTeam):
        super(Tank,self).__init__(root,unitType,side,player,combatTeam)

        self.health = 350
        self.buildCost = 650
        self.buildTime = 10
        self.speed = 4
        self.auto_attack_distance = 5

        self.size_hint = (None,None)
        self.size = (60,60)

class RocketLauncher(GameUnit):
    def __init__(self,root,unitType,side,player,combatTeam):
        super(RocketLauncher, self).__init__(root,unitType,side,player,combatTeam)

        self.shotDistance = 12
        self.health = 150
        self.buildCost = 2500
        self.buildTime = 5
        self.speed = 2
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


class StartButton(Button):
    def __init__(self,root):
        super(Button, self).__init__()
        self.id = "StartButton"
        self.root = root
        self.pos_hint = {"x":0.1,"y":0}
        self.size_hint = (0.9,1)

    def on_release(self):
        self.root.remove_widget(self)
        self.root.start()






