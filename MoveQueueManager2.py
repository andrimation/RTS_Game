import MarsPathfinder_setup
import math
import copy
from GameUnit import GameUnit
from UranMiner import UranMiner

class MoveQueueManager2():
    def __init__(self,root):
        self.root = root

# Wyszukiwanie trasy.
    # 1) w jednym framesie obliczamy path tylko dla jednego unitu.
    #   A) Zaczynając obliczenia z listy z orderami popujemy jeden order_destination z indeksem 0
    #
    #   - sprawdzamy czy dana destynacja jest - w innych orders_destination i czy jest jako destination w move_queue i czy jest wolna
    #     czyli:
    #     - sprawdzamy czy dana komórka jest w innych oczekujących do oliczenia rozkazach
    #     - sprawdzamy czy dana komórka jest już w innych wykonywanych rozkazach
    #     - sprawdzamy czy dana komórka jest wolna.
    #     Jeśli się komórka powtarza, to wyszukujemy nowej, bliskiej komórki docelowej, jeśli nie to zwracamy wybraną komórkę, jako komórkę
    #     docelową dla której szukamy trasy.

    #   B) Jeśli obliczenie orderu zakończy się pomyślnie, to przekazujemy order do kolejki move_queue, a wypopowany order destynacja przepada
    #       - sprawdzamy czy order destination jest dłuższy niż zwykły - jeśli jest dłuższy, to do move queue przekazujemy wynik obliczania trasy
    #         + trasa która jest zapisana jako [-1] order destination
    #   C) Jeśli obliczenie orderu zwróci None, to z wynikiem nie robimy nic, a wypopowany wcześniej order, wsadzamy z powrotem na koniec kolejki destynacji
    #   - takie rozwiązanie spowoduje że jeśli jakiś order nie jest możliwy do obliczenia w danym momencie, to nie będzie on pobierany w kolejnym framesie
    #     ale obliczane będą kolejne ordersy, a w miarę ich wykonania, może stać się możliwe obliczenie tego ordersu który zwracał None. Pomoże to uniknąć
    #     zapętlenia na nieobliczalnym rozkazie ( w danej chwili )

# Wykonywanie rozkazów:
    # 1) rozkazy wykonywane są jak dotychczas.
    # 2) Jeśli kolejna komórka na którą ma wjechać pojazd, jest zajęta przez coś innego to:
    #    - pojazd odlicza do 50
    #    - po odliczeniu do 50 sprawdzamy czy kolejna komórka wciąż jest zajęta.
    #       - Jeśli nie - to wykonujemy ruch
    #       - Jeśli tak - to obliczamy trasę - od komórki gdzie znajduje się jednostka, do kolejnej najbliższej wolnej komórki w obliczonym już rozkazie.
    #       Pierwsza wersja: zakładam obliczenie tej mini trasy we framesie ruchu - sprawdzamy która kolejna komórka jest wolna, i obliczamy
    #                        trasę dla tej komórki - odejmujemy trasę z komórką zajętą od istniejącej trasy w rozkazie, i dodajemy mini trasę do istniejącego rozkazu
    #
    #       Wersja druga:   usuwamy istniejący rozkaz z move queue, i dodajemy do kolejki rozkazów do obliczenia nowy rozkaz do obliczenia, zawierający obliczenie mini
    #                       trasy + na końcu listę z obliczonymi wcześniej rozkazami - w tym przypadku, na początku algorytmu musimy sprawdzać czy order destination
    #                       ma len 4(albo 3?) czy 5(albo 4?) - jeśli jest ten dłuższy, to wiemy, że jest to obliczanie mini trasy i po obliczeniu mini trasy, do
    #                       obliczonej mini trasy dodajemy ostatni element order destination - czyli wczesniej obliczoną już trasę. ( to chyba lepsze wyjście, nie
    #                       będzie blokować move, a obliczenie będzie się wykonywać w funkcji obliczania. )
    # 3) popawić pozycje jednostek tak aby nigdy sie nie przenikały na mapie !
    # 4) Problem utraty kontroli nad jednostkami po iluś atakach
    # 5) Problem nie pojawiających się uranMinerów po ataku na inne jednostki

    # Rozkaz jest usuwany jeżeli
    #   1) jednostka znajdzie się w komórce do której miała dotrzeć
    #   2) jeżeli jednostka atakuje i znajduje sie w odległości strzału od atakowanego obiektu

    # Inside functions
    def check_destination_cell(self,destination,unitInMove):
        """Function checks if destination is duplicated in orders_destinations, in move_queue and if position is free
            - returns new destination if duplication or not-free , or returns destination"""
        # Tu coś chujowo działa. - problem z zacinaniem się przy krótkich dystansach wynikał z tego że każda jednostka dostawała tą samą destynację.
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

    # Main functions
    def compute_orders_paths(self):
        if self.root.orders_destinations:
            order_destination = self.root.orders_destinations.pop(0)
            unit = order_destination[0]
            destination = self.check_destination_cell(order_destination[1],unit)  # nie wywoływać tego dla UranMinerów ! one maja trafiać idealnie !
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
                return

            if computePath == None:
                self.root.orders_destinations.append(order_destination)


