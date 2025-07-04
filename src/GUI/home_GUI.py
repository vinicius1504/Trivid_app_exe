from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTabWidget, QMessageBox,
    QGridLayout,QTableWidget, QTableWidgetItem, QHeaderView, 
    QProgressBar,QAbstractItemView
)
from PySide6.QtGui import QIcon, QPixmap, QMouseEvent,QGuiApplication
from PySide6.QtCore import Qt
import sys
from src.GUI.download_GUI import MainWindow as DownloadWindow
from src.GUI.history_GUI import HistoryPanel
from src.core.detector_link import detect_platform, is_valid_url
from src.GUI.style.home_STY import HomeStyleSheet



class MediaDownloaderPro(QWidget):
    # Inicializa a janela principal e configura layout básico
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TriviD")
        self.setFixedSize(800, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Remove barra padrão
        self.setWindowIcon(QIcon("app_copy copy 2\images\icon.png"))
        
        # Aplicar estilos separados
        self.setStyleSheet(
            HomeStyleSheet.main_widget_style() + 
            HomeStyleSheet.tab_widget_style() + 
            HomeStyleSheet.line_edit_style() + 
            HomeStyleSheet.primary_button_style()
        )
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

    # Cria barra de título personalizada com botões minimizar/maximizar/fechar
    def create_title_bar(self): 
        bar = QWidget()
        bar.setFixedHeight(30)
        bar.setStyleSheet(HomeStyleSheet.title_bar_style())
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

        # Botão minimizar com ícone
        btn_min = QPushButton()
        btn_min.setFixedSize(20, 20)
        min_icon = QIcon("images/icons/minimize_icon.png")
        btn_min.setIcon(min_icon)
        btn_min.setIconSize(btn_min.size())
        btn_min.setStyleSheet(HomeStyleSheet.title_bar_button_style())
        btn_min.clicked.connect(self.showMinimized)
        layout.addWidget(btn_min)

        # Botão maximizar com ícone
        btn_max = QPushButton()
        btn_max.setFixedSize(18, 18)
        max_icon = QIcon("images/icons/maximize_icon.png")
        btn_max.setIcon(max_icon)
        btn_max.setIconSize(btn_max.size())      
        btn_max.setStyleSheet(HomeStyleSheet.title_bar_button_style())
        btn_max.clicked.connect(self.toggle_max_restore)
        layout.addWidget(btn_max)

        # Botão fechar com ícone
        btn_close = QPushButton()
        btn_close.setFixedSize(20, 20) 
        close_icon = QIcon("images/icons/close_icon.png")
        btn_close.setIcon(close_icon)
        btn_close.setIconSize(btn_close.size()) 
        btn_close.setStyleSheet(HomeStyleSheet.title_bar_button_style())
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        # Permitir mover a janela
        bar.mousePressEvent = self.title_bar_mouse_press
        bar.mouseMoveEvent = self.title_bar_mouse_move

        return bar

    # Alterna entre maximizar e restaurar janela
    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # Captura clique para começar a arrastar janela
    def title_bar_mouse_press(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    # Move a janela quando arrastada
    def title_bar_mouse_move(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    # Configura a interface do usuário com abas e painel de histórico
    def setup_ui(self):
        layout = self.body_layout

        # Tabs (apenas Home e Settings)
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_home_tab(), "Home")
        self.tabs.addTab(self.create_settings_tab(), "Settings")
        layout.addWidget(self.tabs)
        
        # Painel de histórico retrátil na parte inferior
        self.history_panel = HistoryPanel()  # Agora usa a classe separada
        layout.addWidget(self.history_panel)

    # Cria a aba inicial com o botão "Paste Here"
    def create_home_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)

        # Container central
        central_container = QWidget()
        central_layout = QVBoxLayout(central_container)
        central_layout.setSpacing(15)
        
        # Label do texto
        label = QLabel("Click and paste the link here")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(HomeStyleSheet.home_label_style())
        
        # Botão Paste Here com ícone
        paste_btn = QPushButton()
        paste_btn.setFixedSize(150, 40)

        # Layout horizontal para o conteúdo do botão
        btn_content = QHBoxLayout()
        btn_content.setContentsMargins(10, 0, 10, 0)
        btn_content.setSpacing(8)

        # Ícone no botão
        icon_label = QLabel()
        icon_pixmap = QPixmap("images/icons/paste_icon.png")
        icon_label.setPixmap(icon_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setStyleSheet(HomeStyleSheet.icon_transparent_style())

        # Texto do botão
        text_label = QLabel("Paste Here")
        text_label.setStyleSheet(HomeStyleSheet.paste_button_text_style())
        
        # Adiciona ícone e texto ao layout do botão
        btn_content.addStretch()
        btn_content.addWidget(icon_label)
        btn_content.addWidget(text_label)
        btn_content.addStretch()

        # Widget container para o conteúdo do botão
        btn_container = QWidget()
        btn_container.setLayout(btn_content)
        paste_btn.setStyleSheet("""
            QPushButton {
                background-color: #008080;
                border: none;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #006666;
            }
        """)

        # Define o widget de conteúdo como o layout do botão
        paste_btn.setLayout(btn_content)
        paste_btn.clicked.connect(self.paste_and_detect)

        # Adiciona widgets ao layout central
        central_layout.addSpacing(50)  # Espaço no topo
        central_layout.addWidget(label)
        central_layout.addWidget(paste_btn, alignment=Qt.AlignCenter)
        central_layout.addStretch(1)  # Empurra tudo para cima

        # Adiciona o container central ao layout principal
        layout.addWidget(central_container)
        
        return tab

    # Pega o link da área de transferência e detecta a plataforma
    def paste_and_detect(self):
        """Pega o link da área de transferência e detecta a plataforma"""
        clipboard = QGuiApplication.clipboard()
        link = clipboard.text().strip()
        
        if not link:
            QMessageBox.warning(self, "Atenção", "Nenhum link encontrado na área de transferência.")
            return
        
        if not is_valid_url(link):
            QMessageBox.warning(self, "Erro", "Por favor cole um link válido.")
            return
            
        platform = detect_platform(link)
        
        if platform in ['youtube', 'twitch', 'spotify']:
            # Usar a mesma GUI, mas passar a plataforma
            self.download_window = DownloadWindow(link, platform)
            self.download_window.show()
        else:
            QMessageBox.warning(self, "Erro", "Plataforma não suportada. Suportamos YouTube, Twitch e Spotify.")

    # Cria a aba de configurações com informações da conta e benefícios do plano
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
        account_layout.addWidget(manage_btn, 2, 1, alignment=Qt.AlignRight)

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

    # Detecta o link e abre a janela de download
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
