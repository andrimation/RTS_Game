import math,time


testPathMap = [
    ["","","","","","","","","","","","","","K",],
    ["","","","","","","","","","","","","","",],
    ["","","A","A","A","","","","","","","","","",],
    ["","","","","A","A","","","","","","","","",],
    ["","","","","","A","A","A","","","","","","",],
    ["","","","","","","","A","A","","","","","",],
    ["","","","","","","","","A","A","","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["P","","","","","","","","","","","","","",],
]
print(len(testPathMap))
print(len(testPathMap[0]))

# Czyli tak najpierw ustalić położenie początkowe -> tzn x, y mojej pozycji.
# -> a czyli po prostu sprawdzamy czy jak odejmiemy -1 do x, i albo -1 y, to czy wyjdzie liczba mniej niż zero.
# to wtedy pomijamy

# dalej -> bierzemy wszystkich sąsiadów naszego pola -> obliczamy który jest najbardziej w stronę celu i
# dodajemy sąsiadów do listy -> najbliższy idzie jako pierwszy, i rekurencyjnie wywołujemy funkcję dla
# najbliższego. Pól niedostępnych, oznaczonych jako A nie odwiedzamy. Jeśli dojdziemy do K to przerywamy działanie
# funkcji.

class Node():
    def __init__(self,position=None,parent=None,endNode=[0,0]):
        self.position = position
        self.parent   = parent
        self.endNode  = endNode

        self.g = 0   # Distance between current and start
        self.h = self.heuristic()   # Estimated distance between curent and end
        self.f = self.g + self.h

    def heuristic(self):
        if self.position != Node:
            result = abs(self.position[0] - self.endNode[0]) + abs(self.position[1]-self.endNode[1])
            return result
        else:
            return 0

    def __eq__(self, other):
        return self.position == other.position


def marsPathfinder(startPoint:list,endPoint:list,mapMatrix:list):
    startNode = Node(startPoint,None,endPoint)
    startNode.f = startNode.g = startNode.h = 0

    endNode = Node(endPoint,None,endPoint)

    openList = [Node(startPoint, endNode=endPoint)]
    closedList = []

    while openList:
        openList.sort(key= lambda x: x.f)
        currentNode = openList.pop(0)
        closedList.append(currentNode)

        if currentNode == endNode:
            return closedList

        children = []
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                if currentNode.position[0] + x >= 0 and currentNode.position[1] + y >= 0 and currentNode.position[0] + x < len(mapMatrix) and currentNode.position[1] + y < len(mapMatrix[0]):
                    if mapMatrix[currentNode.position[0]+x][currentNode.position[1]+y] != "A":
                        child_Node = Node([currentNode.position[0]+x,currentNode.position[1]+y],currentNode,endPoint)
                        children.append(child_Node)

        for child in children:
            child.g = currentNode.g + 1
            childChecker = False
            for list_child in openList:
                print()
                if child == list_child:
                    if child.g > list_child.g:
                        childChecker = True
            if not childChecker:
                openList.append(child)






    return closedList


# # Detect neighbours
    # for x in [-1,0,1]:
    #     for y in [-1,0,1]:
    #         if startX + x >= 0 and startY + y >= 0 and startX + x < len(mapMatrix) and startY+y < len(mapMatrix[0]):
    #             if mapMatrix[startX+x][startY+y] == "K":
    #                 time.sleep(1)
    #                 print("K")
    #                 return answer
    #             if mapMatrix[startX+x][startY+y] != "A" and mapMatrix[startX+x][startY+y] != "Q" and mapMatrix[startX+x][startY+y] != "B" and mapMatrix[startX+x][startY+y] != "K" :
    #                 if [startX + x, startY + y] not in candidates:
    #                     print(startX+x,startY+y)
    #                     mapMatrix[startX+x][startY+y] = "Q"
    #
    #                     candidates.append([startX+x,startY+y])
    # # Sort list by distances
    # candidates.sort(key= lambda x: math.sqrt((x[0]-endX)**2 + (x[1]-endY)**2))
    # mapMatrix[candidates[0][0]][candidates[0][1]] = "B"
    # answer.append([candidates[0][0],candidates[0][1]])
    # # time.sleep(0.25)
    # for x in mapMatrix:
    #     print(x)
    # for point in candidates:
    #     new_start = candidates.pop(0)
    #     print(candidates)
    #     return  marsPathfinder(new_start,endPoint,mapMatrix,candidates,answer)
    #
    # return answer
    #
    #
    #
    #
    #


path = marsPathfinder([11,0],[0,13],testPathMap)
print(path)

testPathMap = [
    ["","","","","","","","","","","","","","K",],
    ["","","","","","","","","","","","","","",],
    ["","","A","A","A","","","","","","","","","",],
    ["","","","","A","A","","","","","","","","",],
    ["","","","","","A","A","A","","","","","","",],
    ["","","","","","","","A","A","","","","","",],
    ["","","","","","","","","A","A","","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["P","","","","","","","","","","","","","",],
]

for point in path:
    testPathMap[point.position[0]][point.position[1]] = "B"

for x in testPathMap:
    print(x)