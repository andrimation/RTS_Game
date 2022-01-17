testPathMap = [
    ["","","","","","","","","","A","","","","K",],
    ["","","","","","","","","","A","","","","",],
    ["","","A","A","A","","","","","","A","","","",],
    ["","","","","A","A","","","","","","","A","",],
    ["","","","","","A","A","A","","","","A","","",],
    ["","","","","","","","A","A","","","","","",],
    ["","","","","","","","","A","A","","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["","","","","","","","","","","A","A","","",],
    ["P","","","","","","","","","","","A","","",],
]




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



def marsPathfinder(startPosition,endPosition,mapMatrix):

    startNode = position(startPosition)
    startNode.name = "start"
    endNode   = position(endPosition)
    endNode.name = "end"

    openList   = [startNode]
    closedList = []

    while openList:
        openList.sort(key= lambda node: abs(node.x-endNode.x)+abs(node.y-endNode.y) + node.steps)
        currentNode = openList[0]
        print(currentNode.pos)
        if currentNode == endNode:
            currentNode.name = "end"
            currentNode.previous_position = closedList[-1]
            closedList.append(currentNode)
            return closedList  # tu napisać funkcję zwracającą ostateczną ścieżkę
        if mapMatrix[currentNode.x][currentNode.y] == "K":
            currentNode.name = "end"
            currentNode.previous_position = closedList[-1]
            closedList.append(currentNode)
            return closedList

        openList.remove(currentNode)
        closedList.append(currentNode)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if currentNode.x + x >= 0 and currentNode.y + y >= 0 and currentNode.x + x < len(mapMatrix) and currentNode.y + y < len(mapMatrix[0]):
                    child_of_currentNode = position([currentNode.x+x,currentNode.y+y],previous_position=currentNode)
                    child_of_currentNode.steps = currentNode.steps + 1
                    # if mapMatrix[child_of_currentNode.x][child_of_currentNode.y] == "A":
                    #     continue
                    if child_of_currentNode not in openList and mapMatrix[child_of_currentNode.x][child_of_currentNode.y] != "A" and child_of_currentNode not in closedList:
                        openList.append(child_of_currentNode)
                    else:
                        continue




pathAnswer = marsPathfinder([11,0],[0,13],testPathMap)
print(pathAnswer)

for x in pathAnswer:
    print(x.name)



testPathMap = [
    ["","","","","","","","","","A","","","","K",],
    ["","","","","","","","","","A","","","","",],
    ["","","A","A","A","","","","","","A","","","",],
    ["","","","","A","A","A","A","","","","","A","",],
    ["","","","","","A","A","A","","","","A","","",],
    ["","","","","","", "", "A","A","","","","","",],
    ["","","","","","","","","A","A","","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["","","","","","","","","","","A","A","","",],
    ["P","","","","","","","","","","","A","","",],
]
# -> zaczynamy wyznaczanie ścieżki od końcowego punktu -> "end"
def find_answer_path(pathAnswer):

    finalPath = []


    for position in pathAnswer:
        if position.name == "end":
            endPosition = position
            pathAnswer.pop(pathAnswer.index(endPosition))
            finalPath.append(endPosition)
            print(endPosition,"endPos")
            print(finalPath[-1].pos)
    while True:
        for position in pathAnswer:
            if position == finalPath[-1].previous_position:
                print(finalPath[-1].previous_position)
                print(position.pos)
                prevPos = position
                pathAnswer.pop(pathAnswer.index(prevPos))
                finalPath.append(prevPos)
                if finalPath[-1].name == "start":
                    print("jest start")
                    finalPathXY = []
                    for position in finalPath:
                        finalPathXY.append(position.pos)
                    return finalPathXY


    return finalPath

finalPath = find_answer_path(pathAnswer)

#
testPathMap = [
    ["","","","","","","","","","A","","","","K",],
    ["","","","","","","","","","A","","","","",],
    ["","","A","A","A","","","","","","A","","","",],
    ["","","","","A","A","","","","","","","A","",],
    ["","","","","","A","A","A","","","","A","","",],
    ["","","","","","","","A","A","","","","","",],
    ["","","","","","","","","A","A","","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","A","A","","","",],
    ["","","","","","","","","","","A","","","",],
    ["","","","","","","","","","","A","A","","",],
    ["P","","","","","","","","","","","A","","",],
]



for position in finalPath:
    testPathMap[position[0]][position[1]] = "@"




for x in pathAnswer:
    print(x.previous_position)




for x in testPathMap:
    print(x)