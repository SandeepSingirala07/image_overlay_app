from PyQt6.QtWidgets import (
    QWidget, QPushButton, QSlider, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self, overlay_window):
        super().__init__()
        self.overlay = overlay_window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(30, 30, 30, 230); color: white; font-size: 14px;")

        self.collapsed = True
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedSize(30, 30)
        self.toggle_btn.clicked.connect(self.toggle_panel)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.setFixedWidth(100)
        self.slider.valueChanged.connect(self.update_opacity)

        self.zoom_in_btn = QPushButton("+")
        self.zoom_out_btn = QPushButton("-")
        self.zoom_in_btn.clicked.connect(lambda: self.overlay.zoom('in'))
        self.zoom_out_btn.clicked.connect(lambda: self.overlay.zoom('out'))

        self.move_btn = QPushButton("Move")
        self.move_btn.setCheckable(True)
        self.move_btn.clicked.connect(self.toggle_move_mode)

        self.close_btn = QPushButton("✕")
        self.close_btn.clicked.connect(self.exit_app)

        self.control_frame = QFrame()
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.move_btn)
        control_layout.addWidget(self.zoom_out_btn)
        control_layout.addWidget(self.zoom_in_btn)
        control_layout.addWidget(self.slider)
        control_layout.addWidget(self.close_btn)
        control_layout.setContentsMargins(5, 5, 5, 5)
        self.control_frame.setLayout(control_layout)
        self.control_frame.setVisible(False)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.control_frame)
        main_layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(main_layout)
        self.setFixedSize(270, 100)

        self.drag_active = False
        self.drag_pos = None

    def toggle_panel(self):
        self.collapsed = not self.collapsed
        self.control_frame.setVisible(not self.collapsed)

    def update_opacity(self, val):
        self.overlay.set_opacity(val / 100.0)

    def toggle_move_mode(self):
        move_enabled = self.move_btn.isChecked()
        self.overlay.set_drag_enabled(move_enabled)
        self.move_btn.setText("Stop" if move_enabled else "Move")

    def exit_app(self):
        self.overlay.close()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_active = True
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.drag_active:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_active = False