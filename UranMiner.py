from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton
from kivy.app import App
import MarsPathfinder_setup

from Storage import Storage
from  GameUnit import GameUnit
import math


class UranMiner(GameUnit):
    selected = BooleanProperty(False)
    def __init__(self,root,unitType,side,player,combatTeam):
        super(UranMiner, self).__init__(root,unitType,side,player,combatTeam)
        self.root = root
        self.speed = 2
        self.matrixObjectSize = 1
        self.matrixPosition = []
        self.moveEndPosition = []
        self.size_hint = (None,None)
        self.size = (60,60)

        self.moveX = 0
        self.moveY = 0

        self.autoMode = True
        self.motherRafinery = []
        self.wait = 0
        self.buildCost = 0
        self.side = "Friend"
        self.health = 350
        self.shotDistance = 5
        self.firePower = 10
        self.reloadTime = 30
        self.reloadCounter = 0
        self.attack = False
        self.startPos = []
        self.target = []
        self.uranLoad = 0
        self.working = False

        self.closestUranSpot = []
        self.uranSpots = []
        self.closestUran = None
        self.type = "uranminer"

    def mineUran(self):
        if self.closestUranSpot == []:
            if self.working == False:
                self.uranSpots = []
                for object in self.root.urans:
                    self.uranSpots.append(object)
                if self.uranSpots and len(self.uranSpots) > 1:
                    self.closestUran = self.uranSpots.pop(0)
                    for uran in self.uranSpots:
                        if math.dist(self.matrixPosition,self.closestUran.matrixPosition) > math.dist(self.matrixPosition,uran.matrixPosition) and self.root.gameMapMatrix[uran.matrixPosition[0]][uran.matrixPosition[1]][-1] != "uranMiner":
                            self.closestUran = uran
                    self.closestUranSpot = self.closestUran
                    self.root.gameMapMatrix[self.closestUran.matrixPosition[0]][self.closestUran.matrixPosition[1]].append("uranMiner")
                    self.go_to_uran()
                    return self.closestUran
                else:
                    try:
                        self.closestUran = self.uranSpots[0]
                        self.closestUranSpot = self.closestUran
                        self.go_to_uran()
                    except:
                        pass
                    return

            else:
                return
        elif self.matrixPosition == self.closestUranSpot.matrixPosition:
            self.mine_uran()

        elif self.matrixPosition == self.motherRafinery:
            self.deliver_uran_to_rafinery()
        else:
            for order in self.root.move_queue:
                if order[0] == self and order[2] == None:
                    self.deliver_uran_to_rafinery()

    def go_to_uran(self):
        self.selected = False
        if self.closestUranSpot != []:
            if self.working == False:
                self.root.orders_destinations.append([self, self.closestUranSpot.matrixPosition, "Move", self.closestUranSpot,None])
                # self.root.compute_orders_paths()

    def mine_uran(self):
        self.working = True
        self.wait += 1
        if self.wait == 500:
            self.wait = 0
            self.working = False
            try:
                if self.root.gameMapMatrix[self.closestUranSpot.matrixPosition[0]][self.closestUranSpot.matrixPosition[1]][-1] == "uranMiner":
                    self.root.gameMapMatrix[self.closestUranSpot.matrixPosition[0]][self.closestUranSpot.matrixPosition[1]].pop(-1)
                    self.closestUranSpot.remove_minimap_widget()
                    self.root.urans.remove(self.closestUranSpot)
                    self.root.onMapObjectsToShift.remove(self.closestUranSpot)
                    self.root.remove_widget(self.closestUranSpot)
            except:
                pass
            self.root.orders_destinations.append([self, self.motherRafinery, "Move",self.motherRafinery,None])
            # self.root.compute_orders_paths()

    def deliver_uran_to_rafinery(self):
        self.wait += 1
        self.player.money += 1
        self.player.update_money()
        if self.wait == 500:
            self.wait = 0
            self.closestUranSpot = []
            self.working = False

