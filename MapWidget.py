import requests
from settings import *

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi


class MapWidget(QWidget):
    def __init__(self, window_size, coords):
        super().__init__()
        loadUi("UICs/MapWidget.ui", self)

        self.window_size = window_size
        self.coords = coords

        self.resize(self.window_size[0], self.window_size[1])
        self.set_map_image()

    def get_map_image(self):
        geocoder_params = {
            "ll": self.coords,
            "spn": SPN,
            "l": L
        }

        response = requests.get(STATIC_MAPS_API_SERVER, params=geocoder_params)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def set_map_image(self):
        self.mapImage.resize(self.window_size[0], self.window_size[1])
        self.get_map_image()
        self.mapImage.setPixmap(QPixmap(self.map_file))

    def closeEvent(self, event):
        from os import remove
        remove(self.map_file)
