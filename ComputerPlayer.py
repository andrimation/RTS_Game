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
        self.money = 15_000

        self.computerBuildDelay = 0
        self.computerBuildDelayTIME = 0
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
            return True

    def act_Delay(self):
        if self.computerActDelay != 1000:
            self.computerActDelay += 1
        else:
            self.computerActDelay = 0
            return True
    ##########################


    def create_units_build_plan(self):
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

                currentBuilding.matrixPosition = spotArea
                currentBuilding.originMatrix = currentBuilding.matrixPosition[0]
                matrixPos = currentBuilding.matrixPosition[0]
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
        # Build tasks
        self.execute_units_build_queue()
        # self.attack_human()

        # Zrobić jakoś tak, żeby nie za jednym razem wydawał rozkazy wszystkim, ale żeby za 1 razem 1 grupie, za 2 razem drugiej grupie itp.
        # if self.attackCounter == 100:
        #     self.attack_human()
        #     self.attackCounter = 0
        # else:
        #     self.attackCounter += 1
        #
        # # Attack/defend tasks
        # pass

    def execute_units_build_queue(self):
        if self.root.humanPlayer.units:
            if len(self.units) % 5 == 0 and len(self.units) < self.playerMaxUnitsCount:
                for x in range(5):
                    if self.WarFactory != None:
                        unitType = random.choice(self.aviableUnits)
                        currentUnit = GameUnit(self.root,unitType,"Enemy",self,self.combatTeams).create_unit()
                        currentUnit.build_unit_in_factory()
                # self.attack_human()
                self.combatTeams += 1

    def update_money(self):
        self.root.ids["Money_labelComp"].text = str(self.money)

    def find_attack_target(self,teamNumber):
        if teamNumber in [4,3,2]:
            if self.root.humanPlayer.units:
                target = random.choice(self.root.humanPlayer.units)
                return target
            elif self.root.humanPlayer.buildings:
                target = random.choice(self.root.humanPlayer.buildings)
                return target
        else:
            if self.root.humanPlayer.buildings:
                target = random.choice(self.root.humanPlayer.buildings)
                return target
            elif self.root.humanPlayer.units:
                target = random.choice(self.root.humanPlayer.units)
                return target


    # def attack_human(self):
    #     # plan jest taki - jest 5 teamów, 3 atakują najpierw rocket launchery i tanki ( min 1 rocket launchery, pozostałe 2 losowo ), 2 atakują najpierw budynki.
    #     targets = []
    #     if self.root.humanPlayer.units:
    #         target = self.find_attack_target(4)
    #         for unit in self.units:
    #             if unit.combatTeam == 4 and unit.target == []:
    #                 unit.target = target
    #                 self.root.orders_destinations.append([unit, target.matrixPosition, "Attack", target])
    #                 self.root.updateGameMatrix()
    #                 print("dodaje")


        pass