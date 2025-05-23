import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QScreen

def take_screenshot(save_path):
    app = QApplication.instance() or QApplication(sys.argv)
    screen: QScreen = app.primaryScreen()
    screenshot = screen.grabWindow(0)
    screenshot.save(save_path, 'png')