import sys

from PyQt5.QtWidgets import QApplication
from Map_no2 import MapWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapWidget((600, 450), '37.530887,55.703118')
    ex.show()
    sys.exit(app.exec())
