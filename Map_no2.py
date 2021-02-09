import requests
from settings import *

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class MapWidget(QWidget):
    def __init__(self, window_size, coords):
        super().__init__()
        loadUi("UICs/MapWidget.ui", self)

        self.window_size = window_size
        self.coords = coords

        self.resize(self.window_size[0], self.window_size[1])
        self.set_map_image()

    def keyPressEvent(self, e):
        global SPN
        if e.key() == Qt.Key_PageUp:
            new_spn = float(SPN.split(",")[0]) - 0.005
        elif e.key() == Qt.Key_PageDown:
            new_spn = float(SPN.split(",")[0]) + 0.005
        else:
            return
        if new_spn > 0.025:
            QMessageBox.information(self, 'Неверный масштаб', 'Слишком мелкий масштаб!')
        elif new_spn < 0.004:
            QMessageBox.information(self, 'Неверный масштаб', 'Слишком крупный масштаб!')
        else:
            SPN = f'{new_spn},{new_spn}'
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
