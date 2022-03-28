from kivy.uix.image import Image
from kivy.uix.widget import Widget

# Algorytm
# Wyznaczamy odległość jaka nas interesuje do rzucania cienia:
# Sprawdzamy czy są w tej odległosci jakieś obiekty
# Do znalezionych w tej odległości obiektów rysujemy trójkątne widgety

# Później ( albo obliczamy katy, albo, chyba prościej, ) rysujemy widgety pomiędzy obiektami,
# przez punkty rzucające cień , ale dalej ( to są światła nie zablokowane przez inne obiekty )

