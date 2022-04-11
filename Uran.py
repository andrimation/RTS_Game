from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from UranMiner import UranMiner
from kivy.graphics import Rectangle

import math


class Uran(Button):
    def __init__(self):
        super(Uran, self).__init__()
        self.root = ""
        self.matrixPosition = []
        self.size_hint = (None,None)
        self.size = (60,60)
        self.minimapUnit = None
        self.minimapName = None
        self.source_rectangle = None
        self.find_source_rectangle()
        self.source_rectangle.source = "Models/Models_textures/Uran_source/uran.png"
        self.button = None


    def find_source_rectangle(self):
        for element in self.canvas.before.children:
            if isinstance(element,Rectangle):
                self.source_rectangle = element

    def on_release(self):
        uranMiner = None
        for object in self.root.movableObjects:
            if isinstance(object,UranMiner) and object.selected == True:
                uranMiner = object
                break
        if isinstance(uranMiner,UranMiner):
            uranMiner.closestUranSpot = self
            uranMiner.go_to_uran()
            uranMiner.selected = False

        elif uranMiner == None:
            self.root.click_on_map("Uran",self)

    def compute_minimapXY(self):
        imageX, imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size
        zeroX, zeroY = ((Window.size[0] * 0.1) * 0.025, self.root.ids["SidePanelWidget"].height * 0.83)
        posX = int((self.matrixPosition[1] * ((Window.size[0] * 0.1) * 0.95)) / len(self.root.gameMapMatrix[0]))
        posY = math.ceil((abs((self.matrixPosition[0] - (len(self.root.gameMapMatrix)))) * ( imageY * (Window.size[0] * 0.1)) / imageX) / len(self.root.gameMapMatrix[0]))
        return zeroX,zeroY,posX,posY

    # Pamiętać aby usuwając jednostkę usuwać również obiekt minimapy - z widgetów i ze słownika obiektów minimap
    def add_on_minimap(self):
        self.minimapUnit = Image()
        zeroX,zeroY,posX,posY = self.compute_minimapXY()
        self.minimapName = str(self) + "Mini"
        self.root.miniMapUnits[self.minimapName] = self.minimapUnit
        self.minimapUnit.size_hint = (None,None)
        self.minimapUnit.color = (1,0,0)
        self.minimapUnit.size = (2,2)
        self.minimapUnit.pos = (zeroX + posX, zeroY + posY)
        self.root.minimapObject.add_widget(self.minimapUnit)
        self.root.ids["SidePanelWidget"].index = 0

    def remove_minimap_widget(self):
        self.root.minimapObject.remove_widget(self.minimapUnit)
        del self.root.miniMapUnits[self.minimapName]
        self.minimapName = None
        self.minimapUnit = None






