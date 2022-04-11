from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from SelectBox import SelectBox
from kivy.core.window import Window
from kivy.graphics import *
from kivy.graphics import InstructionGroup

import time
import math

SCROLL_SPEED = 60  # Scroll speed must be power of 2


class MainMapPicture(Scatter):

    canvasCleaner = 0
    root = ""
    source = StringProperty()
    draw_mode = StringProperty()
    shiftXCounter = 0
    shiftYCounter = 0
    explosions = []
    explosionsCounter = 0
    shadowRange = 2
    def moveX(self,mouseX,screenWidth):
        if self.root.scrollEnabled == True:
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
        if self.root.scrollEnabled == True:
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

    def draw_explosion(self,pos,bulletRoot):
        self.explosionsCounter += 1
        if self.explosionsCounter == 2:
            self.explosionsCounter = 0
            explosion = InstructionGroup()
            if bulletRoot.player == self.root.humanPlayer:
                explosion.add(Rectangle(texture=self.root.bullet_friend_source["bullet_expl"],pos=(pos[1]-30,pos[0]-30),size=(120,120)))
            else:
                explosion.add(Rectangle(texture=self.root.bullet_enemy_source["bullet_expl"], pos=(pos[1] - 30, pos[0] - 30),size=(120, 120)))
            self.explosions.append(explosion)
            self.canvas.add(explosion)

    def clear_explosions(self):
        if self.canvasCleaner == 9:
            if self.explosions:
                for x in self.explosions:
                    self.canvas.remove(x)
                    self.explosions.remove(x)
                    self.canvasCleaner = 0
        else:
            self.canvasCleaner += 1













