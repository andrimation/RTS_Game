from GameUnit import GameUnit

class HumanPlayer():
    def __init__(self,root):
        self.root = root
        self.money = 100_000
        self.buildings = []

        self.aviableEnergy = 0
        self.buildUnitsQueue = []
        self.MainBase = None
        self.WarFactory = None
        self.units      = []
        self.playerMaxUnitsCount = 25
        self.combatTeams = 0
        self.side = "Friend"


    def execute_build_queue(self):
        if self.buildUnitsQueue:
            currentUnit = self.buildUnitsQueue[0]
            if currentUnit.wait != currentUnit.buildTime:
                currentUnit.wait += 1
            else:
                self.buildUnitsQueue.remove(currentUnit)
                currentUnit.build_unit_in_factory()

    def update_money(self):
        self.root.ids["Money_label"].text = str(self.money)

    def build_unit(self,unitType,side):
        if len(self.units) % 5 == 0 and len(self.units) < self.playerMaxUnitsCount:
            for x in range(5):
                newUnit = GameUnit(self.root,unitType,side,self,self.combatTeams).create_unit()
                if self.money >= newUnit.buildCost:
                    newUnit.add_unit_to_build_queue()
                    self.money -= newUnit.buildCost
                    self.update_money()
            self.combatTeams += 1