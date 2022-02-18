from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Rectangle,Ellipse,Color,Line

class miniMap(Widget):
    def __init__(self,root):
        super(miniMap, self).__init__()
        self.root = root
        self.imageX, self.imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size
        self.viewBox = None

    def create_minimap(self):
        self.size_hint = (None,None)
        self.size = ((Window.size[0] * 0.1)*0.95, int((self.imageY * (Window.size[0] * 0.1)*0.95) / self.imageX))
        posX,posY = ((Window.size[0] * 0.1)*0.025,self.root.ids["SidePanelWidget"].height * 0.83)
        self.pos = (posX,posY)
        self.root.ids["SidePanelWidget"].add_widget(self,0)
        self.root.minimapObject = self
        self.add_view_position()

    def add_view_position(self):
        self.viewBox = Image()
        zeroX, zeroY = ((Window.size[0] * 0.1) * 0.025, self.root.ids["SidePanelWidget"].height * 0.83)
        self.viewBox.pos = (zeroX,zeroY)
        bigViewX,bigViewY = Window.size[0]*0.9,Window.size[1]
        smallX = (bigViewX * self.size[0])/self.imageX
        smallY = (bigViewY * self.size[1])/self.imageY
        self.viewBox.size_hint = (None,None)
        self.viewBox.size = (smallX,smallY)
        self.viewBox.color = (0.2,0.7,1,0.5)
        self.add_widget(self.viewBox,0)

    def update_view_position(self,shiftX,shiftY):
        if shiftX != None:
            self.viewBox.pos[0] += -((shiftX * self.width)/self.imageX)
        if shiftY != None:
            self.viewBox.pos[1] += -((shiftY * self.height) / self.imageY)


