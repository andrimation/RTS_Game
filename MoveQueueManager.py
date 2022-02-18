import MarsPathfinder_setup
import math

class MoveQueueManager():
    def __init__(self,root):
        self.root = root

    def compute_paths_for_orders(self):
        usedCoords = []
        for destination in self.root.orders_destinations:
            usedCoords.append(destination[1])

        for order_destination in self.root.orders_destinations:
            unitInMove, matrixDestination, moveType, moveTarget = order_destination
            if usedCoords.count(matrixDestination) > 1:
                matrixDestination = MarsPathfinder_setup.find_Closesd_Free(self.root.numpyMapMatrix, order_destination[1])
            try:
                computePath = MarsPathfinder_setup.marsPathfinder(unitInMove.matrixPosition, matrixDestination,self.root.numpyMapMatrix)
                current_order = [unitInMove, matrixDestination, computePath, moveType, moveTarget, ""]
                unitInMove.moveEndPosition = computePath[-1]
            except:
                # self.orders_destinations.remove(order_destination)  # To mogę usunąć, to jednostki będą ruszać nawet jeśli jch jest wiele w jednym miejscu.
                self.root.updateGameMatrix()
                continue

            if computePath != None:
                self.root.orders_destinations.remove(order_destination)
                # Remove old order if object got new during old
                for order in self.root.move_queue:
                    try:
                        if order[0] == current_order[0]:
                            self.root.move_queue.remove(order)
                    except:
                        pass
                try:
                    self.root.move_queue.append(current_order)
                except:
                    pass

    def execute_units_movement(self):
        # Avoid updating minimap in every step
        self.root.miniMapCounter += 1
        refreshMinimap = False
        if self.root.miniMapCounter == 30:
            refreshMinimap = True
            self.root.miniMapCounter = 0

        # Execute move queue
        for order in self.root.move_queue:
            unitInMove, matrixDestination, matrixPath, moveType, moveTarget = order[0], order[1], order[2], order[3],order[4]
            if refreshMinimap:
                unitInMove.updade_minimapPos()
            if moveType == "Move":
                unitInMove.attack = False
                unitInMove.target = []

            if matrixPath and unitInMove.moveX == 0 and unitInMove.moveY == 0:
                try:
                    currentPosition = matrixPath.pop(0)
                except:
                    continue
                if matrixPath:
                    newPosition = matrixPath[0]
                    if self.root.gameMapMatrix[newPosition[0]][newPosition[1]][2] == True:
                        self.root.updateGameMatrix()
                        computePath = MarsPathfinder_setup.marsPathfinder(unitInMove.matrixPosition,matrixPath[-1],self.root.numpyMapMatrix)
                        matrixPath = computePath
                        continue

                    if currentPosition[1] < newPosition[1]:
                        unitInMove.moveX = 60
                    if currentPosition[1] > newPosition[1]:
                        unitInMove.moveX = -60
                    if currentPosition[0] < newPosition[0]:
                        unitInMove.moveY = -60
                    if currentPosition[0] > newPosition[0]:
                        unitInMove.moveY = 60
                    try:
                        self.root.gameMapMatrix[currentPosition[0]][currentPosition[1]][2] = None
                        unitInMove.matrixPosition = newPosition
                        self.root.gameMapMatrix[unitInMove.matrixPosition[0]][unitInMove.matrixPosition[1]][2] = True
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
        # Remove object from move queue if order finished
        for order in self.root.move_queue:
            if matrixDestination == unitInMove.matrixPosition or matrixPath == []:
                try:
                    self.root.move_queue.remove(order)
                except:
                    pass