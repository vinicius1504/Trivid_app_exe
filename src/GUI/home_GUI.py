from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTabWidget, QMessageBox,
    QGridLayout,QTableWidget, QTableWidgetItem, QHeaderView, 
    QProgressBar,QAbstractItemView
)
from PySide6.QtGui import QIcon, QPixmap, QMouseEvent
from PySide6.QtCore import Qt
from pytablericons import TablerIcons, OutlineIcon, FilledIcon
import sys
from src.GUI.download_GUI import MainWindow as DownloadWindow  # Adicione este import




class MediaDownloaderPro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TriviD")
        self.setFixedSize(800, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Remove barra padrão
        self.setWindowIcon(QIcon("app_copy copy 2\images\icon.png"))
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
                background-color: #f5f5f5;
            }
            QLabel {
                font-weight: 500;
                margin-bottom: 0px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 7px;
                background: #e9e9e9;
                color: #888;
                font-size: 15px;
            }
            QLineEdit:focus {
                outline: none;
                border: 1.5px solid #008080;
                background: #f8f8f8;
                color: #222;
            }
            QPushButton {
                padding: 10px 28px;
                background-color: #008080;
                color: white;
                border: none;
                border-radius: 7px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #006666;
            }
            QTabBar::tab {
                padding: 10px 20px;
                background: #f8f8f8;
                border-bottom: 2px solid transparent;
                color: #666666;
            }
            QTabBar::tab:selected {
                border-bottom: 2px solid #008080;
                color: #008080;
                font-weight: bold;
                color: #343434;

            }
        """)
        # Barra personalizada no topo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.title_bar = self.create_title_bar()
        main_layout.addWidget(self.title_bar)
        # Layout original
        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.setup_ui()
        main_layout.addWidget(self.body_widget)

    def create_title_bar(self): 
        bar = QWidget()
        bar.setFixedHeight(30)
        bar.setStyleSheet("""
            background: #007474;
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(10)  # Menor espaçamento para não empurrar os botões

        # Logo (não alterado)
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

        # Botão minimizar (amarelo)
        btn_min = QPushButton("")
        btn_min.setFixedSize(10, 10)
        btn_min.setStyleSheet("""
            QPushButton {
                background: #FFD600;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #FFEA00;
            }
        """)
        btn_min.clicked.connect(self.showMinimized)
        layout.addWidget(btn_min)

        # Botão maximizar (verde)
        btn_max = QPushButton("")
        btn_max.setFixedSize(10, 10)
        btn_max.setStyleSheet("""
            QPushButton {
                background: #00C853;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #69F0AE;
            }
        """)
        btn_max.clicked.connect(self.toggle_max_restore)
        layout.addWidget(btn_max)

        # Botão fechar (vermelho)
        btn_close = QPushButton("")
        btn_close.setFixedSize(10, 10)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #FF5252;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #FF1744;
            }
        """)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        # Permitir mover a janela
        bar.mousePressEvent = self.title_bar_mouse_press
        bar.mouseMoveEvent = self.title_bar_mouse_move

        return bar

    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def title_bar_mouse_press(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def title_bar_mouse_move(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def setup_ui(self):
        layout = self.body_layout

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_home_tab(), "Home")
        self.tabs.addTab(self.create_settings_tab(), "Account Settings")
        self.tabs.addTab(self.create_history_tab(), "History")  # <-- Adiciona a aba de histórico
        layout.addWidget(self.tabs)

    def create_home_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        # Label
        label = QLabel("Paste the media link")
        layout.addWidget(label)

        # Input + Button
        input_row = QHBoxLayout()
        input_row.setSpacing(12)
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        detect_button = QPushButton("Detect")
        detect_button.setFixedHeight(38)
        detect_button.clicked.connect(self.detect_clicked)

        input_row.addWidget(self.link_input)
        input_row.addWidget(detect_button)
        layout.addLayout(input_row)

        layout.addStretch()
        return tab

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)


        # ==== Account Info Section (com Grid) ====
        account_box = QWidget()
        account_box.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)
        account_layout = QGridLayout(account_box)
        account_layout.setContentsMargins(20, 20, 20, 20)
        account_layout.setHorizontalSpacing(40)
        account_layout.setVerticalSpacing(16)

        # Linha 1: Username (esquerda), Email (direita)
        account_layout.addWidget(QLabel("Username:"), 0, 0, alignment=Qt.AlignRight)
        account_layout.addWidget(QLabel("johndoe"), 0, 1)
        account_layout.addWidget(QLabel("Email:"), 0, 2, alignment=Qt.AlignRight)
        account_layout.addWidget(QLabel("john.doe@example.com"), 0, 3)

        # Linha 2: Account Status, Renewal Date
        account_layout.addWidget(QLabel("Account Status:"), 1, 0, alignment=Qt.AlignRight)
        status_badge = QLabel("Premium")
        status_badge.setStyleSheet("""
            background-color: #d1fae5;
            color: #065f46;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 13px;
        """)
        account_layout.addWidget(status_badge, 1, 1)
        account_layout.addWidget(QLabel("Renewal Date:"), 1, 2, alignment=Qt.AlignRight)
        account_layout.addWidget(QLabel("December 15, 2023"), 1, 3)

        # Linha 3: Botão somente no lado esquerdo
        manage_btn = QPushButton("Manage Subscription")
        manage_btn.setStyleSheet("""
            QPushButton {
                background-color: #006666;
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004d4d;
            }
        """)
        account_layout.addWidget(manage_btn, 2, 1, alignment=Qt.AlignLeft)

        # Adiciona o box ao layout principal da aba
        layout.addWidget(account_box)


        # ==== Plan Benefits Section ====
        benefit_box = QWidget()
        benefit_box.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)
        benefit_layout = QHBoxLayout(benefit_box)
        benefit_layout.setContentsMargins(20, 20, 20, 20)
        benefit_layout.setSpacing(40)

        # Left column of benefits
        left_benefits = QVBoxLayout()
        left_benefits.addWidget(QLabel("✅ Unlimited Downloads\nNo daily limits"))
        left_benefits.addWidget(QLabel("✅ 4K Resolution\nHighest quality available"))

        # Right column of benefits
        right_benefits = QVBoxLayout()
        right_benefits.addWidget(QLabel("✅ Simultaneous Downloads\nUp to 5 at once"))
        right_benefits.addWidget(QLabel("✅ Batch Processing\nProcess multiple links at once"))

        benefit_layout.addLayout(left_benefits)
        benefit_layout.addLayout(right_benefits)
        layout.addWidget(benefit_box)

        return tab

    def create_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        # Search bar
        search_row = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by title...")
        search_input.setFixedHeight(32)
        search_row.addWidget(search_input)
        search_row.addStretch()
        layout.addLayout(search_row)

        # Table
        table = QTableWidget(0, 4)  # 4 columns: File Name, Type, Progress, Actions
        table.setHorizontalHeaderLabels(["File Name", "Type", "Progress", "Actions"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background: #fff;
                border-radius: 10px;
                font-size: 14px;
            }
            QHeaderView::section {
                background: #f8f8f8;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Exemplo de dados (adicione dinamicamente conforme seu app)
        example_data = [
            {"name": "How to Create Amazing UI Designs", "type": "Video", "progress": 100},
            {"name": "Summer Vibes - Chill Mix", "type": "Audio", "progress": 100},
            {"name": "Dance Tutorial - Beginner Level", "type": "Video", "progress": 60},
        ]
        for row, item in enumerate(example_data):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(item["name"]))
            table.setItem(row, 1, QTableWidgetItem(item["type"]))
            # Progress bar
            progress = QProgressBar()
            progress.setValue(item["progress"])
            progress.setTextVisible(item["progress"] < 100)
            table.setCellWidget(row, 2, progress)
            # Actions (exemplo: botão de deletar com ícone)
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(4)
            delete_btn = QPushButton()
            # delete_btn.setIcon(QIcon(TablerIcons.load(OutlineIcon.TRASH)))
            delete_btn.setFixedSize(28, 28)
            delete_btn.setStyleSheet("border: none; background: transparent; font-size: 16px;")
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            table.setCellWidget(row, 3, actions_widget)

        layout.addWidget(table)
        layout.addStretch()
        return tab

    def detect_clicked(self):

        if not self.link_input.text():
            QMessageBox.warning(self, "Atenção", "Cole um link antes de buscar.")
            return
        link = self.link_input.text()
        # print("🔍 Link detectado:", link)
        self.download_window = DownloadWindow(link)  # Passe o link aqui
        self.download_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MediaDownloaderPro()
    window.show()
    sys.exit(app.exec())
