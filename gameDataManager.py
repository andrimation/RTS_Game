from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer
from MoveQueueManager import MoveQueueManager
from kivy.core.window import Window
from GameUnit import GameUnit
from Building import Building
from Uran import Uran
from UranMiner import UranMiner

class Game_state_reset():
    def __init__(self,root):
        self.root = root
        self.root.scrollEnabled = True
        self.root.clickOnMapEnabled = True

    def set_game_data(self):
        self.root.miniMap = None
        self.root.gameDataObject = Game_state_reset(self.root)
        self.root.humanPlayer = HumanPlayer(self.root)
        self.root.computerPlayer = ComputerPlayer(self.root)
        self.root.computerPlayerEnabled = False
        self.root.moveQueueManager = MoveQueueManager(self.root)

        self.root.building_add_index = 1
        self.root.obj_add_index = 1
        self.root.positionX = Window.size[0] * 0.1
        self.root.positionY = 0
        self.root.shiftX = 0
        self.root.shiftY = 0
        self.root.scrollEnabled = True
        self.root.clickOnMapEnabled = True
        self.root.counter = 0
        self.root.miniMapCounter = 0

        self.root.gameMapMatrix = []
        self.root.numpyMapMatrix = []
        self.root.move_queue = []
        self.root.orders_destinations = []

        self.root.buildingToAdd = []
        self.root.miniMapObject = None
        self.root.miniMapUnits = {}
        self.root.humanPlayerUnits = []
        self.root.computerPlayerUnits = []
        self.root.combatTeamsCounterHuman = 0
        self.root.combatTeamsCounterComp = 0

        self.root.selectedUnits = False
        self.root.onMapObjectsToShift = []
        self.root.movableObjects = []
        self.root.buildings = []
        self.root.bullets = []
        self.root.autoUnits = []
        self.root.urans = []
        self.root.ids["MainMapPicture"].shiftXCounter = 0
        self.root.ids["MainMapPicture"].shiftYCounter = 0
        self.root.ids["MainMapPicture"].x = 0
        self.root.ids["MainMapPicture"].y = 0
        self.root.ids["MapView"].root = self.root
        self.root.ids["MainMapPicture"].root = self.root
        self.root.ids["MapView"].scroll_timeout = 1  # Zsisablować multitouch
        self.root.ids["MapView"].scroll_distance = 100000000
        self.root.ids["MainMapPicture"].scroll_timeout = 1
        self.root.ids["MainMapPicture"].scroll_distance = 100000000

        # Selection box
        self.root.selectBoxSizes = []
        self.root.selectBoxesObjects = []

        # Buttons status
        self.root.ids["MenuButton_BuildMainBase"].disabled = False
        self.root.ids["MenuButton_BuildRafinery"].disabled = True
        self.root.ids["MenuButton_BuildPowerPlant"].disabled = True
        self.root.ids["MenuButton_BuildWarFactory"].disabled = True
        self.root.ids["MenuButton_BuildDefenceTower"].disabled = True

    def start_game(self):

        self.root.startChildren = self.root.children.copy()
        self.root.create_map_matrix()
        self.root.convertMapNumpy()
        self.root.remove_widget(self.root.ids["StartButton"])
        self.root.ids["MenuButton_BuildMainBase"].disabled = False
        self.root.positionX = Window.size[0] * 0.1
        self.root.create_minimap()
        self.root.add_uran()
        self.root.update_money()
        self.root.computerPlayerEnabled = True
        self.root.computerPlayer.execute_build_plan()

    def reset_game_objects(self):
        for uranMiner in self.root.onMapObjectsToShift:
            if isinstance(uranMiner,UranMiner):
                self.root.urans.remove(uranMiner.closestUranSpot)
                self.root.onMapObjectsToShift.remove(uranMiner.closestUranSpot)
                self.root.remove_widget(uranMiner.closestUranSpot)
                for uran in uranMiner.uranSpots:
                    self.root.remove_widget(uran)
                if uranMiner.closestUran != None:
                    self.root.remove_widget(uranMiner.closestUran)

        for unit in self.root.onMapObjectsToShift:
            if isinstance(unit, GameUnit):
                unit.remove_object()
        for building in self.root.onMapObjectsToShift:
            if isinstance(building, Building):
                building.remove_object()

        for uran in self.root.onMapObjectsToShift:
            if isinstance(uran,Uran):
                uran.remove_minimap_widget()
                self.root.urans.remove(uran)
                self.root.onMapObjectsToShift.remove(uran)
                self.root.remove_widget(uran)


