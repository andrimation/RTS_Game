import MarsPathfinder_setup
import math
import copy
import GameUnit
from UranMiner import UranMiner
from Building import Building

class MoveQueueManager():
    def __init__(self,root):
        self.root = root

    def check_destination_cell(self,destination,unitInMove):
        """Function checks if destination is duplicated in orders_destinations, in move_queue and if position is free
            - function returns new destination if cell is duplicated or not-free, or returns destination"""

        if isinstance(unitInMove,UranMiner):
            return destination
        cellOccurCounter = 0
        allDestinations = set()
        for order_destination in self.root.orders_destinations:
            allDestinations.add(tuple(order_destination[1]))
            if order_destination[1] == destination:
                cellOccurCounter += 1
        for order in self.root.move_queue:
            allDestinations.add(tuple(order[1]))
            if order[1] == destination:
                cellOccurCounter += 1
        for unit in self.root.movableObjects:
            if unit.matrixPosition == destination:
                cellOccurCounter += 1

        if cellOccurCounter == 0:
            return destination
        else:
            new_destination = MarsPathfinder_setup.find_Closesd_Free(self.root.numpyMapMatrix,destination)
            while tuple(new_destination) in destination:
                new_destination = MarsPathfinder_setup.find_Closesd_Free(self.root.numpyMapMatrix, destination)
            return new_destination

    def check_order_remove(self,destination):
        """Function removes orders that probably cannot be executed because of crowd in distance area
            - it checks if square around destination cell is used by objects in specified percentage"""
        absUnitDistance     = 5
        searchSquareMaxSize = 6
        percentageOfUsedCells = 0.5

        allCellsCount  = 0
        usedCellsCount = 0
        y = destination[0]
        x = destination[1]

        # Check square max-size
        if y > searchSquareMaxSize:
            yRangeStart = y-searchSquareMaxSize
        else:
            yRangeStart = 0
        if x > searchSquareMaxSize:
            xRangeStart = x-searchSquareMaxSize
        else:
            xRangeStart = 0

        if y + searchSquareMaxSize > len(self.root.numpyMapMatrix):
            yRangeStop = len(self.root.numpyMapMatrix)
        else:
            yRangeStop = y + searchSquareMaxSize

        if x + searchSquareMaxSize > len(self.root.numpyMapMatrix[0]):
            xRangeStop  = len(self.root.numpyMapMatrix[0])
        else:
            xRangeStop  = x + searchSquareMaxSize

        for yLine in range(yRangeStart,yRangeStop):
            for xLine in range(xRangeStart,xRangeStop):
                allCellsCount += 1
                if self.root.numpyMapMatrix[yLine][xLine] == 1:
                    usedCellsCount += 1

        if allCellsCount/usedCellsCount > percentageOfUsedCells:
            return True
        else:
            return False

    def compute_paths_for_orders(self):
        if self.root.orders_destinations:
            order_destination = self.root.orders_destinations.pop(0)
            unit = order_destination[0]
            destination = self.check_destination_cell(order_destination[1],unit)
            move_type = order_destination[2]
            move_target = order_destination[3]
            move_targetFirstPos = order_destination[4]


            try:
                computePath = MarsPathfinder_setup.marsPathfinder(unit.matrixPosition,destination,self.root.numpyMapMatrix,move_type)
                current_order = [unit,destination, computePath, move_type,move_target, move_targetFirstPos]
                unit.moveEndPosition = destination
            except:
                self.root.updateGameMatrix()
                computePath = None

            # Normal order case
            if computePath != None:
                # Remove old order if object got new during old
                for order in self.root.move_queue:
                    if order[0] == current_order[0]:
                        self.root.move_queue.remove(order)
                self.root.move_queue.append(current_order)
                unit.attack = False
                return

            if computePath == None:
                if (math.dist(unit.matrixPosition, destination) <= 7 and self.check_order_remove(destination)
                    and not isinstance(unit,UranMiner)) and move_type == "Move":
                    try:
                        self.root.orders_destinations.remove(order_destination)
                        unit.movePending = False
                    except:
                        pass
                else:
                    self.root.orders_destinations.append(order_destination)

    def execute_units_movement(self):
        # Avoid updating minimap in every step
        self.root.miniMapCounter += 1
        refreshMinimap = False
        if self.root.miniMapCounter == 30:
            refreshMinimap = True
            self.root.miniMapCounter = 0

        for order in self.root.move_queue:
            unitInMove, matrixDestination,matrixPath,moveType,moveTarget,moveTargetFirstPosition = order
            if isinstance(unitInMove,Building):
                continue
            if refreshMinimap:
                unitInMove.updade_minimapPos()
            if unitInMove.attack == True:
                continue
            if matrixPath == None and unitInMove.moveX == 0 and unitInMove.moveY == 0:
                if moveType == "Move":
                    self.root.orders_destinations.append([unitInMove,matrixDestination,moveType,moveTarget,None])
                elif moveType == "Attack":
                    unitInMove.attack = False
                    self.root.orders_destinations.append([unitInMove,moveTarget.matrixPosition,
                                                          moveType,moveTarget,list(moveTarget.matrixPosition.copy())])
                self.root.move_queue.remove(order)
                continue
            if moveType == "Move":
                unitInMove.attack = False
                unitInMove.target = []
            if moveType == "Attack":
                if moveTarget.matrixPosition != moveTargetFirstPosition and unitInMove.moveX == 0 and unitInMove.moveY == 0:
                    unitInMove.wait += 1
                    if unitInMove.wait == 50:
                        unitInMove.attack = False
                        self.root.orders_destinations.append([unitInMove, moveTarget.matrixPosition,
                                                              moveType, moveTarget,list(moveTarget.matrixPosition.copy())])
                        self.root.move_queue.remove(order)
                        unitInMove.wait = 0
                        continue
                    else:
                        pass

            if matrixPath and unitInMove.moveX == 0 and unitInMove.moveY == 0:
                try:
                    currentPosition = matrixPath[0]
                except:
                    continue
                if matrixPath and len(matrixPath) >= 2:
                    newPosition = matrixPath[1]

                    # Colission -> next cell taken
                    if self.root.numpyMapMatrix[newPosition[0]][newPosition[1]] == 1:
                        if (math.dist(matrixPath[0],matrixDestination) <= 7 and self.check_order_remove(matrixDestination)
                                and not isinstance(unitInMove,UranMiner) and moveType == "Move"):
                            for destination in self.root.orders_destinations:
                                if destination[0] == unitInMove:
                                    self.root.orders_destinations.remove(destination)
                            self.root.move_queue.remove(order)
                            continue
                        else:
                            self.root.orders_destinations.append([unitInMove,matrixDestination,moveType,moveTarget,moveTargetFirstPosition])
                            self.root.move_queue.remove(order)
                            continue

                    currentPosition = matrixPath.pop(0)
                    if currentPosition[1] < newPosition[1]:
                        unitInMove.moveX = 60
                    if currentPosition[1] > newPosition[1]:
                        unitInMove.moveX = -60
                    if currentPosition[0] < newPosition[0]:
                        unitInMove.moveY = -60
                    if currentPosition[0] > newPosition[0]:
                        unitInMove.moveY = 60
                    try:
                        self.root.numpyMapMatrix[currentPosition[0]][currentPosition[1]] = 0
                        unitInMove.matrixPosition = newPosition
                        self.root.numpyMapMatrix[unitInMove.matrixPosition[0]][unitInMove.matrixPosition[1]] = 1
                    except:
                        pass
                else:
                    unitInMove.matrixPosition = currentPosition

            if unitInMove.moveX > 0:
                unitInMove.x += 2
                unitInMove.moveX -= 2
            elif unitInMove.moveX < 0:
                unitInMove.x -= 2
                unitInMove.moveX += 2
            else:
                pass

            if unitInMove.moveY > 0:
                unitInMove.y += 2
                unitInMove.moveY -= 2
            elif unitInMove.moveY < 0:
                unitInMove.y -= 2
                unitInMove.moveY += 2
            else:
                pass

        for order in self.root.move_queue:
            if order[2] == [] and order[3] == "Move":
                unitInMove.moveX = 0
                unitInMove.moveY = 0
                try:
                    unitInMove.movePending = False
                    self.root.move_queue.remove(order)
                except:
                    pass

    # Tu jest coś zjebane
    def attack(self):
        for order in self.root.move_queue:
            if order[3] == "Attack" and order[4] != None and order[4] != []:
                object = order[0]
                target = order[4]
                objectMatrixPos = object.matrixPosition
                if isinstance(object,Building):
                    objectMatrixPos = object.matrixPosition[0]


                if math.dist(objectMatrixPos,target.matrixPosition) < object.shotDistance and object.moveX == 0 and object.moveY == 0:
                    self.root.numpyMapMatrix[objectMatrixPos[0]][object.matrixPosition[1]] = 1
                    object.attack = True
                    object.target = target
                else:
                    object.attack = False
                    object.target = []
                    continue

                if object.attack == True:
                    if object.reloadCounter == object.reloadTime:
                        self.root.make_bullet(object, object.target)
                        object.reloadCounter = 0
                    else:
                        object.reloadCounter += 1
                    if  object.target.health <= 0:# Też musze usunąć order jednostki która zginęła !!
                        object.target.remove_unit()
                        object.attack = False
                        object.target = []
                        # prawdopodobnie zbędne


    def computer_attack(self):
        for order in self.root.move_queue:
            if order[0].player == self.root.computerPlayer and (order[2] == None or order[2] == []):
                target = self.root.computerPlayer.find_attack_target(order[0].combatTeam)
                for unit in self.root.computerPlayer.units:
                    if unit.combatTeam == order[0].combatTeam:
                        self.root.orders_destinations.append([unit, target.matrixPosition, "Attack", target])



