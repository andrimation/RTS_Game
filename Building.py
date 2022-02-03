from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.core.window import Window

from MenuButton import MenuButton
from kivy.app import App
from UranMiner import UranMiner

from MarsPathfinder_setup import find_Closesd_Free
from Storage import Storage


class Building(Button):
    def __init__(self):
        super(Building, self).__init__()
        self.buildingType = ""
        self.buildMode = False
        self.HP = 0
        self.matrixPosition = []
        self.addCounter = 0


        self.root = ""
        self.selected = BooleanProperty(False)

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

    def on_release(self):
        self.root.ids["MenuButton_BuildMainBase"].disabled = True
        self.root.ids["MenuButton_BuildRafinery"].disabled = False
        self.root.ids["MenuButton_BuildPowerPlant"].disabled = False
        self.root.ids["MenuButton_BuildWarFactory"].disabled = False
        if Storage.MenuButtonSelected == False:
            self.selected = not self.selected

        if self.buildMode == True:
            self.addCounter += 1


# Zmniejszyć budynki skoro czołgi nie mogą za nie wjezdzac
    def add_to_game(self,root,type):
        self.root = root
        if type == "MainBase":
            self.buildingType = "MainBase"
            self.size_hint = None, None
            self.size = (240,360)
            self.matrixSize = [6,4]
            self.buildMode = True
            self.HP = 1000
            self.root.add_widget(self,index=self.root.building_add_index)
            self.root.buildingToAdd.append(self)
            self.root.ids["SidePanelWidget"].index = 0
        elif type == "Rafinery":
            self.buildingType = "Rafinery"
            self.size_hint = None, None
            self.size = (180, 240)
            self.matrixSize = [4, 3]
            self.buildMode = True
            self.HP = 700
            self.root.add_widget(self,canvas="before",index=self.root.building_add_index)
            self.root.buildingToAdd.append(self)
            self.root.ids["SidePanelWidget"].index = 0
            # Add uran miner - find closest free space:


        elif type == "PowerPlant":
            self.buildingType = "PowerPlant"
            self.size_hint = None, None
            self.size = (180, 180)
            self.matrixSize = [3, 3]
            self.buildMode = True
            self.HP = 500
            self.root.add_widget(self,canvas="before",index=self.root.building_add_index)
            self.root.buildingToAdd.append(self)
            self.root.ids["SidePanelWidget"].index = 0
        elif type == "WarFactory":
            self.buildingType = "WarFactory"
            self.size_hint = None, None
            self.size = (180, 240)
            self.matrixSize = [4, 3]
            self.buildMode = True
            self.HP = 500
            self.root.add_widget(self,canvas="before",index=self.root.building_add_index)
            self.root.buildingToAdd.append(self)
            self.root.ids["SidePanelWidget"].index = 0

    def add_uranMiner(self):
        # PAthfinder chujowo umieszcza minera -> napisać nowy  -> tu się coś złego dzieje - dodaje mi minery duzo powyżej jeśli przesunę - prawdopodobnie nie shiftuje mi budynku po dodaniu
        # - mogę to rozwiązać tak że rafineria po prostu buduje minera i tyle
        self.matrixPosition.sort(key= lambda x: x[0])
        freePlace = [self.matrixPosition[0][0]+self.matrixSize[0],self.matrixPosition[0][1]]
        print(self.pos)
        uranMiner = UranMiner()
        uranMiner.motherRafinery = freePlace
        uranMiner.matrixPosition = freePlace
        uranMiner.root = self.root
        # uranMiner.pos = (self.root.gameMapMatrix[freePlace[0]][freePlace[1]][0]+Window.size[0]*0.1,self.root.gameMapMatrix[freePlace[0]][freePlace[1]][1])
        uranMiner.pos = (self.pos[0],self.pos[1]-60)
        self.root.add_widget(uranMiner,canvas="after",index=self.root.obj_add_index)
        self.root.updateGameMatrix()

    def on_press(self):
        print(self.matrixPosition)
