from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from MenuButton import MenuButton
from kivy.app import App
import MarsPathfinder_setup

from  Uran import Uran
from Storage import Storage
import math


class UranMiner(Button):
    def __init__(self):
        super(UranMiner, self).__init__()
        self.root = ""
        self.speed = 1
        self.matrixObjectSize = 1
        self.matrixPosition = []
        self.moveEndPosition = []
        self.size_hint = (None,None)
        self.size = (60,60)

        self.moveX = 0
        self.moveY = 0

        self.motherRafinery = []
        self.wait = 0
        self.buildCost = 0
        self.side = "Friend"
        self.health = 100
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

    def on_release(self):
        print(self.matrixPosition,self.pos,self.root.gameMapMatrix[self.matrixPosition[0]][self.matrixPosition[1]],"Uran miner")

    def mineUran(self):
        if self.closestUranSpot == []:
            print("Szukam uranu")
            if self.working == False:
                uranSpots = []
                for object in self.root.children:
                    if isinstance(object,Uran):
                        uranSpots.append(object)
                if uranSpots and len(uranSpots) > 1:
                    closestUran = uranSpots.pop(0)
                    for uran in uranSpots:
                        if math.dist(self.matrixPosition,closestUran.matrixPosition) > math.dist(self.matrixPosition,uran.matrixPosition):
                            closestUran = uran
                    print(closestUran.matrixPosition,"Closest uran")
                    self.closestUranSpot = closestUran
                    self.go_to_uran()
                    return closestUran
                else:
                    closestUran = uranSpots[0]
                    self.closestUranSpot = closestUran
                    self.go_to_uran()
                    print(self.closestUranSpot)
                    return

            else:
                return
        elif self.matrixPosition == self.closestUranSpot.matrixPosition:
            self.mine_uran()

        elif self.matrixPosition == self.motherRafinery:
            self.deliver_uran_to_rafinery()

    def go_to_uran(self):
        if self.closestUranSpot != []:
            if self.working == False:
                self.root.orders_destinations.append([self, self.closestUranSpot.matrixPosition, "Move", self.closestUranSpot])



    def mine_uran(self):
        print("Mine uran")
        print(self.wait)
        print(self.closestUranSpot)
        self.wait += 1
        if self.wait == 500:
            self.wait = 0
            self.root.remove_widget(self.closestUranSpot)
            self.root.orders_destinations.append([self, self.motherRafinery, "Move",self.motherRafinery])


    def deliver_uran_to_rafinery(self):
        print("Deliver to rafinery")
        self.wait += 1
        if self.wait == 500:
            self.wait = 0
            self.closestUranSpot = []
