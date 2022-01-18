testPathMap = [
    ["","","","","","","","","","A","","","","K",],
    ["","","","","","","","","","A","","","","",],
    ["","","A","A","A","","","","","","A","","","",],
    ["","","","","A","A","","A","","","","","A","",],
    ["","","","","","A","A","","","","","A","","",],
    ["","","","","","","","A","A","","","","","",],
    ["","","","","","","","","A","A","","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["","","","","","","","","","","A","A","","",],
    ["P","","","","","","","","","","","A","","",],
]
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
            else:
                newLine.append("A")
        convertedMap.append(newLine)
    return convertedMap



def marsPathfinder(startPosition,endPosition,mapMatrix):
    #Debug Matrix
    mapMatrix[startPosition[0]][startPosition[1]] = "S"
    mapMatrix[endPosition[0]][endPosition[1]] = "K"
    for line in mapMatrix:
        print(line)
    #
    startNode = position(startPosition)
    startNode.name = "start"
    endNode   = position(endPosition)
    endNode.name = "end"

    openList   = [startNode]
    closedList = []

    while openList:
        openList.sort(key= lambda node: abs(node.x-endNode.x)+abs(node.y-endNode.y) + node.steps)
        currentNode = openList[0]
        if currentNode == endNode:
            currentNode.name = "end"
            currentNode.previous_position = closedList[-1]
            closedList.append(currentNode)
            answer = find_answer_path(closedList)
            answer.reverse()
            return answer  # tu napisać funkcję zwracającą ostateczną ścieżkę



        openList.remove(currentNode)
        closedList.append(currentNode)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if currentNode.x + x >= 0 and currentNode.y + y >= 0 and currentNode.x + x < len(mapMatrix) and currentNode.y + y < len(mapMatrix[0]):
                    child_of_currentNode = position([currentNode.x+x,currentNode.y+y],previous_position=currentNode)
                    child_of_currentNode.steps = currentNode.steps + 1
                    if child_of_currentNode not in openList and mapMatrix[child_of_currentNode.x][child_of_currentNode.y] != "A" and child_of_currentNode not in closedList:
                        # Wykluczenie skosu
                        try:
                            if mapMatrix[currentNode.x-1][currentNode.y] == "A" and mapMatrix[currentNode.x][currentNode.y+1] == "A":
                                continue
                        except:
                            pass
                        try:
                            if mapMatrix[currentNode.x][currentNode.y+1] == "A" and mapMatrix[currentNode.x+1][currentNode.y] == "A":
                                continue
                        except:
                            pass
                        try:
                            if mapMatrix[currentNode.x][currentNode.y-1] == "A" and mapMatrix[currentNode.x+1][currentNode.y] == "A":
                                continue
                        except:
                            pass
                        try:
                            if mapMatrix[currentNode.x][currentNode.y-1] == "A" and mapMatrix[currentNode.x-1][currentNode.y] == "A":
                                continue
                        except:
                            pass

                        openList.append(child_of_currentNode)
                    else:
                        continue


# -> zaczynamy wyznaczanie ścieżki od końcowego punktu -> "end"
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
