from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle,Ellipse,Color,Line

class miniMap(Widget):
    def __init__(self,root):
        super(miniMap, self).__init__()
        self.root = root

    def create_minimap(self):
        imageX,imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size
        self.size_hint = (None,None)
        self.size = ((Window.size[0] * 0.1)*0.95, int((imageY * (Window.size[0] * 0.1)*0.95) / imageX))
        posX,posY = ((Window.size[0] * 0.1)*0.025,self.root.ids["SidePanelWidget"].height * 0.83)
        self.pos = (posX,posY)
        self.root.ids["SidePanelWidget"].add_widget(self,0)
        self.root.minimapObject = self
