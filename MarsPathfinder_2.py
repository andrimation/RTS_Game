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

class position():
    def __init__(self,pos,previous_position=None):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

        self.steps = 0



def marsPathfinder(startPoint:list,endPoint:list,mapMatrix:list,candidates=[],answer=[]):


    startX,startY = startPoint
    endX,endY = endPoint
    actual_position = position(startPoint)

    # Detect neighbours
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            if startX + x >= 0 and startY + y >= 0 and startX + x < len(mapMatrix) and startY+y < len(mapMatrix[0]):
                if mapMatrix[startX+x][startY+y] == "K":
                    time.sleep(1)
                    print("K")
                    return answer
                if mapMatrix[startX+x][startY+y] != "A" and mapMatrix[startX+x][startY+y] != "Q" and mapMatrix[startX+x][startY+y] != "B" and mapMatrix[startX+x][startY+y] != "K" :
                    if [startX + x, startY + y] not in candidates:
                        print(startX+x,startY+y)
                        mapMatrix[startX+x][startY+y] = "Q"
                        actual_position = position([startX + x, startY + y],[startX,startY])
                        actual_position.steps = actual_position.steps + 1
                        candidates.append(actual_position)
    # Sort list by distances -> w pierwszej kolejności sprawdzam pukty, kórych odległość od końca jest mniejsza + ilosc stepsów
    print(candidates)
    candidates.sort(key= lambda a: math.sqrt((a.x-endX)**2 + (a.y-endY)**2) + a.steps )
    # mapMatrix[candidates[0][0]][candidates[0][1]] = "B"
    answer.append(candidates[0])
    # time.sleep(0.25)
    for x in mapMatrix:
        print(x)
    for point in candidates:
        new_start = candidates.pop(0)
        print(new_start)
        new_start = new_start.pos
        return  marsPathfinder(new_start,endPoint,mapMatrix,candidates,answer)

    return answer







path = marsPathfinder([11,0],[0,13],testPathMap)
print(path)

# testPathMap = [
#     ["","","","","","","","","","","","","","K",],
#     ["","","","","","","","","","","","","","",],
#     ["","","A","A","A","","","","","","","","","",],
#     ["","","","","A","A","","","","","","","","",],
#     ["","","","","","A","A","A","","","","","","",],
#     ["","","","","","","","A","A","","","","","",],
#     ["","","","","","","","","A","A","","","","",],
#     ["","","","","","","","","","A","A","","","",],
#     ["","","","","","","","","","A","A","","","",],
#     ["","","","","","","","","","","A","","","",],
#     ["","","","","","","","","","","A","","","",],
#     ["P","","","","","","","","","","","","","",],
# ]
#
# for point in path:
#     testPathMap[point[0]][point[1]] = "B"
#
# for x in testPathMap:
#     print(x)