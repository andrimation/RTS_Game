# - napisać AI kompa
#   - komputer będzie miał 3 podstawowe stany: budowa bazy/jednostek/obrony   , obrona - bazy/zbieraczy,   atak
#       - budowa bazy: na początku buduje elektrownie, 2 rafinerie, i losuje czy WarFactory + czołgi czy 3 rafinerie + defence tower.
#       - zaczyna budować czołgi, jest w trybie obrony -> losuje czy wybudować 5 czołgów czy rafinerę, czy wieżę obronną
#       - jeśli wybudował odpowiednio, to atakuje- atak nie przerywa procesu budowania bazy

#       Atak:
#       - jeśli ma liczbę czołgów, dział podobną do humana +/- losowa między (4 a 11) to atakuje.
#       - losuje sposoby ataku - wojska dzieli na 2, 3, 4 grupy, z czego zawsze jedna zostaje w bazie dla obrony
#           - jeśli jest 1 grupa atakująca to atakuje najpierw jednostki playera, i towery, a jeśli zostanie bardzo mało jednostek lub 0, to atakuje budynki
#           - jeśli atakują 2,3 grupy to 1,2 atakują jednostki, a jedna budynek - rafineria, war factory, main base itp

#       Obrona:
#       - obrona włącza się jeżeli atakowana jest baza lub minery. - wtedy do obrony rzuca się co najmniej tyle jednostek ile jest atakujących
#       w jakiejś tam odległosci od atakowanego obiektu, lub wszystkie dostępne, jeśli jest za mało

# Musi istnieć jakaś kolejka, żeby komp nie zmieniał ciągle zdania co robi.
# Generalnie tryb budowy działa cały czas, natomiast tryb obrona/atak zmienia się w zależnosci od okoliczności
# No i musi istnieć jakiś delay w budowie budynków przez kompa, żeby nie wszystkie na raz, a po kolei
from kivy.core.window import Window
from Building import Building
from GameUnit import GameUnit

import random
import MarsPathfinder_setup
import time

class ComputerPlayer():
    def __init__(self,root):
        self.root = root
        self.money = 150_000
        self.power = 50_000

        self.computerBuildDelay = 0
        self.computerBuildDelayTIME = 1000
        self.computerActDelay   = 0
        self.aviableUnits = ["Tank","RocketLauncher"]
        self.computerBuildingQueue = [["MainBase",[7,52]],["WarFactory",[4,47]],["Rafinery",[12,53]],
                                      ["Rafinery",[10,47]],["Rafinery",[6,40]],["Rafinery",[7,35]],
                                      ["DefenceTower",[1,34]],["DefenceTower",[1,19]],["DefenceTower",[20,54]],
                                      ["DefenceTower",[5,24]],["DefenceTower",[10,28]],["DefenceTower",[14,33]],
                                      ["DefenceTower",[16,39]],["DefenceTower",[18,46]]]
        # self.computerBuildingQueue = [["DefenceTower",[10,28]]]
        self.buildUnitsQueue = []
        self.rafineries = 0
        self.MainBase = None
        self.WarFactory = None
        self.units = []
        self.unitsNoOrders = []
        self.buildings = []
        self.playerMaxUnitsCount = 25
        self.combatTeams = 0
        self.attackCounter = 0
        self.side = "Enemy"


    # Delay Functions
    def build_Delay(self):
        if self.computerBuildDelay != self.computerBuildDelayTIME:
            self.computerBuildDelay += 1
        else:
            self.computerBuildDelay = 0
            self.computerBuildDelayTIME = random.randint(1,500)
            return True

    def act_Delay(self):
        if self.computerActDelay != 1000:
            self.computerActDelay += 1
        else:
            self.computerActDelay = 0
            return True
    ##########################


    def create_units_build_plan(self):
        if self.WarFactory != None:
            if self.build_Delay():
                for x in range(5):
                    unitType = random.choice(self.aviableUnits)
                    unitToBuild = GameUnit(self.root,unitType,"Enemy",self,self.combatTeams).create_unit()
                    self.buildUnitsQueue.append(unitToBuild)
                self.combatTeams += 1
                pass

# Można dodać sprawdzanie żeby nie stawiał budynków zaraz przy sobie

    def execute_build_plan(self):
        if self.computerBuildingQueue:
            for building in self.computerBuildingQueue.copy():
                buildingType,buildingInitMatrix = building[0],building[1]
                currentBuilding = Building(self.root,"Enemy",self,buildingType)
                currentBuilding.add_to_game()
                spotArea = []
                for y in range(currentBuilding.matrixSize[0]):
                    for x in range(currentBuilding.matrixSize[1]):
                        spotArea.append([buildingInitMatrix[0] - y, buildingInitMatrix[1] + x])

                currentBuilding.fullMatrixPosition = spotArea
                currentBuilding.matrixPosition = currentBuilding.fullMatrixPosition[0]
                matrixPos = currentBuilding.fullMatrixPosition[0]
                posX,posY = self.root.gameMapMatrix[matrixPos[0]][matrixPos[1]][0]+self.root.positionX,self.root.gameMapMatrix[matrixPos[0]][matrixPos[1]][1]+self.root.positionY
                currentBuilding.pos = (posX,posY)
                currentBuilding.mark_position_as_used()
                currentBuilding.add_on_minimap()

                self.root.building_add_index += 1
                self.root.add_widget(currentBuilding, index=self.root.building_add_index)
                self.root.onMapObjectsToShift.append(currentBuilding)
                self.root.buildings.append(currentBuilding)
                self.root.ids["SidePanelWidget"].index = 0

                if currentBuilding.buildingType == "Rafinery":
                    currentBuilding.add_uranMiner()

                self.computerBuildingQueue.pop(0)



    def execute_Computer_Play(self):
        self.execute_units_build_queue()



    def execute_units_build_queue(self):
        if self.build_Delay():
            if self.root.humanPlayer.units:
                if len(self.units) % 5 == 0 and len(self.units) < self.playerMaxUnitsCount:
                    unitType = random.randint(1,100)
                    if unitType % 6 == 0:
                        unitType = ["RocketLauncher",2500]
                    else:
                        unitType = ["Tank",650]
                    if self.WarFactory != None and self.money >= 5*unitType[1]:
                        for x in range(5):
                            currentUnit = GameUnit(self.root,unitType[0],"Enemy",self,self.combatTeams).create_unit()
                            currentUnit.color = (1,0,0)
                            currentUnit.build_unit_in_factory()
                    self.combatTeams += 1

    def update_money(self):
        self.root.ids["Money_labelComp"].text = str(self.money)




