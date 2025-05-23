import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from image_overlay.overlay import OverlayImage
#from .control_panel import ControlPanel
from image_overlay.control_panel import ControlPanel
#from .utils import open_image_dial
from image_overlay.utils import open_image_dialog

def main():
    app = QApplication(sys.argv)

    # Let user select any PNG image file from anywhere
    image_path = open_image_dialog()
    if not image_path:
        QMessageBox.warning(None, "No Image Selected", "No image was selected. Exiting application.")
        sys.exit(0)

    overlay = OverlayImage(image_path)
    overlay.show()

    controls = ControlPanel(overlay)
    controls.move(100, 100)
    controls.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
