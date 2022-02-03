from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.widget import Widget


import time
import math

SCROLL_SPEED = 60  # Scroll speed must be power of 2


class MainMapPicture(Scatter):

    source = StringProperty()
    draw_mode = StringProperty()
    shiftXCounter = 0
    shiftYCounter = 0
    def moveX(self,mouseX,screenWidth):
        if mouseX == 0:
            if self.x != 0:
                self.x += SCROLL_SPEED
                self.shiftXCounter -= SCROLL_SPEED
                return SCROLL_SPEED
        elif mouseX > screenWidth - 3:
            if self.shiftXCounter + self.width * 0.9< self.children[0].size[0]:
                self.right -= SCROLL_SPEED
                self.shiftXCounter += SCROLL_SPEED
                return -SCROLL_SPEED

    def moveY(self,mouseY,screenHeight):
        if mouseY == 1:
            if self.y != 0:
                self.y += SCROLL_SPEED
                self.shiftYCounter -= SCROLL_SPEED
                return SCROLL_SPEED

        elif mouseY > screenHeight - 5:
            if self.shiftYCounter + self.height < self.children[0].size[1]:
                self.top -= SCROLL_SPEED
                self.shiftYCounter += SCROLL_SPEED
                return -SCROLL_SPEED






