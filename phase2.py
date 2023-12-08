from datetime import datetime
import time

class stop_red():
    def __init__(self, pair, color,dist):
        self.pair=pair
        self.color=color
        self.dist=dist

    def stop_motors(self):
        print(self.color.get_color())
         