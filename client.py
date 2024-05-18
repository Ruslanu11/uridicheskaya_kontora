from PySide6.QtWidgets import QApplication
import sys
from src.client.main_widgets.main_window import MainWindow
from src.database.database_models import Position

Position.create(post='manager', power_level=1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = MainWindow()
    app.exec()
