from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.core.window import Window

import  math
from MenuButton import MenuButton
from kivy.app import App
from UranMiner import UranMiner

from MarsPathfinder_setup import find_Closesd_Free
from Storage import Storage

# Zrobić dla klasy budynków jak dla klasy pojazdów- że klasa building ma funkcję zwracającą obiekty pod-klasy - rafinery itp itd
class Building(Button):
    def __init__(self,side,player,originMatrix=[]):
        super(Building,self).__init__()
        self.buildingType = ""
        self.buildMode = False
        self.HP = 0
        self.originMatrix = originMatrix
        self.matrixPosition = []
        self.addCounter = 0
        self.wait = 0
        self.minimapUnit = None
        self.minimapName = None

        self.root = ""
        self.selected = BooleanProperty(False)
        self.player = player

        self.buildAndEnergyCosts = {"MainBase":(500,0),"Rafinery":(3000,-500),"PowerPlant":(1000,1500),"WarFactory":(1500,-500),"DefenceTower":(500,-250)}
        self.side = side
        self.health = 100
        self.shotDistance = 5
        self.firePower = 10
        self.reloadTime = 30
        self.reloadCounter = 0
        self.attack = False
        self.startPos = []
        self.target = []
        self.active = True

    def on_release(self):
        self.root.ids["MenuButton_BuildMainBase"].disabled = True
        self.root.ids["MenuButton_BuildRafinery"].disabled = False
        self.root.ids["MenuButton_BuildPowerPlant"].disabled = False
        self.root.ids["MenuButton_BuildWarFactory"].disabled = False
        self.root.ids["MenuButton_BuildDefenceTower"].disabled = False
        if Storage.MenuButtonSelected == False:
            self.selected = not self.selected

        if self.buildMode == True:
            self.addCounter += 1


# Zmniejszyć budynki skoro czołgi nie mogą za nie wjezdzac
    def add_to_game(self,root,type):
        self.root = root
        if self.root.humanPlayer.money > self.buildAndEnergyCosts[type][0]:
            if type == "MainBase":
                self.buildingType = "MainBase"
                self.size_hint = None, None
                self.size = (240,360)
                self.matrixSize = [6,4]
                self.buildMode = True
                self.HP = 1500
                self.root.add_widget(self,index=self.root.building_add_index)
                self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0

            elif type == "Rafinery":
                self.buildingType = "Rafinery"
                self.size_hint = None, None
                self.size = (180, 240)
                self.matrixSize = [4, 3]
                self.buildMode = True
                self.HP = 800
                self.root.add_widget(self,canvas="before",index=self.root.building_add_index)
                self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0

            elif type == "PowerPlant":
                self.buildingType = "PowerPlant"
                self.size_hint = None, None
                self.size = (180, 180)
                self.matrixSize = [3, 3]
                self.buildMode = True
                self.HP = 800
                self.root.add_widget(self,canvas="before",index=self.root.building_add_index)
                self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0

            elif type == "WarFactory":
                self.buildingType = "WarFactory"
                self.size_hint = None, None
                self.size = (180, 240)
                self.matrixSize = [4, 3]
                self.buildMode = True
                self.HP = 700
                self.root.add_widget(self,canvas="before",index=self.root.building_add_index)
                self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0
                self.root.ids["MenuButton_BuildTank"].disabled = False
                self.root.ids["MenuButton_BuildRocketLauncher"].disabled = False

            elif type == "DefenceTower":
                self.buildingType = "WarFactory"
                self.size_hint = None, None
                self.size = (60, 120)
                self.matrixSize = [2, 1]
                self.buildMode = True
                self.HP = 400
                self.root.add_widget(self, canvas="before", index=self.root.building_add_index)
                self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0
            self.root.humanPlayer.money -= self.buildAndEnergyCosts[type][0]
            self.root.humanPlayer.aviableEnergy += self.buildAndEnergyCosts[type][1]

    def compute_minimapXY(self):
        imageX, imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size
        zeroX, zeroY = ((Window.size[0] * 0.1) * 0.025, self.root.ids["SidePanelWidget"].height * 0.83)
        posX = int((self.originMatrix[1] * ((Window.size[0] * 0.1) * 0.95)) / len(self.root.gameMapMatrix[0]))
        posY = math.ceil((abs((self.originMatrix[0] - (len(self.root.gameMapMatrix)))) * ( imageY * (Window.size[0] * 0.1)) / imageX) / len(self.root.gameMapMatrix[0]))
        sizeX = int((self.size[0] * ((Window.size[0] * 0.1) * 0.95)) / imageX)
        sizeY = math.ceil((abs((self.size[1] * (imageY * (Window.size[0] * 0.1)) / imageX) / imageY)))
        return zeroX,zeroY,posX,posY,sizeX,sizeY

    # Pamiętać aby usuwając budynek usuwać również obiekt minimapy - z widgetów i ze słownika obiektów minimap
    def add_on_minimap(self):
        self.minimapUnit = Image()
        zeroX,zeroY,posX,posY,sizeX,sizeY = self.compute_minimapXY()
        self.minimapName = str(self) + "Mini"
        self.root.miniMapUnits[self.minimapName] = self.minimapUnit
        self.minimapUnit.size_hint = (None,None)
        self.minimapUnit.size = (sizeX,sizeY)
        self.minimapUnit.pos = (zeroX + posX, zeroY + posY)
        self.root.minimapObject.add_widget(self.minimapUnit)
        self.root.ids["SidePanelWidget"].index = 0


    # Rafinery only
    def add_uranMiner(self):
        self.matrixPosition.sort(key= lambda x: x[0])
        freePlace = [self.matrixPosition[0][0]+self.matrixSize[0],self.matrixPosition[0][1]]
        uranMiner = UranMiner(self.root,"UranMiner",self.side,self.player)
        uranMiner.motherRafinery = freePlace
        uranMiner.matrixPosition = freePlace
        uranMiner.root = self.root
        uranMiner.pos = (self.pos[0],self.pos[1]-60)
        uranMiner.add_on_minimap()
        self.root.autoUnits.append(uranMiner)
        self.root.onMapObjectsToShift.append(uranMiner)
        self.root.movableObjects.append(uranMiner)
        self.root.add_widget(uranMiner,canvas="after",index=self.root.obj_add_index)
        self.root.updateGameMatrix()


    def on_press(self):
        print(self.pos,"Building pos")
        print(self.matrixPosition,"Building matrix")
