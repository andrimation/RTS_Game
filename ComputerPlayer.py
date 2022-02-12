
class ComputerPlayer():
    def __init__(self,root):
        self.root = root
        self.money = 10_000

        self.aviableEnergy = 0
        self.buildUnitsQueue = []


    def execute_build_queue(self):
        if self.buildUnitsQueue:
            currentUnit = self.buildUnitsQueue[0]
            if currentUnit.wait != currentUnit.buildTime:
                currentUnit.wait += 1
            else:
                self.buildUnitsQueue.remove(currentUnit)
                currentUnit.build_unit_in_factory()