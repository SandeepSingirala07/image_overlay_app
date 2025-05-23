import ctypes
from PyQt6.QtWidgets import QWidget, QLabel, QSizeGrip
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen

# Windows constants for click-through
GWL_EXSTYLE = -20
WS_EX_TRANSPARENT = 0x20
WS_EX_LAYERED = 0x80000

user32 = ctypes.windll.user32
GetWindowLong = user32.GetWindowLongW
SetWindowLong = user32.SetWindowLongW

class OverlayImage(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.image_label = QLabel(self)
        self.original_pixmap = QPixmap(image_path)
        self.scale_factor = 1.0
        self.image_label.setPixmap(self.original_pixmap)
        self.image_label.setScaledContents(True)

        self.resize(self.original_pixmap.size())
        self.image_label.resize(self.size())

        self.size_grip = QSizeGrip(self)
        self.size_grip.resize(20, 20)
        self.size_grip.setStyleSheet("background-color: rgba(255,255,255,0);")

        self._drag_active = False
        self._drag_pos = QPoint()
        self.drag_enabled = False
        self.set_click_through(True)

        self.highlight_enabled = False
        self.glow_timer = QTimer(self)
        self.glow_opacity = 0
        self.glow_direction = 1
        self.glow_timer.timeout.connect(self.update_glow)

    def resizeEvent(self, event):
        self.image_label.resize(self.size())
        self.size_grip.move(self.width() - 20, self.height() - 20)

    def mousePressEvent(self, event):
        if self.drag_enabled and event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.highlight_enabled = True
            self.glow_opacity = 50
            self.glow_direction = 1
            self.glow_timer.start(30)

    def mouseMoveEvent(self, event):
        if self.drag_enabled and self._drag_active:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_active = False
        self.highlight_enabled = False
        self.glow_timer.stop()
        self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom('in')
        else:
            self.zoom('out')
        self.highlight_enabled = True
        self.glow_opacity = 100
        QTimer.singleShot(300, self.disable_glow)
        self.update()

    def disable_glow(self):
        self.highlight_enabled = False
        self.update()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.close()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.highlight_enabled:
            painter = QPainter(self)
            pen = QPen(QColor(0, 120, 215, self.glow_opacity))  # Blue glow color
            pen.setWidth(10)
            painter.setPen(pen)
            painter.drawRect(self.rect().adjusted(5, 5, -5, -5))

    def update_glow(self):
        if self.glow_direction == 1:
            self.glow_opacity += 10
            if self.glow_opacity >= 150:
                self.glow_direction = -1
        else:
            self.glow_opacity -= 10
            if self.glow_opacity <= 50:
                self.glow_direction = 1
        self.update()

    def set_click_through(self, enabled):
        hwnd = self.winId().__int__()
        ex_style = GetWindowLong(hwnd, GWL_EXSTYLE)
        if enabled:
            SetWindowLong(hwnd, GWL_EXSTYLE, ex_style | WS_EX_TRANSPARENT | WS_EX_LAYERED)
        else:
            SetWindowLong(hwnd, GWL_EXSTYLE, ex_style & ~WS_EX_TRANSPARENT)

    def set_opacity(self, value):
        self.setWindowOpacity(value)

    def zoom(self, in_out):
        if in_out == 'in':
            self.scale_factor *= 1.1
        elif in_out == 'out':
            self.scale_factor /= 1.1

        new_size = self.original_pixmap.size() * self.scale_factor
        self.resize(new_size)
        self.image_label.setPixmap(self.original_pixmap.scaled(new_size, Qt.AspectRatioMode.KeepAspectRatio))

    def set_drag_enabled(self, enabled):
        self.drag_enabled = enabled
        self.set_click_through(not enabled)
