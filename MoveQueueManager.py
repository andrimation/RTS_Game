# import MarsPathfinder_setup
# import math
# import copy
# import GameUnit
#
# class MoveQueueManager():
#     def __init__(self,root):
#         self.root = root
#
#     def compute_paths_for_orders(self):
#         usedCoords = []
#         for destination in self.root.orders_destinations:
#             usedCoords.append(destination[1])
#
#         for order_destination in self.root.orders_destinations:
#             unitInMove, matrixDestination, moveType, moveTarget, targetFirstPosition = order_destination
#
#             if usedCoords.count(matrixDestination) >= 1:
#                 matrixDestination = MarsPathfinder_setup.find_Closesd_Free(self.root.numpyMapMatrix, order_destination[1])
#                 order_destination[1] = matrixDestination
#             try:
#                 computePath = MarsPathfinder_setup.marsPathfinder(unitInMove.matrixPosition,[order_destination[1][0], order_destination[1][1]],self.root.numpyMapMatrix,moveType)
#                 current_order = [unitInMove,(order_destination[1][0], order_destination[1][1]), computePath, moveType, moveTarget,targetFirstPosition]
#                 unitInMove.moveEndPosition = computePath[-1]
#             except:
#                 self.root.updateGameMatrix()
#                 continue
#
#             if computePath != None and computePath != []:
#                 self.root.orders_destinations.remove(order_destination)
#                 # Remove old order if object got new during old
#                 for order in self.root.move_queue:
#                     if order[0] == current_order[0]:
#                         self.root.move_queue.remove(order)
#
#                 self.root.move_queue.append(current_order)
#
#     def execute_units_movement(self):
#         # Avoid updating minimap in every step
#         self.root.miniMapCounter += 1
#         refreshMinimap = False
#         if self.root.miniMapCounter == 30:
#             refreshMinimap = True
#             self.root.miniMapCounter = 0
#
#         # Execute move queue   - nie odejmuje mi ruchów które zostały wykonane, tylko wciąż sa w move queue
#         for order in self.root.move_queue:
#             unitInMove, matrixDestination,matrixPath,moveType,moveTarget,moveTargetFirstPosition = order
#
#             if refreshMinimap:
#                 unitInMove.updade_minimapPos()
#             if unitInMove.attack == True:
#                 continue
#             if matrixPath == None and unitInMove.moveX == 0 and unitInMove.moveY == 0:
#                 if moveType == "Move":
#                     self.root.orders_destinations.append([unitInMove,matrixDestination,moveType,moveTarget,None])
#                 elif moveType == "Attack":
#                     unitInMove.attack = False
#                     self.root.orders_destinations.append([unitInMove,moveTarget.matrixPosition,moveType,moveTarget,list(moveTarget.matrixPosition.copy())])
#                     self.root.move_queue.remove(order)
#                 continue
#             if moveType == "Move":
#                 unitInMove.attack = False
#                 unitInMove.target = []
#             if moveType == "Attack":
#                 if moveTarget.matrixPosition != moveTargetFirstPosition and unitInMove.moveX == 0 and unitInMove.moveY == 0:
#                     unitInMove.wait += 1
#                     if unitInMove.wait == 50:
#                         unitInMove.attack = False
#                         self.root.orders_destinations.append([unitInMove, moveTarget.matrixPosition, moveType, moveTarget,list(moveTarget.matrixPosition.copy())])
#                         self.root.move_queue.remove(order)
#                         unitInMove.wait = 0
#                         continue
#                     else:
#                         pass
#
#
#             if matrixPath and unitInMove.moveX == 0 and unitInMove.moveY == 0:
#                 try:
#                     currentPosition = matrixPath[0]
#                 except:
#                     continue
#                 if matrixPath and len(matrixPath) >= 2:
#                     newPosition = matrixPath[1]
#                     if self.root.numpyMapMatrix[newPosition[0]][newPosition[1]] == 1:
#                         self.root.move_queue.remove(order)
#                         self.root.orders_destinations.append([unitInMove,matrixDestination,moveType,moveTarget,moveTargetFirstPosition])
#                         continue
#                     currentPosition = matrixPath.pop(0)
#                     if currentPosition[1] < newPosition[1]:
#                         unitInMove.moveX = 60
#                     if currentPosition[1] > newPosition[1]:
#                         unitInMove.moveX = -60
#                     if currentPosition[0] < newPosition[0]:
#                         unitInMove.moveY = -60
#                     if currentPosition[0] > newPosition[0]:
#                         unitInMove.moveY = 60
#
#                     self.root.numpyMapMatrix[currentPosition[0]][currentPosition[1]] = 0
#                     unitInMove.matrixPosition = newPosition
#                     self.root.numpyMapMatrix[unitInMove.matrixPosition[0]][unitInMove.matrixPosition[1]] = 1
#
#                 else:
#                     unitInMove.matrixPosition = currentPosition
#
#             if unitInMove.moveX > 0:
#                 unitInMove.x += 2
#                 unitInMove.moveX -= 2
#             elif unitInMove.moveX < 0:
#                 unitInMove.x -= 2
#                 unitInMove.moveX += 2
#             else:
#                 pass
#
#             if unitInMove.moveY > 0:
#                 unitInMove.y += 2
#                 unitInMove.moveY -= 2
#             elif unitInMove.moveY < 0:
#                 unitInMove.y -= 2
#                 unitInMove.moveY += 2
#             else:
#                 pass
#         # Remove object from move queue if order finished
#         for order in self.root.move_queue:
#             if order[0].matrixPosition == order[1] and order[3] == "Move": # ahh tupla != lista !
#                 try:
#                     self.root.move_queue.remove(order)
#                 except:
#                     pass
#
#     # Tu jest coś zjebane
#     def attack(self):
#         for order in self.root.move_queue:
#             if order[3] == "Attack" and order[4] != None and order[4] != []:
#                 object = order[0]
#                 target = order[4]
#                 if math.dist(object.matrixPosition,target.matrixPosition) < object.shotDistance and object.moveX == 0 and object.moveY == 0:
#                     self.root.numpyMapMatrix[object.matrixPosition[0]][object.matrixPosition[1]] = 1
#                     object.attack = True
#                     object.target = target
#                 else:
#                     object.attack = False
#                     object.target = []
#                     continue
#
#                 if object.attack == True:
#                     if object.reloadCounter == object.reloadTime:
#                         self.root.make_bullet(object, object.target)
#                         object.reloadCounter = 0
#                     else:
#                         object.reloadCounter += 1
#                     if  object.target.health <= 0:# Też musze usunąć order jednostki która zginęła !!
#                         object.target.remove_unit()
#                         object.attack = False
#                         object.target = []
#
#
#
#
#     def computer_attack(self):
#         for order in self.root.move_queue:
#             if order[0].player == self.root.computerPlayer and (order[2] == None or order[2] == []):
#                 target = self.root.computerPlayer.find_attack_target(order[0].combatTeam)
#                 for unit in self.root.computerPlayer.units:
#                     if unit.combatTeam == order[0].combatTeam:
#                         self.root.orders_destinations.append([unit, target.matrixPosition, "Attack", target])
#


