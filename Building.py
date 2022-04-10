from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.graphics import Rectangle


import  math
from MenuButton import MenuButton
from kivy.app import App
from UranMiner import UranMiner

from MarsPathfinder_setup import find_Closesd_Free
from Storage import Storage

# Zrobić dla klasy budynków jak dla klasy pojazdów- że klasa building ma funkcję zwracającą obiekty pod-klasy - rafinery itp itd
class Building(Button):
    def __init__(self,root,side,player,type,originMatrix=[],):
        super(Button,self).__init__()
        self.buildingType = type
        self.buildMode = False
        self.HP = 0
        self.matrixPosition = []
        self.originMatrix = originMatrix
        self.fullMatrixPosition = []
        self.addCounter = 0
        self.wait = 0
        self.minimapUnit = None
        self.minimapName = None
        self.moveX = 0
        self.moveY = 0
        self.animation_counter = 0
        self.frames_counter    = 0
        self.animation_source = None
        self.path = ""
        self.win = 0

        self.root = root
        self.selected = BooleanProperty(False)
        self.player = player

        self.buildAndEnergyCosts = {"MainBase":(500,0),"Rafinery":(1500,-500),"PowerPlant":(1000,1500),
                                    "WarFactory":(3250,-500),"DefenceTower":(500,-250)}
        self.side = side
        self.health = 100
        self.shotDistance = 10
        self.firePower = 50
        self.reloadTime = 20
        self.reloadCounter = 0
        self.attack = False
        self.startPos = []
        self.target = []
        self.active = True

        self.size_hint = (None,None)

        self.source_rectangle = self.find_source_rectangle()
        self.set_building_image()

    def find_source_rectangle(self):
        for element in self.canvas.before.children:
            if isinstance(element,Rectangle):
                return element

    def set_building_image(self):
        if self.buildingType == "MainBase":
            if self.player == self.root.humanPlayer:
                self.animation_source = self.root.main_base_friend_animation
            else:
                self.animation_source = self.root.main_base_enemy_animation
        elif self.buildingType == "WarFactory":
            if self.player == self.root.humanPlayer:
                self.animation_source = self.root.war_factory_friend_animation
            else:
                self.animation_source = self.root.war_factory_enemy_animation
        elif self.buildingType == "Rafinery":
            if self.player == self.root.humanPlayer:
                self.animation_source = self.root.rafinery_friend_animation
            else:
                self.animation_source = self.root.rafinery_enemy_animation
        elif self.buildingType == "PowerPlant":
            if self.player == self.root.humanPlayer:
                self.animation_source = self.root.power_plant_friend_animation
            else:
                self.animation_source = self.root.power_plant_enemy_animation
        elif self.buildingType == "DefenceTower":
            if self.player == self.root.humanPlayer:
                self.animation_source = self.root.defence_friend
            else:
                self.animation_source = self.root.defence_enemy


    def animate_building(self):
        try:   # Ten try usunać gdy będą gotowe wszystkie słowniki z obrazkami
            self.animation_counter += 1
            if self.animation_counter == 2:
                self.frames_counter += 1
                self.animation_counter = 0
                if self.frames_counter == 79:
                    self.frames_counter = 0
                self.source_rectangle.texture = self.animation_source[str(self.frames_counter)]
        except:
            pass

    def on_release(self):
        if self.side == "Friend" and self.buildingType == "MainBase":
            self.root.ids["MenuButton_BuildMainBase"].disabled = True
            self.root.ids["MenuButton_BuildRafinery"].disabled = False
            self.root.ids["MenuButton_BuildPowerPlant"].disabled = False
            self.root.ids["MenuButton_BuildWarFactory"].disabled = False
            self.root.ids["MenuButton_BuildDefenceTower"].disabled = False

        if Storage.MenuButtonSelected == False:
            self.selected = not self.selected

        if self.buildMode == True:
            self.addCounter += 1

    def matrixPositionFunc(self):
        return self.matrixPosition[0]

    def add_to_game(self):
        """Set building stats, depending on building type and add building on game map, adds building widget to game map"""
        if self.player.money > self.buildAndEnergyCosts[self.buildingType][0]:
            if self.buildingType == "MainBase":
                self.size = (240,360)
                self.matrixSize = [6,4]
                self.buildMode = True
                self.health = 1500
                if self.side != "Enemy":
                    self.root.add_widget(self, index=self.root.building_add_index)
                    self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0
                self.player.MainBase = self

            elif self.buildingType == "Rafinery":
                self.size = (180, 300)
                self.matrixSize = [5, 3]
                self.buildMode = True
                self.health = 800
                if self.side != "Enemy":
                    self.root.add_widget(self, canvas="before", index=self.root.building_add_index)
                    self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0

            elif self.buildingType == "PowerPlant":
                self.size = (180, 180)
                self.matrixSize = [3, 3]
                self.buildMode = True
                self.health = 800
                if self.side != "Enemy":
                    self.root.add_widget(self, canvas="before", index=self.root.building_add_index)
                    self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0

            elif self.buildingType == "WarFactory":
                if self.player.WarFactory == None:
                    self.size = (180, 300)
                    self.matrixSize = [5, 3]
                    self.buildMode = True
                    self.health = 700
                    if self.side != "Enemy":
                        self.root.add_widget(self, canvas="before", index=self.root.building_add_index)
                        self.root.buildingToAdd.append(self)
                        self.root.ids["SidePanelWidget"].index = 0

                    self.player.WarFactory = self
                else:
                    return self

            elif self.buildingType == "DefenceTower":
                self.buildingType = "DefenceTower"
                self.size = (120, 120)
                self.matrixSize = [2, 2]
                self.buildMode = True
                self.health = 400
                if self.side != "Enemy":
                    self.root.add_widget(self, canvas="before", index=self.root.building_add_index)
                    self.root.buildingToAdd.append(self)
                self.root.ids["SidePanelWidget"].index = 0




            return self

    def low_power(self):
        if self.player.power <= 0:
            self.root.ids["MenuButton_BuildTank"].disabled = True
            self.root.ids["MenuButton_BuildTank"].text = "Low Power"
            self.root.ids["MenuButton_BuildRocketLauncher"].disabled = True
            self.root.ids["MenuButton_BuildRocketLauncher"].text = "Low Power"
        else:
            self.root.ids["MenuButton_BuildTank"].disabled = False
            self.root.ids["MenuButton_BuildTank"].text = "Tank"
            self.root.ids["MenuButton_BuildRocketLauncher"].disabled = False
            self.root.ids["MenuButton_BuildRocketLauncher"].text = "RocketLauncher"

    def move_building_widget_along_cursor(self):
        mouseX = (((Window.mouse_pos[0] - Window.size[0] * 0.1) // 60)) * 60
        mouseY = (Window.mouse_pos[1] // 60) * 60
        matrixY, matrixX = int((len(self.root.gameMapMatrix) - 1) - (mouseY // 60)), int(mouseX // 60)

        if Window.mouse_pos[0] >= Window.size[0] * 0.1 + 60:
            self.x = mouseX + Window.size[0] * 0.1
            self.y = mouseY
        else:
            self.pos[0] = Window.size[0] * 0.1
            self.pos[1] = mouseY

        if self.top > Window.size[1]:
            self.top = Window.size[1]

        if self.addCounter == 1:
            matrixY, matrixX = self.root.compute_mouse_position(self.x - Window.size[0] * 0.1, self.y,"building")
            matrixY -= 1

            if self.build_position_possible(matrixY, matrixX):
                self.mark_position_as_used()
                self.originMatrix = [matrixY, matrixX]
                self.buildMode = False
                self.add_on_minimap()
                if self.buildingType == "Rafinery":
                    self.add_uranMiner()
                self.root.onMapObjectsToShift.append(self)
                self.root.buildings.append(self)
                self.root.buildingToAdd = []
                self.root.recomupute_all_orders()
                self.root.humanPlayer.update_power()
                if self.player == self.root.humanPlayer:
                    self.player.money -= self.buildAndEnergyCosts[self.buildingType][0]
                    self.player.power += self.buildAndEnergyCosts[self.buildingType][1]
                    self.player.update_money()
                    self.player.update_power()
                    self.player.aviableEnergy += self.buildAndEnergyCosts[self.buildingType][1]
                    if self.buildingType == "WarFactory":
                        self.root.ids["MenuButton_BuildTank"].disabled = False
                        self.root.ids["MenuButton_BuildRocketLauncher"].disabled = False
                    if self.buildingType != "MainBase":
                        self.low_power()
                pass

    def build_position_possible(self,matrixY,matrixX):
        """Checking if all fields for build are free and distance from main base"""
        maxBuildDistance = 35
        for y in range(self.matrixSize[0]):
            for x in range(self.matrixSize[1]):
                self.fullMatrixPosition.append([matrixY - y, matrixX + x])
                if (self.root.numpyMapMatrix[matrixY - y][matrixX + x] == 1
                        or math.dist([len(self.root.numpyMapMatrix)-1,0],[matrixY,matrixX]) > maxBuildDistance):
                    self.fullMatrixPosition = []
                    self.addCounter = 0
                    return False
        if self.player == self.root.humanPlayer:
            self.matrixPosition = self.fullMatrixPosition[0]
        return True

    def compute_minimapXY(self):
        """Returns building position on minimap"""
        imageX, imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size
        zeroX, zeroY = ((Window.size[0] * 0.1) * 0.025, self.root.ids["SidePanelWidget"].height * 0.83)
        posX = int((self.matrixPosition[1] * ((Window.size[0] * 0.1) * 0.95)) / len(self.root.gameMapMatrix[0]))
        posY = math.ceil((abs((self.matrixPosition[0] - (len(self.root.gameMapMatrix)))) * ( imageY * (Window.size[0] * 0.1)) / imageX) / len(self.root.gameMapMatrix[0]))
        sizeX = int((self.size[0] * ((Window.size[0] * 0.1) * 0.95)) / imageX)
        sizeY = math.ceil((abs((self.size[1] * (imageY * (Window.size[0] * 0.1)) / imageX) / imageY)))
        return zeroX,zeroY,posX,posY,sizeX,sizeY

    # Pamiętać aby usuwając budynek usuwać również obiekt minimapy - z widgetów i ze słownika obiektów minimap
    def add_on_minimap(self):
        """Adds widget representing building to minimap"""
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
        """Add uranMiner next to rafinery - need separate invoke when building matrix position is known"""
        self.fullMatrixPosition.sort(key= lambda x: x[0])
        freePlace = [self.fullMatrixPosition[0][0]+self.matrixSize[0],self.fullMatrixPosition[0][1]]
        uranMiner = UranMiner(self.root,"UranMiner",self.side,self.player,None)
        uranMiner.motherRafinery = freePlace
        uranMiner.matrixPosition = freePlace
        uranMiner.root = self.root
        uranMiner.pos = (self.pos[0],self.pos[1]-60)
        uranMiner.add_on_minimap()
        self.root.autoUnits.append(uranMiner)
        self.root.onMapObjectsToShift.append(uranMiner)
        self.root.movableObjects.append(uranMiner)
        self.root.add_widget(uranMiner,index=self.root.ids["SidePanelWidget"].index+1)
        self.root.updateGameMatrix()
        self.player.buildings.append(self)

    def mark_position_as_used(self):
        """Sets all matrix fields under building as used"""
        for position in self.fullMatrixPosition:
            self.root.numpyMapMatrix[position[0]][position[1]] = 1

    def on_press(self):
        if self.side == "Enemy":
            self.root.click_on_map("Attack", self)

    def auto_attack(self):
        # Znów defence towery nie strzelają jak należy
        for order in self.root.move_queue:
            if order[0] == self:
                return

        if self.buildingType == "DefenceTower":
            if self.target == [] and self.attack == False:
                for unit in self.root.movableObjects:
                    if unit.player != self.player and math.dist(self.matrixPosition,unit.matrixPosition) < self.shotDistance and not isinstance(unit,UranMiner):
                        auto_attack = [self, unit.matrixPosition, [self.matrixPosition], "Attack", unit,list(unit.matrixPosition.copy())]
                        self.root.move_queue.append(auto_attack)
                        return
        else:
            return


    def reset_attack(self):
        self.attack = False
        self.target = []

    def remove_object(self):
        for order in self.root.move_queue:
            if order[0] == self or order[4] == self:
                self.root.move_queue.remove(order)
        for unit in self.player.buildings:
            if unit.target == self:
                unit.target = []
                unit.attack = False

        try:
            self.root.buildings.remove(self)
        except:
            pass
        try:
            self.player.buildings.remove(self)
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
            self.root.minimapObject.remove_widget(self.minimapUnit)
            del self.root.miniMapUnits[self.minimapName]
            self.minimapName = None
            self.minimapUnit = None
        except:
            pass

        if self.buildingType == "WarFactory":
            if self.player == self.root.humanPlayer:
                self.root.ids["MenuButton_BuildTank"].disabled = True
                self.root.ids["MenuButton_BuildRocketLauncher"].disabled = True
                self.player.WarFactory = None
            else:
                self.player.WarFactory = None

        elif self.buildingType == "MainBase":
            self.player.MainBase = "Destroyed"



