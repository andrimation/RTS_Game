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
from kivy.config import Config
from Uran import Uran
from SelectBox import SelectBox
from kivy.config import Config
from MoveQueueManager import MoveQueueManager
from UranMiner import UranMiner
from miniMap import miniMap
from gameDataManager import Game_state_reset

# Others
import threading
import PIL
import random
import pyautogui
import math
import MarsPathfinder_setup
import numpy
import gc
import copy



# Fullscreen
Window.fullscreen = 'auto'    # To nam włacza fullscreen
# Mouse
Config.set("input","mouse","mouse,disable_multitouch")


class MainWindow(FloatLayout):

    def __init__(self):

        super(MainWindow, self).__init__()
        self.restart = 0
        self.gameDataObject = Game_state_reset(self)
        self.gameDataObject.set_game_data()
        Window.fullscreen = 'auto'

    def start(self):
        self.gameDataObject.start_game()

    def create_minimap(self):
        miniMapInit  = miniMap(self)
        miniMapInit.create_minimap()
        self.miniMap = miniMapInit

    # Selecting
    def on_touch_move(self, touch):   # Create select box
        if not self.selectedUnits:
            self.clickOnMapEnabled = False
            self.scrollEnabled = False
            if touch.pos[0] >= Window.size[0]*0.1:
                self.selectBoxSizes.append(touch.pos)
                boxStartPos = self.selectBoxSizes[0]
                selectBox = SelectBox()
                selectBox.pos = boxStartPos
                selectBox.size_hint = (None,None)
                selectBox.width = touch.pos[0]-boxStartPos[0]
                selectBox.height = touch.pos[1]-boxStartPos[1]
                self.add_widget(selectBox,index=self.ids["SidePanelWidget"].index+1)
                self.selectBoxesObjects.append(selectBox)
                if len(self.selectBoxesObjects) >= 2:
                    boxToRemove = self.selectBoxesObjects.pop(-2)
                    self.remove_widget(boxToRemove)
                self.ids["SidePanelWidget"].index = 0

    def on_touch_up(self, touch):
        if self.selectBoxesObjects:

            selectBoxOrigin = self.selectBoxSizes[0]
            boxToRemove = self.selectBoxesObjects.pop()
            rangeXStart = int(selectBoxOrigin[0])
            rangeXEnd   = int(selectBoxOrigin[0] + boxToRemove.width)
            rangeYStart = int(selectBoxOrigin[1])
            rangeYEnd   = int(selectBoxOrigin[1] + boxToRemove.height)

            if rangeXStart > rangeXEnd:
                rangeXStart,rangeXEnd = rangeXEnd,rangeXStart

            if rangeYStart > rangeYEnd:
                rangeYStart,rangeYEnd = rangeYEnd,rangeYStart

            for object in self.movableObjects:
                if object.pos[0] in range(rangeXStart,rangeXEnd) and object.pos[1] in range(rangeYStart,rangeYEnd) and object.player == self.humanPlayer:
                    object.selected = True
                    for unit in self.movableObjects:
                        if unit.combatTeam == object.combatTeam and unit.side == object.side:
                            unit.selected = object.selected
                    self.selectedUnits = True

            self.remove_widget(boxToRemove)
            self.selectBoxSizes = []

        self.scrollEnabled = True
        self.ids["SidePanelWidget"].index = 0

    def deselect_all_objects_on_map(self):
        for object in self.movableObjects:
                object.selected = False
        self.selectedUnits = False

    def create_map_matrix(self):
        imageX,imageY = self.ids["MainMapPicture"].ids["main_map_image"].size
        matrixX = int(imageX/60)
        matrixY = int(imageY/60)
        # Muszę pamiętać że matryca jest odwrócona
        for y in range(matrixY):
            self.gameMapMatrix.append([])
            imageY -= 60
            for x in range(matrixX):
                self.gameMapMatrix[-1].append([x*60,imageY])

    def convertMapNumpy(self):
        # Tworząc numpy array najpierw musze podać jej rozmiary - z lenów mojego matrixa, a dopiero później zamianieać w niej miejsce
        convertedMap = []
        for line in self.gameMapMatrix:
            newLine = []
            for point in line:
                newLine.append(0)
            convertedMap.append(newLine)
        self.numpyMapMatrix = numpy.array(convertedMap,dtype=object)

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
                if self.numpyMapMatrix[position[0] + y][position[1] + x] == 0:
                    uranOnMap.root = self
                    uranOnMap.matrixPosition = [position[0] + y, position[0] + x]
                    uranOnMap.pos = [self.gameMapMatrix[uranOnMap.matrixPosition[0]][uranOnMap.matrixPosition[1]][0]+Window.size[0]*0.1,self.gameMapMatrix[uranOnMap.matrixPosition[0]][uranOnMap.matrixPosition[1]][1]]
                    uranOnMap.add_on_minimap()
                    self.urans.append(uranOnMap)
                    self.onMapObjectsToShift.append(uranOnMap)
                    self.add_widget(uranOnMap,canvas="before",index=self.ids["SidePanelWidget"].index+1)

    def scroll_game_map(self):
        if self.scrollEnabled:
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

            # Move minimap
            if self.miniMap != None:
                self.miniMap.update_view_position(self.shiftX,self.shiftY)


            # Shift all objects on map     # Utworzyć osobne listy obiektów do shiftowania, a nie iterowac po wszystkim i robić dodatkowe ify
            for element in self.onMapObjectsToShift:
                try:
                    element.x += self.shiftX
                except:
                    pass
                try:
                    element.y += self.shiftY
                except:
                    pass

            for element in self.bullets:
                try:
                    element.x += self.shiftX
                except:
                    pass
                try:
                    element.y += self.shiftY
                except:
                    pass
        # Tu usunąłem shiftowanie rozkazów - przez to były dziwne pozycje

    def build_HumanPlayerUnit(self,unitType,side):
        self.humanPlayer.build_unit(unitType,side)

    def build_queue_execute(self):
        self.humanPlayer.execute_build_queue()

    def make_bullet(self, startObject, endPos):
        new_Bullet = Bullet()
        new_Bullet.root = startObject
        new_Bullet.targetMatrix = endPos.matrixPosition.copy()

        startPos = startObject.matrixPosition
        # if isinstance(startObject,Building):
        #     startPos = startObject.matrixPosition[0]

        new_Bullet.absoluteBulletStartX = self.gameMapMatrix[startPos[0]][startPos[1]][0]
        new_Bullet.absoluteBulletStartY  = self.gameMapMatrix[startPos[0]][startPos[1]][1]

        targetMatrixPos = new_Bullet.root.target.matrixPosition
        # if isinstance(new_Bullet.root.target,Building):
        #     targetMatrixPos = new_Bullet.root.target.matrixPosition[0]

        new_Bullet.absoluteTargetX = self.gameMapMatrix[targetMatrixPos[0]][targetMatrixPos[1]][0]
        new_Bullet.absoluteTargetY = self.gameMapMatrix[targetMatrixPos[0]][targetMatrixPos[1]][1]
        new_Bullet.distanceToFly = startObject.shotDistance
        new_Bullet.pos   = [startObject.pos[0],startObject.pos[1]]
        new_Bullet.id = f"Bullet{self.obj_add_index}"
        new_Bullet.size_hint = (None, None)
        new_Bullet.target = endPos
        new_Bullet.size = (20, 20)
        self.bullets.append(new_Bullet)
        self.add_widget(new_Bullet,index=self.ids["SidePanelWidget"].index+1,canvas="after")
        self.obj_add_index += 1
        self.ids["SidePanelWidget"].index = 0


    def add_building(self,*args):
        self.deselect_all_objects_on_map()
        buildingAdd = Building(self,args[1],self.humanPlayer,args[0])
        buildingAdd.add_to_game()

    def move_building_on_map(self):
        if self.buildingToAdd:
            currentBuilding = self.buildingToAdd[0]
            currentBuilding.move_building_widget_along_cursor()

    def update_money(self):
        self.ids["Money_label"].text = str(self.humanPlayer.money)

    def bullet_shot_execute(self):
        for bullet in self.bullets:
            bulletRootPos = bullet.root.matrixPosition

            if bullet.target == None:
                self.bullets.remove(bullet)
                self.remove_widget(bullet)
                continue
            elif bullet.target.health <= 0:
                self.bullets.remove(bullet)
                self.remove_widget(bullet)
                continue
            distance = math.dist(bullet.root.pos,bullet.target.pos)
            x = abs(bullet.absoluteBulletStartX-bullet.absoluteTargetX)/60
            y = abs(bullet.absoluteBulletStartY-bullet.absoluteTargetY)/60

            if bullet.target.health <= 0 or bullet.target == None or bullet.target == []:
                self.bullets.remove(bullet)
                self.remove_widget(bullet)
                continue
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
            # Bullet hit
            if bullet.collide_widget(bullet.target):
                bullet.target.health -= bullet.root.firePower
                self.ids["MainMapPicture"].draw_explosion([bullet.absoluteTargetY,bullet.absoluteTargetX])
                self.bullets.remove(bullet)
                self.remove_widget(bullet)

            elif math.dist(bulletRootPos,[bulletRootPos[0]+bullet.moveX//60,bulletRootPos[1]+bullet.moveY//60]) >= bullet.distanceToFly:
                self.bullets.remove(bullet)
                self.remove_widget(bullet)



    def move_queue_execute(self):
        self.moveQueueManager.execute_units_movement()

    def make_attack(self):
        self.moveQueueManager.attack()

    def compute_mouse_position(self,*args):
        if args[-1] == "building":
            imageY = self.ids["MainMapPicture"].ids["main_map_image"].size[1]
            x, y = args[0],args[1]
            bigMatrixY = math.floor(abs((abs(self.positionY) + y) - imageY) // 60)
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
        # self.moveQueueManager.compute_paths_for_orders()
        self.moveQueueManager.pathThreads_creator()
        # print(self.path_compute_threads)

    # Funkcja czyści wszystkie pending rozkazy i dodaje zje znów do orders destinations.
    # Jakby tu zrobić że oznacza tylko rozkazy do usunięcia, a później co jedną klatkę usuwa i przelicza 1 rozkaz
    # - to by nie bylo takiego laga w momencie dodawania budynku
    def recomupute_all_orders(self):
        self.orders_destinations = []
        for order in self.move_queue:
            try:
                self.orders_destinations.append([order[0],order[2][-1],order[3],order[4],None])
                if isinstance(order[0],Building):
                    order[0].reset_attack()
            except:
                pass

    def click_on_map(self,*args):   # Dodac ograniczenie że za jednym razem można np max 7 unitów
        self.updateGameMatrix()
        try:
            if args[1].button == "right":
                return self.deselect_all_objects_on_map()
        except:
            pass
        if args[0] != "Attack":
            # Deselect
            if args[1].button =="right":
                self.deselect_all_objects_on_map()

            # Move objects
            elif self.ids["MenuButton_AddSelect"].selected == False:
                pos_X,pos_Y,matrixX,matrixY = self.compute_mouse_position(*args)
            else:
                self.buildingToAdd = []

        # Add object,coords to orders compute
        elif args[0] == "Attack":
                matrixX, matrixY = args[1].matrixPosition
        selectedObjectsList = []
        for object in self.movableObjects:
            if  object.selected == True : #and object.side == "Friend":
                selectedObjectsList.append(object)
        # usedCoords = []
        if args[0] == "Attack":
            move = "Attack"
            target = args[1]
            # usedCoords.append([matrixX,matrixY])
        else:
            move = "Move"
            target = None
        if selectedObjectsList:
            for object in selectedObjectsList:
                if move == "Move":
                    self.orders_destinations.append([object, [matrixX, matrixY],move,target,None])
                    continue
                elif move == "Attack" and isinstance(object,UranMiner):
                    move = "Move"
                    self.orders_destinations.append([object, [matrixX, matrixY], move,target,list(target.matrixPosition.copy())])
                    continue
                elif move == "Attack":
                    self.orders_destinations.append([object, [matrixX, matrixY], move, target, list(target.matrixPosition.copy())])
                    continue

    def update_positionX(self):
        self.positionX = Window.size[0] * 0.1

    # Nie updejtować force matrixa co klatkę ! - zbyt kosztowne, np co kliknięcie
    def updateGameMatrix(self):
        positions = []
        for object in self.children:
            if isinstance(object, GameUnit):
                positions.append(object.matrixPosition)
            elif isinstance(object, Building):
                for smallPos in object.fullMatrixPosition:
                    positions.append(smallPos)

        for x in range(len(self.gameMapMatrix)-1):
            for y in range(len(self.gameMapMatrix[0])-1):
                if [x,y] in positions:
                    self.numpyMapMatrix[x][y] = 1
                else:
                    self.numpyMapMatrix[x][y] = 0

    def manage_auto_units(self):
        # uran miner
        for object in self.autoUnits:
            object.mineUran()

        for object in self.movableObjects:
            object.auto_attack()

        for building in self.buildings:
            building.auto_attack()

    def order_and_units_cleaner(self):
        for order in self.orders_destinations:
            if isinstance(order[0],GameUnit)and not isinstance(order[3],Building) and order[3] not in self.movableObjects and order[2] == "Attack":
                order[0].attack = False
                order[0].target = []
                self.orders_destinations.remove(order)
            if isinstance(order[0],GameUnit) and order[0] not in self.movableObjects:
                self.orders_destinations.remove(order)
        for order in self.move_queue:
            if isinstance(order[0],GameUnit) and not isinstance(order[4],Building) and order[4] not in self.movableObjects and order[3] == "Attack":
                order[0].attack = False
                order[0].target = []
                try:
                    self.move_queue.remove(order)
                except:
                    pass
            if isinstance(order[0],GameUnit) and order[0] not in self.movableObjects:
                try:
                    self.move_queue.remove(order)
                except:
                    pass
            if isinstance(order[0],Building) and order[4] not in self.movableObjects:
                order[0].attack = False
                order[0].target = []
                try:
                    self.move_queue.remove(order)
                except:
                    pass

    def check_if_loose(self):  # Zmienić że poprostu zniszczenie main base.
        if self.humanPlayer.money < 650 * 5 and self.humanPlayer.units == []:
            self.time = 0.5
            self.gameDataObject.reset_game_objects()
            self.gameDataObject.set_game_data()
            self.start()
        elif self.computerPlayer.money < 650 * 5 and self.computerPlayer.units == []:
            self.gameDataObject.reset_game_objects()
            self.gameDataObject.set_game_data()
            self.start()

###########################################################################

    def next_frame(self,*args):

        # Check mouse position, and move map.
        self.scroll_game_map()

        # Compute paths
        self.compute_orders_paths()

        # Attack
        self.make_attack()

        # Bulet shot
        self.bullet_shot_execute()

        # Move units on map
        self.move_queue_execute()

        # Adding buildings
        self.move_building_on_map()

        # Auto units behave
        self.manage_auto_units()

        # execute build queue
        self.build_queue_execute()

        # Clean orders
        self.order_and_units_cleaner()

        # Make sure panel inex is 0
        self.ids["SidePanelWidget"].index = 0

        # Computer Player
        if self.computerPlayerEnabled:
            self.computerPlayer.execute_Computer_Play()

        self.check_if_loose()

        self.ids["MainMapPicture"].clear_explosions()

    pass

class MainGameApp(App):

    def build(self):
        mainwindow = MainWindow()
        Clock.schedule_interval(mainwindow.next_frame,0.008)
        return mainwindow

if __name__ == "__main__":
    MainGameApp().run()