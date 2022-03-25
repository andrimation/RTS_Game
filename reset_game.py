from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer
from MoveQueueManager import MoveQueueManager
from kivy.core.window import Window

class Game_state_reset():
    def __init__(self,root):
        self.root = root
        self.root.scrollEnabled = True
        self.root.clickOnMapEnabled = True

    def reset_everything(self):
        self.root.miniMap = None
        self.root.reset = Game_state_reset(self.root)
        self.root.humanPlayer = HumanPlayer(self.root)
        self.root.computerPlayer = ComputerPlayer(self.root)
        self.root.computerPlayerEnabled = False
        self.root.moveQueueManager = MoveQueueManager(self.root)
        for widget in self.root.children:
            self.root.children.remove(widget)
        self.root.children = self.root.startChildren


        self.root.building_add_index = 1
        self.root.obj_add_index = 1  # Indeks obiektów będzie zawsze wyższy niż budynków, więc obiekty będą zawsze chować się za budynkami
        self.root.positionX = Window.size[0] * 0.1  # Ta wartość na początku jest 800x600 - musi być później zaktualizowana ! ale tylko jednorazowo -> np przycisk start, albo coś
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

        # Separated objects lists   - more memory, but saves many "if" checking
        # Remember to remove object representation from all lists
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

        for unit in self.root.humanPlayer.units:
            unit.remove_object()
        for unit in self.root.computerPlayer.units:
            unit.remove_object()

        # Select box
        self.root.selectBoxSizes = []
        self.root.selectBoxesObjects = []

        self.root.start()