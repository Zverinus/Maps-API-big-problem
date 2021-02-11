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
        self.lat_dependence = window_size[0] / window_size[1]
        self.lon_dependence = window_size[1] / window_size[0]
        self.coords = coords
        self.lat, self.lon = self.coords.split(',')
        self.spn = f"{0.01 * self.lat_dependence},{0.01 * self.lon_dependence}"

        self.resize(self.window_size[0], self.window_size[1])
        self.set_map_image()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_PageUp:
            spn1 = float(self.spn.split(",")[0]) - 0.005 * self.lat_dependence
            spn2 = float(self.spn.split(",")[0]) - 0.005 * self.lon_dependence
            self.set_new_spn(spn1, spn2)
        elif e.key() == Qt.Key_PageDown:
            spn1 = float(self.spn.split(",")[0]) + 0.005 * self.lat_dependence
            spn2 = float(self.spn.split(",")[0]) + 0.005 * self.lon_dependence
            self.set_new_spn(spn1, spn2)
        elif e.key() == Qt.Key_Up:
            self.set_new_coords('lon', '+')
        elif e.key() == Qt.Key_Down:
            self.set_new_coords('lon', '-')
        elif e.key() == Qt.Key_Left:
            self.set_new_coords('lat', '-')
        elif e.key() == Qt.Key_Right:
            self.set_new_coords('lat', '+')

    def set_new_coords(self, line, operation):
        if line == 'lat':
            if abs(float(self.spn.split(',')[0])) <= 180:
                self.lat = eval(f"{self.lat} {operation} {float(self.spn.split(',')[0]) * 2}")
            else:
                QMessageBox.information(self, 'Неверные координаты', 'Вы за границами карты!')
        else:
            if abs(float(self.spn.split(',')[1])) <= 90:
                self.lon = eval(f"{self.lon} {operation} {float(self.spn.split(',')[1])}")
            else:
                QMessageBox.information(self, 'Неверные координаты', 'Вы за границами карты!')
        self.coords = f"{self.lat},{self.lon}"
        self.set_map_image()

    def set_new_spn(self, spn1, spn2):
        if spn1 > 0.025 or spn2 > 0.025:
            QMessageBox.information(self, 'Неверный масштаб', 'Слишком мелкий масштаб!')
        elif spn1 < 0.004 or spn1 < 0.004:
            QMessageBox.information(self, 'Неверный масштаб', 'Слишком крупный масштаб!')
        else:
            self.spn = f'{spn1},{spn2}'
            print(self.spn)
            self.set_map_image()

    def get_map_image(self):
        geocoder_params = {
            "ll": self.coords,
            "spn": self.spn,
            "l": L,
            "size": f"{self.window_size[0]},{self.window_size[1]}"
        }

        response = requests.get(STATIC_MAPS_API_SERVER, params=geocoder_params)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def set_map_image(self):
        self.get_map_image()
        self.mapImage.setPixmap(QPixmap(self.map_file))

    def closeEvent(self, event):
        from os import remove
        remove(self.map_file)
