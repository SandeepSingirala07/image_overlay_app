from PyQt6.QtWidgets import QFileDialog

def open_image_dialog(parent=None):
    """Open a file dialog to select a PNG image from anywhere on system."""
    options = QFileDialog.Option.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Select PNG Image",
        "",
        "PNG Images (*.png);;All Files (*)",
        options=options
    )
    return file_path