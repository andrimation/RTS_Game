# Kivy
import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from MainMapPicture import MainMapPicture
from MapView import MapView
from GameObject import GameObject
from MenuButton import MenuButton
from MatrixMapWidget import MatrixMapWidget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.config import Config
from kivy.properties import BooleanProperty

# Others
import pyautogui
import math
import MarsPathfinder_setup


# Fullscreen
# Window.fullscreen = 'auto'    # To nam włacza fullscreen
# Mouse
Config.set("input","mouse","mouse,multitouch_on_demand")


class MainWindow(FloatLayout):
    obj_add_index = 1
    positionX = Window.size[0] * 0.1
    positionY = 0
    shiftX = 0
    shiftY = 0

    gameMapMatrix = []
    move_queue = []


    def deselect_all_objects_on_map(self):
        for object in self.children:
            if isinstance(object, GameObject):
                object.selected = False

    def create_map_matrix(self):
        imageX,imageY = self.ids["MainMapPicture"].ids["main_map_image"].size
        matrixX = int(imageX/60)
        matrixY = int(imageY/60)
        print(imageX,imageY)
        # Muszę pamiętać że matryca jest odwrócona
        for y in range(matrixY):
            self.gameMapMatrix.append([])
            imageY -= 60
            for x in range(matrixX):
                self.gameMapMatrix[-1].append([x*60,imageY,None])

        # DEBUG matrix print
        for x in self.gameMapMatrix:
            print(x)


    def scroll_game_map(self):
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

        # Shift all objects on map
        for element in self.children:
            if isinstance(element,GameObject):
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


        # Czyli muszę shiftować wszystko na planszy -> włacznie z wydanymi rozkazami
        # -> shifrować będę musiał też położenia kolejnych boxów matrixa mapy jak będe poruszał się po boxach
        # np, mogę zamieniać boxy na kolejne pozycje

    # Prosty algorytm wyszukiwania trasy -> sprawdzamy wolne pola wokół jednostki i mierzymy odległośc między wolnymi polami
    # i wybieiramy to wolne które jest najbliżej.
    #
    # -> bardziej złożony, ale poprawny -> algorytm który nadaje wagi poszczególnym badanym polom, z tym że większą wagę mają te pola, które
    # są bliżej

    def add_GameObject(self,add_X,add_Y,matrixX,matrixY):
        new_GameObject = GameObject()
        new_GameObject.pos = (add_X,add_Y)
        new_GameObject.size_hint = (None,None)
        new_GameObject.size = (60,60)
        new_GameObject.id   = f"Game_object_{self.obj_add_index}"
        new_GameObject.matrixPosition = [matrixX,matrixY]
        self.gameMapMatrix[matrixX][matrixY][2] = True
        self.add_widget(new_GameObject,self.obj_add_index)
        self.obj_add_index += 1
        self.ids["SidePanelWidget"].index = 0

    def move_queue_execute(self):
        for order in self.move_queue:
            object,coords,matrix = order[0],order[1],order[2]
            # print(order)
            if order[3]  and  object.moveX == 0 and object.moveY == 0:
                currentPosition = order[3].pop(0)
                if order[3]:
                    newPosition     = order[3][0]
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
            # if object.moveX == 0:
                # Y-axis
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
            if order[3] == None or order[3] == [] or order[3] == object.matrixPosition:
                try:
                    self.move_queue.remove(order)
                except:
                    pass


    def compute_mouse_position(self,*args):
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



    def click_on_map(self,*args):
        if self.ids["MenuButton_AddSelect"].selected == True:
            add_X,add_Y,matrixX,matrixY = self.compute_mouse_position(*args)
            self.add_GameObject(add_X, add_Y, matrixX, matrixY)
        # Deselect
        elif args[1].button =="right":
            self.deselect_all_objects_on_map()
        # Move objects
        elif self.ids["MenuButton_AddSelect"].selected == False:
            pos_X,pos_Y,matrixX,matrixY = self.compute_mouse_position(*args)
            # Add object,coords,and matrix to move_queue
            for object in self.children:
                if isinstance(object,GameObject) and object.selected == True:
                    try:
                        convertMatrix = MarsPathfinder_setup.convertMap(self.gameMapMatrix,self.move_queue)
                        for x in convertMatrix:
                            print(x)
                        print(object.matrixPosition, [matrixX,matrixY])
                        computePath = MarsPathfinder_setup.marsPathfinder(object.matrixPosition,[matrixX,matrixY],convertMatrix)
                        current_order = [object,(pos_X,pos_Y),(matrixX,matrixY),computePath]
                    except:
                        print("nie można obliczyc trasy")
                        pass
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

    def updateGameMatrix(self):
        positions = []
        for object in self.children:
            if isinstance(object,GameObject):
                positions.append(object.matrixPosition)
        for x in range(len(self.gameMapMatrix)-1):
            for y in range(len(self.gameMapMatrix[0])-1):
                if [x,y] in positions:
                    self.gameMapMatrix[x][y][2] = True
                else:
                    self.gameMapMatrix[x][y][2] = None


    def next_frame(self,*args):
        # Check mouse position, and move map.
        self.scroll_game_map()
        # Force mainMatrix update
        self.updateGameMatrix()
        # Move units on map
        self.move_queue_execute()

        pass

    pass



class MainGameApp(App):

    def build(self):
        mainwindow = MainWindow()
        mainwindow.create_map_matrix()
        Clock.schedule_interval(mainwindow.next_frame,0.0005)
        return mainwindow

if __name__ == "__main__":
    MainGameApp().run()
