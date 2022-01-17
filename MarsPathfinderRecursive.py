import math,time


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
print(len(testPathMap))
print(len(testPathMap[0]))

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


def marsPathfinder(startPoint:list,endPoint:list,mapMatrix:list,candidates=[],answer=[]):


    startX,startY = startPoint
    endX,endY = endPoint
    start_position = position(startPoint)
    start_position.name = "start"
    answer.append(start_position)
    # Detect neighbours
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            if startX + x >= 0 and startY + y >= 0 and startX + x < len(mapMatrix) and startY+y < len(mapMatrix[0]):
                if mapMatrix[startX+x][startY+y] == "K":
                    endPosition = position([startX+x,startY+y],[startX,startY])
                    endPosition.name = "end"
                    answer.append(endPosition)
                    return answer
                if mapMatrix[startX+x][startY+y] != "A" and mapMatrix[startX+x][startY+y] != "Q" and mapMatrix[startX+x][startY+y] != "B" and mapMatrix[startX+x][startY+y] != "K" :
                    if [startX + x, startY + y] not in candidates:
                        mapMatrix[startX+x][startY+y] = "Q"
                        actual_position = position([startX + x, startY + y],[startX,startY])
                        actual_position.steps = actual_position.steps + 1
                        candidates.append(actual_position)
    # Sort list by distances -> w pierwszej kolejności sprawdzam pukty, kórych odległość od końca jest mniejsza + ilosc stepsów
    candidates.sort(key= lambda a: math.sqrt((a.x-endX)**2 + (a.y-endY)**2) + a.steps )
    candidates.reverse()
    answer.append(candidates[0])
    for point in candidates:
        new_start = candidates.pop(0)
        new_start = new_start.pos
        return  marsPathfinder(new_start,endPoint,mapMatrix,candidates,answer)

    return answer







pathAnswer = marsPathfinder([11,0],[0,13],testPathMap)
print(pathAnswer)

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
            if position.pos == finalPath[-1].previous_position:
                prevPos = position
                pathAnswer.pop(pathAnswer.index(prevPos))
                finalPath.append(prevPos)
                if prevPos.steps == 0:
                    finalPathXY = []
                    for position in finalPath:
                        finalPathXY.append(position.pos)
                    return finalPathXY


    return finalPath

finalPath = find_answer_path(pathAnswer)


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




# for x in pathAnswer:
#     print(x.previous_position)




for x in testPathMap:
    print(x)