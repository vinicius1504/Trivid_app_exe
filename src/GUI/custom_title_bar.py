from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtCore import Qt

class CustomTitleBar(QWidget):
    def __init__(self, parent=None, on_close=None, on_min=None, on_max=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("background: #007474;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(10)

        # Logo
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 4, 0, 0)
        logo_layout.setSpacing(0)
        logo = QLabel()
        pixmap = QPixmap("images\\Frame 15.png")
        logo.setPixmap(pixmap.scaledToHeight(20, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        logo_layout.addWidget(logo, alignment=Qt.AlignLeft | Qt.AlignBottom)
        logo_layout.addStretch()
        layout.addWidget(logo_container)
        layout.addStretch()

        # Botão minimizar
        btn_min = QPushButton("")
        btn_min.setFixedSize(10, 10)
        btn_min.setStyleSheet("""
            QPushButton { background: #FFD600; border: none; border-radius: 10px; }
            QPushButton:hover { background: #FFEA00; }
        """)
        if on_min:
            btn_min.clicked.connect(on_min)
        layout.addWidget(btn_min)

        # Botão maximizar
        btn_max = QPushButton("")
        btn_max.setFixedSize(10, 10)
        btn_max.setStyleSheet("""
            QPushButton { background: #00C853; border: none; border-radius: 10px; }
            QPushButton:hover { background: #69F0AE; }
        """)
        if on_max:
            btn_max.clicked.connect(on_max)
        layout.addWidget(btn_max)

        # Botão fechar
        btn_close = QPushButton("")
        btn_close.setFixedSize(10, 10)
        btn_close.setStyleSheet("""
            QPushButton { background: #FF5252; border: none; border-radius: 10px; }
            QPushButton:hover { background: #FF1744; }
        """)
        if on_close:
            btn_close.clicked.connect(on_close)
        layout.addWidget(btn_close)

        # Permitir mover a janela
        self.mousePressEvent = self.title_bar_mouse_press
        self.mouseMoveEvent = self.title_bar_mouse_move
        self._drag_pos = None

    def title_bar_mouse_press(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.parent().frameGeometry().topLeft()
            event.accept()

    def title_bar_mouse_move(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.parent().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()