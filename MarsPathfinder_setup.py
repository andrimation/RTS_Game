import gc
import random
import numpy
# Czyli tak najpierw ustalić położenie początkowe -> tzn x, y mojej pozycji.
# -> a czyli po prostu sprawdzamy czy jak odejmiemy -1 do x, i albo -1 y, to czy wyjdzie liczba mniej niż zero.
# to wtedy pomijamy

# dalej -> bierzemy wszystkich sąsiadów naszego pola -> obliczamy który jest najbardziej w stronę celu i
# dodajemy sąsiadów do listy -> najbliższy idzie jako pierwszy, i rekurencyjnie wywołujemy funkcję dla
# najbliższego. Pól niedostępnych, oznaczonych jako A nie odwiedzamy. Jeśli dojdziemy do K to przerywamy działanie
# funkcji.



class position():
    def __init__(self,pos,previous_position=None):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.previous_position = previous_position

        self.steps = 0
        self.name  = "position"

    def __eq__(self, other):
        return self.pos == other.pos


def convertMap(gameMatrix):
    convertedMap = []
    for line in gameMatrix:
        newLine = []
        for point in line:
            if point[2] == None:
                newLine.append("")
            elif len(point) >= 4:
                if point[3] == "Target":
                    newLine.append(1)
            else:
                newLine.append(1)
        convertedMap.append(newLine)
    convertedMap = numpy.array(convertedMap, dtype=object)
    convertedMap = numpy.array(convertedMap)
    return convertedMap


# Poprawić, żeby szukało najbliższego wolnego po spirali, nie w gwiazdkę
def find_Closesd_Free(gameMatrix,endPosition):
    results = []
    n = 10
    while len(results) < 10:
        for x in range(-n,n):
            q = random.choice([-1,1])
            x *= q
            for y in range(-n,n):
                q = random.choice([-1, 1])
                y *= q
                try:
                    if (endPosition[0] + x >= 0) and (endPosition[1] + y >= 0) and (endPosition[0] + x < len(gameMatrix)-1) and (endPosition[1] + y < len(gameMatrix[0])-1):
                        if gameMatrix[endPosition[0] + x][endPosition[1] + y] != 1:
                            results.append([endPosition[0]+x,endPosition[1]+y])
                except:
                    pass

    results.sort(key= lambda x: abs(x[0]-endPosition[0])+abs(x[1]-endPosition[1]))
    results = results[:5]
    random.shuffle(results)
    return results[0]

def find_Closesd_Free_NoRandom(gameMatrix,endPosition):
    results = []
    n = 15
    while len(results) < 30:
        for x in range(-n,n):
            for y in range(-n,n):
                if endPosition[0] + x >= 0 and endPosition[1] + y >= 0 and endPosition[0] + x < len(gameMatrix) and endPosition[1] + y < len(gameMatrix[0]):
                    if gameMatrix[endPosition[0] + x][endPosition[1] + y] != 1:
                        results.append([endPosition[0]+x,endPosition[1]+y])
                        # print(gameMatrix[endPosition[0] + x][endPosition[1] + y])
    results.sort(key= lambda x: abs(x[0]-endPosition[0])+abs(x[1]-endPosition[1]))
    return results[0]


def marsPathfinder(startPosition,endPosition,mapMatrix,moveType):


    startNode = position(startPosition)
    startNode.name = "start"
    endNode   = position(endPosition)
    endNode.name = "end"

    openList   = [startNode]
    closedList = []
    counter = 0
    counterMaxValue = 100
    if moveType == "Attack":
        counterMaxValue = 50
    while openList:
        counter += 1
        try:
            openList.sort(key= lambda node: abs(node.x-endNode.x)+abs(node.y-endNode.y) + node.steps)
        except:
            pass
        currentNode = openList[0]
        if currentNode == endNode:
            currentNode.name = "end"
            currentNode.previous_position = closedList[-1]
            closedList.append(currentNode)
            answer = find_answer_path(closedList)
            answer.reverse()
            return answer
        if counter > counterMaxValue:  # Przekazać do pathfindera info czy to atak -> jeśli atak to zmniejszyć czas auto wylączenia
            # print("awaryjne wyłączrenie pathfindera")
            return None
        openList.remove(currentNode)
        closedList.append(currentNode)

        # If a is near position -> ignore slant (skos) moves
        checkA = False
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if currentNode.x + x >= 0 and currentNode.y + y >= 0 and currentNode.x + x < len(mapMatrix) and currentNode.y + y < len(mapMatrix[0]):
                    if mapMatrix[currentNode.x+x][currentNode.y+y] == 1:
                        checkA = True
        if checkA:
            for x in [-1, 0, 1]:
                y = 0
                if currentNode.x + x >= 0 and currentNode.y + y >= 0 and currentNode.x + x < len(mapMatrix) and currentNode.y + y < len(mapMatrix[0]):
                    child_of_currentNode = position([currentNode.x+x,currentNode.y+y],previous_position=currentNode)
                    child_of_currentNode.steps = currentNode.steps + 1
                    if child_of_currentNode not in openList and mapMatrix[child_of_currentNode.x][child_of_currentNode.y] != 1 and child_of_currentNode not in closedList:
                        openList.append(child_of_currentNode)
                    else:
                        continue
            for y in [-1,0,1]:
                x = 0
                if currentNode.x + x >= 0 and currentNode.y + y >= 0 and currentNode.x + x < len(mapMatrix) and currentNode.y + y < len(mapMatrix[0]):
                    child_of_currentNode = position([currentNode.x+x,currentNode.y+y],previous_position=currentNode)
                    child_of_currentNode.steps = currentNode.steps + 1
                    if child_of_currentNode not in openList and mapMatrix[child_of_currentNode.x][child_of_currentNode.y] != 1 and child_of_currentNode not in closedList:
                        openList.append(child_of_currentNode)
                    else:
                        continue

        else:
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if currentNode.x + x >= 0 and currentNode.y + y >= 0 and currentNode.x + x < len(mapMatrix) and currentNode.y + y < len(mapMatrix[0]):
                        child_of_currentNode = position([currentNode.x+x,currentNode.y+y],previous_position=currentNode)
                        child_of_currentNode.steps = currentNode.steps + 1
                        if child_of_currentNode not in openList and mapMatrix[child_of_currentNode.x][child_of_currentNode.y] != 1 and child_of_currentNode not in closedList:
                            openList.append(child_of_currentNode)
                        else:
                            continue


# -> zaczynam wyznaczanie ścieżki od końcowego punktu -> "end"
def find_answer_path(pathAnswer):
    finalPath = []


    for position in pathAnswer:
        if position.name == "end":
            endPosition = position
            pathAnswer.pop(pathAnswer.index(endPosition))
            finalPath.append(endPosition)
    while True:
        for position in pathAnswer:
            if position == finalPath[-1].previous_position:
                prevPos = position
                pathAnswer.pop(pathAnswer.index(prevPos))
                finalPath.append(prevPos)
                if finalPath[-1].name == "start":
                    finalPathXY = []
                    for position in finalPath:
                        finalPathXY.append(position.pos)
                    return finalPathXY


    return finalPath
