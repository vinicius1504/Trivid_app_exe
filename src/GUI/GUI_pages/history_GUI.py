from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class HistoryPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_panel()
    
    def setup_panel(self):
        # Container principal do painel
        panel_layout = QVBoxLayout(self)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(0)
        
        # Barra superior com título e botão de toggle
        self.header_bar = self.create_header_bar()
        panel_layout.addWidget(self.header_bar)
        
        # Conteúdo do histórico (inicializar como oculto)
        self.history_content = self.create_history_content()
        self.history_content.setFixedHeight(500)
        self.history_content.hide()  # Começa oculto
        
        panel_layout.addWidget(self.history_content)
    
    def create_header_bar(self):
        header_bar = QWidget()
        header_bar.setFixedHeight(40)
        header_bar.setStyleSheet("""
            QWidget {
                background-color: #008080;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # Título "History"
        history_title = QLabel("History")
        history_title.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 16px;
        """)
        header_layout.addWidget(history_title)
        header_layout.addStretch()
        
        # Botão de toggle
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(30, 30)
        toggle_icon = QIcon("images/icons/down_icon.png")
        self.toggle_btn.setIcon(toggle_icon)
        self.toggle_btn.setIconSize(self.toggle_btn.size())
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }   
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_history)
        header_layout.addWidget(self.toggle_btn)
        
        return header_bar
    
    def create_history_content(self):
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
        """)
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        # Container com scroll para os cards
        from PySide6.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #cccccc;
                border-radius: 4px;
            }
        """)

        # Widget interno do scroll
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(0, 0, 10, 0)

        # Criar cards de exemplo
        example_files = [
            {
                "title": "asdasdasdasdasdasd",
                "format": "MP4 - 1080P",
                "time": "01:00",
                "size": "450Mb"
            },
            {
                "title": "Another Video File",
                "format": "MP3 - 320kbps",
                "time": "03:45",
                "size": "8.5Mb"
            },
            {
                "title": "Tutorial Video",
                "format": "MP4 - 720P",
                "time": "12:30",
                "size": "256Mb"
            }
        ]

        for file_data in example_files:
            card = self.create_file_card(file_data)
            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        return content_widget
    
    def create_file_card(self, file_data):
        """Cria um card individual para cada arquivo"""
        card = QWidget()
        card.setFixedHeight(80)
        card.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
            QWidget:hover {
                background-color: #e9ecef;
            }
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # Ícone de play
        play_icon = QLabel()
        play_icon.setFixedSize(50, 50)
        play_icon.setStyleSheet("""
            QLabel {
                background-color: #6c757d;
                border-radius: 25px;
                color: white;
                font-size: 20px;
            }
        """)
        play_icon.setAlignment(Qt.AlignCenter)
        play_icon.setText("▶")
        layout.addWidget(play_icon)

        # Informações do arquivo
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        # Título
        title_label = QLabel(file_data["title"])
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #212529;
            }
        """)
        
        # Formato e detalhes
        details_label = QLabel(f"{file_data['format']} • Time: {file_data['time']} • Size: {file_data['size']}")
        details_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #6c757d;
            }
        """)

        info_layout.addWidget(title_label)
        info_layout.addWidget(details_label)
        info_layout.addStretch()

        layout.addLayout(info_layout)
        layout.addStretch()

        # Botão de deletar
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #dc3545;
                color: white;
            }
        """)
        layout.addWidget(delete_btn)

        return card
    
    def toggle_history(self):
        if self.history_content.isVisible():
            self.history_content.hide()
            down_icon = QIcon("images/icons/up_icon.png")
            self.toggle_btn.setIcon(down_icon)
        else:
            self.history_content.show()
            up_icon = QIcon("images/icons/down_icon.png")
            self.toggle_btn.setIcon(up_icon)