import MarsPathfinder_setup
import math
import copy
import GameUnit

class MoveQueueManager():
    def __init__(self,root):
        self.root = root
    # Dobra, moje unity w którymś momencie tracą swój target, kiedy ?  # czasem coś sie dzieje że jednostki mają w chuj dziwne matrix pos (629, 35) np...
    # Zrobić żeby
    def compute_paths_for_orders(self):
        usedCoords = []
        for destination in self.root.orders_destinations:
            usedCoords.append(destination[1])

        for order_destination in self.root.orders_destinations:
            unitInMove, matrixDestination, moveType, moveTarget, targetFirstPosition = order_destination

            if usedCoords.count(matrixDestination) > 1:
                matrixDestination = MarsPathfinder_setup.find_Closesd_Free(self.root.numpyMapMatrix, order_destination[1])
                order_destination[1] = matrixDestination
            try:
                computePath = MarsPathfinder_setup.marsPathfinder(unitInMove.matrixPosition,[order_destination[1][0], order_destination[1][1]],self.root.numpyMapMatrix,moveType)
                current_order = [unitInMove,(order_destination[1][0], order_destination[1][1]), computePath, moveType, moveTarget,targetFirstPosition]
                unitInMove.moveEndPosition = computePath[-1]
            except:
                self.root.updateGameMatrix()
                continue

            if computePath != None and computePath != []:
                # print(current_order)
                # print()
                self.root.orders_destinations.remove(order_destination)
                # Remove old order if object got new during old
                for order in self.root.move_queue:
                    if order[0] == current_order[0]:
                        self.root.move_queue.remove(order)

                self.root.move_queue.append(current_order)

    def execute_units_movement(self):
        # Avoid updating minimap in every step
        self.root.miniMapCounter += 1
        refreshMinimap = False
        if self.root.miniMapCounter == 30:
            refreshMinimap = True
            self.root.miniMapCounter = 0

        # Execute move queue   - nie odejmuje mi ruchów które zostały wykonane, tylko wciąż sa w move queue
        for order in self.root.move_queue:
            unitInMove, matrixDestination,matrixPath,moveType,moveTarget,moveTargetFirstPosition = order
            if refreshMinimap:
                unitInMove.updade_minimapPos()
            if unitInMove.attack == True:
                continue
            if matrixPath == None and unitInMove.moveX == 0 and unitInMove.moveY == 0:
                if moveType == "Move":
                    self.root.orders_destinations.append([unitInMove,matrixDestination,moveType,moveTarget,None])
                elif moveType == "Attack":
                    unitInMove.attack = False
                    self.root.orders_destinations.append([unitInMove,moveTarget.matrixPosition,moveType,moveTarget,list(moveTarget.matrixPosition.copy())])
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
                        self.root.orders_destinations.append([unitInMove, moveTarget.matrixPosition, moveType, moveTarget,list(moveTarget.matrixPosition.copy())])
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
        # -- Rozkminić o co chodzi z tymi tuplami !! Po co one były?
        # Remove object from move queue if order finished
        for order in self.root.move_queue:
            if order[1] == tuple(unitInMove.matrixPosition) and order[3] == "Move": # ahh tupla != lista !
                try:
                    self.root.move_queue.remove(order)
                except:
                    pass

    # Tu jest coś zjebane
    def attack(self):
        for order in self.root.move_queue:
            if order[3] == "Attack" and order[4] != None and order[4] != []:
                object = order[0]
                target = order[4]
                if math.dist(object.matrixPosition,target.matrixPosition) < object.shotDistance and object.moveX == 0 and object.moveY == 0:
                    self.root.numpyMapMatrix[object.matrixPosition[0]][object.matrixPosition[1]] = 1
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
                        try:
                            self.root.move_queue.remove(order)
                        except:
                            pass

    def computer_attack(self):
        for order in self.root.move_queue:
            if order[0].player == self.root.computerPlayer and (order[2] == None or order[2] == []):
                target = self.root.computerPlayer.find_attack_target(order[0].combatTeam)
                for unit in self.root.computerPlayer.units:
                    if unit.combatTeam == order[0].combatTeam:
                        self.root.orders_destinations.append([unit, target.matrixPosition, "Attack", target])



