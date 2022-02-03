# Kivy
import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from MainMapPicture import MainMapPicture
from MapView import MapView
from GameUnit import GameUnit,Bullet
from Building import Building
from MenuButton import MenuButton
from MatrixMapWidget import MatrixMapWidget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.config import Config
from kivy.properties import BooleanProperty
from kivy.animation import Animation
from HumanPlayer import HumanPlayer
from Uran import Uran
from UranMiner import UranMiner
# Others
import random
import pyautogui
import math
import MarsPathfinder_setup
import numpy
import time
import gc

# Fullscreen
Window.fullscreen = 'auto'    # To nam włacza fullscreen
# Mouse
Config.set("input","mouse","mouse,multitouch_on_demand")


class MainWindow(FloatLayout):


    def __init__(self):
        super(MainWindow, self).__init__()
        self.humanPlayer = HumanPlayer(self)
        Window.fullscreen = 'auto'

        self.building_add_index = 1
        self.obj_add_index = 1 # Indeks obiektów będzie zawsze wyższy niż budynków, więc obiekty będą zawsze chować się za budynkami
        self.positionX = Window.size[0]*0.1   # Ta wartość na początku jest 800x600 - musi być później zaktualizowana ! ale tylko jednorazowo -> np przycisk start, albo coś
        self.positionY = 0
        self.shiftX = 0
        self.shiftY = 0

        self.gameMapMatrix = []
        self.numpyMapMatrix = []
        self.move_queue = []
        self.orders_destinations = []
        self.buildingToAdd = []

        self.toRemove = []

        # Separated objects lists
        self.objectsToShift = []
        self.autoUnits = []

    def start(self):
        self.remove_widget(self.ids["StartButton"])
        self.positionX = Window.size[0] * 0.1
        print(Window.size)
        self.add_uran()


    def deselect_all_objects_on_map(self):
        for object in self.children:
            if isinstance(object, GameUnit):
                object.selected = False

    def create_map_matrix(self):
        imageX,imageY = self.ids["MainMapPicture"].ids["main_map_image"].size
        matrixX = int(imageX/60)
        matrixY = int(imageY/60)
        # Muszę pamiętać że matryca jest odwrócona
        for y in range(matrixY):
            self.gameMapMatrix.append([])
            imageY -= 60
            for x in range(matrixX):
                self.gameMapMatrix[-1].append([x*60,imageY,None])

    def convertMapNumpy(self):
        convertedMap = []
        for line in self.gameMapMatrix:
            newLine = []
            for point in line:
                newLine.append("")
            convertedMap.append(newLine)
        self.numpyMapMatrix = numpy.char.array(convertedMap)

    def add_uran(self):
        uranOrigins = [[random.randint(0, len(self.gameMapMatrix) - 1),random.randint(0, len(self.gameMapMatrix[0]) - 1)] for x in range(10)]
        for position in uranOrigins:
            count = random.randint(5, 15)
            for nugget in range(count):
                uranOnMap = Uran()
                y = random.randint(-5, 5)
                while position[0] + y > len(self.gameMapMatrix)-1 or position[0] + y < 0:
                    y = random.randint(-5, 5)
                x = random.randint(-5, 5)
                while position[1] + x > len(self.gameMapMatrix[0])-1 or position[0] + y < 0:
                    x = random.randint(-5, 5)
                if self.gameMapMatrix[position[0] + y][position[1] + x][2] == None:
                    uranOnMap.root = self
                    uranOnMap.matrixPosition = [position[0] + y, position[0] + x]
                    # Wtf ?! why 112 ?
                    # a - > bo mamy zły rozmiar ekranu - add uran musi nastąpić po wciśnięciu buttona :)
                    uranOnMap.pos = [self.gameMapMatrix[uranOnMap.matrixPosition[0]][uranOnMap.matrixPosition[1]][0]+Window.size[0]*0.1,self.gameMapMatrix[uranOnMap.matrixPosition[0]][uranOnMap.matrixPosition[1]][1]]
                    self.add_widget(uranOnMap,canvas="before",index=self.obj_add_index)

    def scroll_game_map(self):
        self.ids["MainMapPicture"].older = self  # Przekazanie selfa do mainMapPicture
        mouseX,mouseY = pyautogui.position()
        width,height = pyautogui.size()
        mouseY = abs(mouseY-height)  # Bo pyautogui ma y 0 na górze !
        self.shiftX = self.ids["MainMapPicture"].moveX(mouseX,width)
        self.shiftY = self.ids["MainMapPicture"].moveY(mouseY,height)

        # Shift value for mouse position
        try:
            self.positionX += self.shiftX
        except:
            pass
        try:
            self.positionY += self.shiftY
        except:
            pass

        # Shift all objects on map     # Utworzyć osobne listy obiektów do shiftowania, a nie iterowac po wszystkim i robić dodatkowe ify
        for element in self.children:
            if isinstance(element, GameUnit) or isinstance(element, Building) or isinstance(element,Uran) or isinstance(element,UranMiner):
                try:
                    element.x += self.shiftX
                except:
                    pass
                try:
                    element.y += self.shiftY
                except:
                    pass

        for element in self.children:
            if  isinstance(element,Bullet):
                try:
                    element.x += self.shiftX
                except:
                    pass
                try:
                    element.y += self.shiftY
                except:
                    pass

        #Shift orders
        for order in self.move_queue:
            coordX,coordY = order[1]
            try:
                coordX += self.shiftX
            except:
                pass
            try:
                coordY += self.shiftY
            except:
                pass
            order[1] = (coordX, coordY)

    # Pamiętać żeby jak wcisnę jakiś guzik z dodawaniem czegokolwiek, to żeby odznaczac wszystkie jednostki !!! - albo w ogóle zatrzymać całą grę !
    def add_GameObject(self,add_X,add_Y,matrixX,matrixY):
        self.deselect_all_objects_on_map()
        new_GameObject = GameUnit()
        new_GameObject.pos = (add_X,add_Y)
        new_GameObject.size_hint = (None,None)
        new_GameObject.size = (60,60)
        new_GameObject.id   = f"Game_object_{self.obj_add_index}"
        new_GameObject.matrixPosition = [matrixX,matrixY]
        new_GameObject.root = self
        if self.obj_add_index > 2 :
            new_GameObject.side = "Enemy"
        self.gameMapMatrix[matrixX][matrixY][2] = True
        self.add_widget(new_GameObject,canvas="before",index=self.obj_add_index)
        self.ids["SidePanelWidget"].index = 0

    def make_bullet(self, startObject, endPos):
        new_Bullet = Bullet()
        new_Bullet.root = startObject
        new_Bullet.targetMatrix = endPos.matrixPosition.copy()
        new_Bullet.absoluteBulletStartX = self.gameMapMatrix[startObject.matrixPosition[0]][startObject.matrixPosition[1]][0]
        new_Bullet.absoluteBulletStartY  = self.gameMapMatrix[startObject.matrixPosition[0]][startObject.matrixPosition[1]][1]
        new_Bullet.absoluteTargetX = self.gameMapMatrix[new_Bullet.targetMatrix[0]][new_Bullet.targetMatrix[1]][0]
        new_Bullet.absoluteTargetY = self.gameMapMatrix[new_Bullet.targetMatrix[0]][new_Bullet.targetMatrix[1]][1]
        new_Bullet.distanceToFly = startObject.shotDistance
        new_Bullet.pos   = [startObject.pos[0],startObject.pos[1]]
        new_Bullet.id = f"Bullet{self.obj_add_index}"
        new_Bullet.size_hint = (None, None)
        new_Bullet.target = endPos
        new_Bullet.size = (20, 20)
        self.add_widget(new_Bullet)
        self.obj_add_index += 1
        self.ids["SidePanelWidget"].index = 0

    def add_building(self,*args):
        self.deselect_all_objects_on_map()
        buildingAdd = Building()
        buildingAdd.add_to_game(self,args[0])

    def move_building_on_map(self):
        if self.buildingToAdd:
            mouseX = (((Window.mouse_pos[0] - Window.size[0]*0.1)//60))*60
            mouseY = (Window.mouse_pos[1] //60) * 60
            matrixY, matrixX = int((len(self.gameMapMatrix) - 1) - (mouseY // 60)), int(mouseX // 60)

            if Window.mouse_pos[0] >= Window.size[0] * 0.1+60:
                self.buildingToAdd[0].x = mouseX+Window.size[0] * 0.1
                self.buildingToAdd[0].y = mouseY
            else:
                self.buildingToAdd[0].pos[0] = Window.size[0]*0.1
                self.buildingToAdd[0].pos[1] = mouseY

            if  self.buildingToAdd[0].top > Window.size[1]:
                self.buildingToAdd[0].top = Window.size[1]

            if  self.buildingToAdd[0].addCounter == 1:

                matrixY,matrixX = self.compute_mouse_position(self.buildingToAdd[0].x-Window.size[0]*0.1,self.buildingToAdd[0].y,"building")
                matrixY -= 1

                for y in range(self.buildingToAdd[0].matrixSize[0]):
                    for x in range(self.buildingToAdd[0].matrixSize[1]):
                        self.buildingToAdd[0].matrixPosition.append([matrixY - y, matrixX + x])
                        self.gameMapMatrix[matrixY-y][matrixX+x][2] = True
                self.buildingToAdd[0].buildMode = False
                if self.buildingToAdd[0].buildingType == "Rafinery":
                    self.buildingToAdd[0].add_uranMiner()
                self.buildingToAdd = []
                self.recomupute_all_orders()
                pass

        # Zatwierdzić pozycję po kliknięciu w mapę

    def remove_assets(self):
        for asset in self.toRemove:
           self.remove_widget(asset)

    def bullet_shot_execute(self):
        for bullet in self.children:
            if isinstance(bullet,Bullet):
                distance = math.dist(bullet.root.pos,bullet.target.pos)
                x = abs(bullet.absoluteBulletStartX-bullet.absoluteTargetX)/60
                y = abs(bullet.absoluteBulletStartY-bullet.absoluteTargetY)/60

                if bullet.absoluteBulletStartX < bullet.absoluteTargetX:
                    try:
                        bullet.x += bullet.speed * x/distance
                        bullet.moveX += bullet.speed*x/distance
                    except:
                        pass
                else:
                    try:
                        bullet.x -= bullet.speed*x/distance
                        bullet.moveX -= bullet.speed*x/distance
                    except:
                        pass

                if bullet.absoluteBulletStartY < bullet.absoluteTargetY:
                    try:
                        bullet.y += bullet.speed*y/distance
                        bullet.moveY += bullet.speed*y/distance
                    except:
                        pass
                else:
                    try:
                        bullet.y -= bullet.speed*y/distance
                        bullet.moveY -= bullet.speed*y/distance
                    except:
                        pass
                if bullet.collide_widget(bullet.target):
                    self.remove_widget(bullet)
                    bullet.target.health -= bullet.shotPower
                elif math.dist(bullet.root.matrixPosition,[bullet.root.matrixPosition[0]+bullet.moveX//60,bullet.root.matrixPosition[1]+bullet.moveY//60]) >= bullet.distanceToFly:
                    self.remove_widget(bullet)

    def move_queue_execute(self):
        for order in self.move_queue:
            object, matrix = order[0], order[1]
            if order[3] == "Move":
                object.attack = False
                object.target = []

            if order[2]  and  object.moveX == 0 and object.moveY == 0:
                try:
                    currentPosition = order[2].pop(0)
                except:
                    continue
                if order[2]:
                    newPosition     = order[2][0]
                    if self.gameMapMatrix[newPosition[0]][newPosition[1]][2] == True:
                        computePath = MarsPathfinder_setup.marsPathfinder(object.matrixPosition, [order[2][-1][0], order[2][-1][1]],self.numpyMapMatrix)
                        order[2] = computePath
                        continue

                    if currentPosition[1] < newPosition[1]:
                        object.moveX = 60
                    if currentPosition[1] > newPosition[1]:
                        object.moveX = -60
                    if currentPosition[0] < newPosition[0]:
                        object.moveY = -60
                    if currentPosition[0] > newPosition[0]:
                        object.moveY = 60
                    self.gameMapMatrix[currentPosition[0]][currentPosition[1]][2] = None
                    object.matrixPosition = newPosition
                    self.gameMapMatrix[object.matrixPosition[0]][object.matrixPosition[1]][2] = True
                else:
                    object.matrixPosition = currentPosition

            if object.moveX > 0:
                object.x += 2
                object.moveX -= 2
            elif object.moveX < 0:
                object.x -= 2
                object.moveX += 2
            else:
                pass

            if object.moveY > 0:
                object.y += 2
                object.moveY -= 2
            elif object.moveY < 0:
                object.y -= 2
                object.moveY += 2
            else:
                pass
        # Remove object from move queue if order finished
        for order in self.move_queue:
            if order[1] == object.matrixPosition or order[2] == []:

                try:
                    self.move_queue.remove(order)
                except:
                    pass

    def make_attack(self):
        for order in self.move_queue:
            if order[3] == "Attack" and order[4] != None and order[4] != []:
                object = order[0]
                target = order[4]
                if math.dist(object.matrixPosition,target.matrixPosition) < object.shotDistance and object.moveX == 0 and object.moveY == 0:
                    self.gameMapMatrix[object.matrixPosition[0]][object.matrixPosition[1]][2] = True
                    self.move_queue.remove(order)
                    object.attack = True
                    object.target = target
                else:
                    object.attack = True
                    object.target = []
        for object in self.children:
            if isinstance(object, GameUnit):
                if object.target != [] and object.target != None:
                    if math.dist(object.matrixPosition,object.target.matrixPosition) > object.shotDistance:
                        object.attack = False
                        if object.wait == 50:
                            self.orders_destinations.append([object, object.target.moveEndPosition, "Attack", object.target])
                            object.wait = 0
                        else:
                            object.wait += 1
                            continue
                    elif object.target.health <= 0:
                        self.remove_widget(object.target)
                        object.attack = False
                        object.target = []
                    elif object.attack == True:
                        if object.reloadCounter == object.reloadTime:
                            self.make_bullet(object,object.target)
                            object.reloadCounter = 0
                        else:
                            object.reloadCounter += 1

    def compute_mouse_position(self,*args):

        if args[-1] == "building":
            imageY = self.ids["MainMapPicture"].ids["main_map_image"].size[1]
            x, y = args[0],args[1]
            mouseX = (((Window.mouse_pos[0] - Window.size[0] * 0.1) // 60)) * 60
            bigMatrixY = math.floor(abs((abs(self.positionY) + y) - imageY) // 60)
            bigMatrixX = (((Window.mouse_pos[0] - Window.size[0] * 0.1) // 60))
            bigMatrixX = math.floor(x + abs(self.positionX - Window.size[0] * 0.1)) // 60
            return bigMatrixY,bigMatrixX
        # Convert kivy X,Y coords, to matrix coords
        imageY = self.ids["MainMapPicture"].ids["main_map_image"].size[1]
        x, y = args[1].pos

        # Actual cursor position in window.
        pos_X = (x // 60) * 60 + (Window.size[0] * 0.1)
        pos_Y = (y // 60) * 60

        # Cursor position in whole game matrix
        bigMatrixY = math.floor(abs((abs(self.positionY) + y) - imageY)//60)
        bigMatrixX = math.floor(x + abs(self.positionX-Window.size[0]*0.1))//60
        return pos_X, pos_Y, bigMatrixY, bigMatrixX

    def compute_orders_paths(self):
        usedCoords = []
        for destination in self.orders_destinations:
            usedCoords.append(destination[1])

        for order_destination in self.orders_destinations:
            if usedCoords.count(order_destination[1]) > 1:
                order_destination[1] = MarsPathfinder_setup.find_Closesd_Free(self.numpyMapMatrix,order_destination[1])
            try:
                computePath = MarsPathfinder_setup.marsPathfinder(order_destination[0].matrixPosition, [order_destination[1][0], order_destination[1][1]],self.numpyMapMatrix)
                current_order = [order_destination[0], (order_destination[1][0], order_destination[1][1]), computePath,order_destination[2],order_destination[3],""]
                order_destination[0].moveEndPosition = computePath[-1]
            except:
                computePath = None
                self.orders_destinations.remove(order_destination)
                continue
            if computePath != None:
                self.orders_destinations.remove(order_destination)
                # Remove old order if object got new during old
                for order in self.move_queue:
                    try:
                        if order[0] == current_order[0]:
                            self.move_queue.remove(order)
                    except:
                        pass
                try:
                    self.move_queue.append(current_order)
                except:
                    pass

    # Funkcja czyści wszystkie pending rozkazy i dodaje zje znów do orders destinations.
    def recomupute_all_orders(self):
        self.orders_destinations = []
        for order in self.move_queue:
            try:
                self.orders_destinations.append([order[0],order[2][-1],order[3],order[4]])
            except:
                pass
        self.move_queue = []

    def click_on_map(self,*args):   # Dodac ograniczenie że za jednym razem można np max 7 unitów
        if args[0] != "Attack":
            # Add unit
            if self.ids["MenuButton_AddSelect"].selected == True:
                add_X,add_Y,matrixX,matrixY = self.compute_mouse_position(*args)
                self.add_GameObject(add_X, add_Y, matrixX, matrixY)

            # Deselect
            elif args[1].button =="right":
                self.deselect_all_objects_on_map()

            # Move objects
            elif self.ids["MenuButton_AddSelect"].selected == False:
                pos_X,pos_Y,matrixX,matrixY = self.compute_mouse_position(*args)
            else:
                self.buildingToAdd = []

        # Add object,coords to orders compute
        elif args[0] == "Attack":
            matrixX,matrixY = args[1].matrixPosition
        selectedObjectsList = []
        for object in self.children:
            if isinstance(object, GameUnit) and object.selected == True : #and object.side == "Friend":
                selectedObjectsList.append(object)
        usedCoords = []
        if args[0] == "Attack":
            move = "Attack"
            target = args[1]
            usedCoords.append([matrixX,matrixY])
        else:
            move = "Move"
            target = None
        if selectedObjectsList:
            for object in selectedObjectsList:
                if [matrixX, matrixY] not in usedCoords:
                    object.matrixDestination = [matrixX, matrixY]
                    usedCoords.append([matrixX, matrixY])
                else:
                    convertedMap = MarsPathfinder_setup.convertMap(self.gameMapMatrix)
                    convertedMap[matrixX][matrixY] = "A"
                    matrixX, matrixY = MarsPathfinder_setup.find_Closesd_Free(convertedMap, [matrixX, matrixY])
                    usedCoords.append([matrixX, matrixY])
                self.orders_destinations.append([object, [matrixX, matrixY],move,target])

    def update_positionX(self):
        self.positionX = Window.size[0] * 0.1
        print(self.positionX)

    def updateGameMatrix(self):
        positions = []
        for object in self.children:
            if isinstance(object, GameUnit):
                positions.append(object.matrixPosition)
            elif isinstance(object, Building):
                for smallPos in object.matrixPosition:
                    positions.append(smallPos)
        for x in range(len(self.gameMapMatrix)-1):
            for y in range(len(self.gameMapMatrix[0])-1):
                if [x,y] in positions:
                    self.gameMapMatrix[x][y][2] = True
                    self.numpyMapMatrix[x][y] = "A"
                else:
                    self.gameMapMatrix[x][y][2] = None
                    self.numpyMapMatrix[x][y]   = ""

        # Tu coś jest nie tak - w trakcie ruchu budybki znikają ??

    def manage_auto_units(self):
        # uran miner
        for object in self.children:
            if isinstance(object,UranMiner):
                object.mineUran()




###########################################################################

    def next_frame(self,*args):
        counter = 0
        # Check mouse position, and move map.
        self.scroll_game_map()
        # Force mainMatrix update
        self.updateGameMatrix()
        # Compute paths for orders
        self.compute_orders_paths()
        # Attack
        self.make_attack()
        # Bulet shot
        self.bullet_shot_execute()
        # Move units on map
        self.move_queue_execute()
        # Adding buildings
        self.move_building_on_map()
        # manage auto units
        self.manage_auto_units()
        counter += 1
        if counter == 10000:
            gc.collect()
            counter = 0
        pass

    pass



class MainGameApp(App):

    def build(self):
        mainwindow = MainWindow()
        mainwindow.create_map_matrix()
        mainwindow.convertMapNumpy()
        Clock.schedule_interval(mainwindow.next_frame,0.0005)
        return mainwindow

if __name__ == "__main__":
    MainGameApp().run()