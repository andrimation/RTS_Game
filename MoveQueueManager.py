import MarsPathfinder_setup
import math
import copy
import GameUnit
from UranMiner import UranMiner
from Building import Building
import GameUnit

import threading

class MoveQueueManager():
    def __init__(self, root):
        self.root = root
        self.threads_counter = 0

    # ABY rozwiązac problem usuwania elementu z listy po której sie iteruje, można użyć wyrażenia listowego !!
    def pathThreads_creator(self):
        if len(self.root.path_compute_threads) < 5:
            if self.root.orders_destinations:
                pathThread = threading.Thread(target=self.compute_paths_for_orders)
                self.root.path_compute_threads.append(pathThread)
                self.root.path_compute_threads[-1].run()

        self.pathThreadsRemove()

    def pathThreadsRemove(self):
        if self.threads_counter == 10:
            self.root.path_compute_threads = [thread for thread in self.root.path_compute_threads if thread.is_alive()]
            self.threads_counter = 0
        else:
            self.threads_counter += 1

    def check_destination_cell(self, destination, unitInMove, move_Type):
        """Function checks if destination is duplicated in orders_destinations, in move_queue and if position is free
            - function returns new destination if cell is duplicated or not-free, or returns destination"""
        if isinstance(unitInMove, UranMiner):
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

        if cellOccurCounter == 0 and move_Type != "Attack":
            return destination
        else:
            new_destination = MarsPathfinder_setup.find_Closesd_Free(self.root.numpyMapMatrix, destination)
            while tuple(new_destination) in destination:
                new_destination = MarsPathfinder_setup.find_Closesd_Free(self.root.numpyMapMatrix, destination)
            return new_destination

    def check_order_remove(self, destination):
        """Function removes orders that probably cannot be executed because of crowd in distance area
            - it checks if square around destination cell is used by objects in specified percentage"""
        absUnitDistance = 5
        searchSquareMaxSize = 6
        percentageOfUsedCells = 0.5

        allCellsCount = 0
        usedCellsCount = 0
        y = destination[0]
        x = destination[1]

        # Check square max-size
        if y > searchSquareMaxSize:
            yRangeStart = y - searchSquareMaxSize
        else:
            yRangeStart = 0
        if x > searchSquareMaxSize:
            xRangeStart = x - searchSquareMaxSize
        else:
            xRangeStart = 0

        if y + searchSquareMaxSize > len(self.root.numpyMapMatrix):
            yRangeStop = len(self.root.numpyMapMatrix)
        else:
            yRangeStop = y + searchSquareMaxSize

        if x + searchSquareMaxSize > len(self.root.numpyMapMatrix[0]):
            xRangeStop = len(self.root.numpyMapMatrix[0])
        else:
            xRangeStop = x + searchSquareMaxSize

        for yLine in range(yRangeStart, yRangeStop):
            for xLine in range(xRangeStart, xRangeStop):
                allCellsCount += 1
                if self.root.numpyMapMatrix[yLine][xLine] == 1:
                    usedCellsCount += 1
        if usedCellsCount == 0:
            usedCellsCount = 1
        if allCellsCount / usedCellsCount > percentageOfUsedCells:
            return True
        else:
            return False

    def compute_paths_for_orders(self):
        if self.root.orders_destinations:
            order_destination = self.root.orders_destinations.pop(0)
            unit = order_destination[0]
            move_type = order_destination[2]
            destination = self.check_destination_cell(order_destination[1], unit, move_type)
            move_target = order_destination[3]
            move_targetFirstPos = order_destination[4]

            if not isinstance(unit, Building):
                try:
                    computePath = MarsPathfinder_setup.marsPathfinder(unit.matrixPosition, destination,
                                                                      self.root.numpyMapMatrix, move_type)
                    current_order = [unit, destination, computePath, move_type, move_target, move_targetFirstPos]
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
                        and not isinstance(unit, UranMiner)) and move_type == "Move":
                        try:
                            self.root.orders_destinations.remove(order_destination)
                            unit.movePending = False
                        except:
                            pass
                    else:
                        self.root.orders_destinations.append(order_destination)

    def execute_units_movement(self):
        # Avoid updating minimap in every step
        # Z jakiegoś powodu nie updejtuje mi wrogich jednostek ?? albo wszystkich, które działają w auto-ataku
        self.root.miniMapCounter += 1
        refreshMinimap = False
        if self.root.miniMapCounter == 30:
            refreshMinimap = True
            self.root.miniMapCounter = 0

        for order in self.root.move_queue:
            unitInMove, matrixDestination, matrixPath, moveType, moveTarget, moveTargetFirstPosition = order
            newPosition = []
            currentPosition = []
            if isinstance(unitInMove, Building):
                continue
            if refreshMinimap:
                unitInMove.updade_minimapPos()
            if unitInMove.attack == True:
                continue
            if matrixPath == None and unitInMove.moveX == 0 and unitInMove.moveY == 0:
                if moveType == "Move":
                    self.root.orders_destinations.append([unitInMove, matrixDestination, moveType, moveTarget, None])
                elif moveType == "Attack":
                    unitInMove.attack = False
                    self.root.orders_destinations.append([unitInMove, moveTarget.matrixPosition,moveType, moveTarget, list(moveTarget.matrixPosition.copy())])
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
                                                              moveType, moveTarget,
                                                              list(moveTarget.matrixPosition.copy())])
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

                    if self.root.numpyMapMatrix[newPosition[0]][newPosition[1]] == 1:
                        if (math.dist(matrixPath[0], matrixDestination) <= 7 and self.check_order_remove(
                                matrixDestination)
                                and not isinstance(unitInMove, UranMiner) and moveType == "Move"):
                            for destination in self.root.orders_destinations:
                                if destination[0] == unitInMove:
                                    self.root.orders_destinations.remove(destination)
                            self.root.move_queue.remove(order)
                            continue
                        else:
                            self.root.orders_destinations.append(
                                [unitInMove, matrixDestination, moveType, moveTarget, moveTargetFirstPosition])
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

            if unitInMove.rotate_finish == False:
                try:
                    self.rotate_unit(unitInMove, currentPosition, newPosition)
                    continue
                except:
                    continue

            if unitInMove.moveX > 0:
                unitInMove.x += unitInMove.speed
                unitInMove.moveX -= unitInMove.speed
            elif unitInMove.moveX < 0:
                unitInMove.x -= unitInMove.speed
                unitInMove.moveX += unitInMove.speed
            else:
                pass

            if unitInMove.moveY > 0:
                unitInMove.y += unitInMove.speed
                unitInMove.moveY -= unitInMove.speed
            elif unitInMove.moveY < 0:
                unitInMove.y -= unitInMove.speed
                unitInMove.moveY += unitInMove.speed
            else:
                pass

            if unitInMove.moveX == 0 and unitInMove.moveY == 0:
                unitInMove.rotate_finish = False

        for order in self.root.move_queue:
            if order[2] == [] and order[3] == "Move":
                unitInMove.moveX = 0
                unitInMove.moveY = 0
                try:
                    unitInMove.movePending = False
                    self.root.move_queue.remove(order)
                except:
                    pass

    # Coś jest zjebane z atakiem - jednostki jakby atakują zlą pozycję targetu ( ale tylko czasem )
    # Rozkminić co sie dzieje jak zaczynają dziać się dziwne rzeczy - dodać button do debuowania, że printuje mi
    # attack tylko jak jest wciśnięty i tylko wybranych jednostek - to się dzieje gdy uciekam jednostkami przed atakiem
    def attack(self):
        # Jednostki wroga mogą atakować swoje unity !
        for order in self.root.move_queue:
            # print(order)
            if order[3] == "Attack" and order[4] != None and order[4] != []:
                object = order[0]
                target = order[4]
                objectMatrixPos = object.matrixPosition
                if isinstance(object, Building):
                    if math.dist(objectMatrixPos, target.matrixPosition) >= object.shotDistance:
                        object.reset_attack()
                        self.root.move_queue.remove(order)
                        continue

                targetMatrixPos = target.matrixPosition


                if math.dist(objectMatrixPos,targetMatrixPos) < object.shotDistance and object.moveX == 0 and object.moveY == 0:
                    self.root.numpyMapMatrix[objectMatrixPos[0]][object.matrixPosition[1]] = 1
                    object.attack = True
                    object.target = target
                else:
                    object.reset_attack()
                    continue

                if object.attack == True:
                    if object.reloadCounter == object.reloadTime:
                        self.root.make_bullet(object, object.target)
                        object.reloadCounter = 0
                    else:
                        object.reloadCounter += 1
                    if object.target.health <= 0:  # Też musze usunąć order jednostki która zginęła !!
                        object.target.remove_object()
                        object.reset_attack()

    # Załadować najpierw wszystkie obrazki do ramu, a dopiero potem obracać !!
    def rotate_unit(self, unit, currentMatrixPosition, newMatrixPosition):

        if unit.rotate_finish == False:
            if unit.angle_to_rotate == 0:
                if newMatrixPosition[0] == currentMatrixPosition[0] and newMatrixPosition[1] > currentMatrixPosition[1]:
                    desiredAngle = 0
                elif newMatrixPosition[0] < currentMatrixPosition[0] and newMatrixPosition[1] > currentMatrixPosition[1]:
                    desiredAngle = 45
                elif newMatrixPosition[0] < currentMatrixPosition[0] and newMatrixPosition[1] == currentMatrixPosition[1]:
                    desiredAngle = 90
                elif newMatrixPosition[0] < currentMatrixPosition[0] and newMatrixPosition[1] < currentMatrixPosition[1]:
                    desiredAngle = 135
                elif newMatrixPosition[0] == currentMatrixPosition[0] and newMatrixPosition[1] < currentMatrixPosition[1]:
                    desiredAngle = 180
                elif newMatrixPosition[0] > currentMatrixPosition[0] and newMatrixPosition[1] < currentMatrixPosition[1]:
                    desiredAngle = 225
                elif newMatrixPosition[0] > currentMatrixPosition[0] and newMatrixPosition[1] == currentMatrixPosition[1]:
                    desiredAngle = 270
                elif newMatrixPosition[0] > currentMatrixPosition[0] and newMatrixPosition[1] > currentMatrixPosition[1]:
                    desiredAngle = 315

                anglePrepare = desiredAngle - unit.angle_
                if anglePrepare > 180:
                    anglePrepare = -1 * ((360 - desiredAngle) + unit.angle_)
                unit.angle_to_rotate = anglePrepare

                if unit.angle_to_rotate == 0:
                    unit.rotate_finish = True

            else:
                if unit.angle_to_rotate > 0:
                    unit.angle_ += 5
                    unit.angle_to_rotate -= 5

                elif unit.angle_to_rotate < 0:
                    unit.angle_ -= 5
                    unit.angle_to_rotate += 5

                unit.set_unit_image()


                if unit.angle_to_rotate > 0:
                    unit.rotate_finish = False
                    return

                elif unit.angle_to_rotate == 0:
                    unit.rotate_finish = True
                    return

