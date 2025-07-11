from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QGridLayout
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, Signal,QEasingCurve,QPropertyAnimation
from src.GUI.style.GUI_style.history_STY import HistoryStyleSheet

class HistoryPanel(QWidget):
    history_expanded = Signal()
    history_collapsed = Signal()


    def __init__(self):
        super().__init__()
        self.is_two_columns = True  # Controla se exibe em 1 ou 2 colunas
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
        # Não definimos altura fixa aqui, para permitir que ele se expanda
        self.history_content.hide()  # Começa oculto
        
        panel_layout.addWidget(self.history_content)
    
    def create_header_bar(self):
        header_bar = QWidget()
        header_bar.setFixedHeight(40)
        header_bar.setStyleSheet(HistoryStyleSheet.header_bar_style())
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # Título "History"
        history_title = QLabel("History")
        history_title.setStyleSheet(HistoryStyleSheet.history_title_style())
        header_layout.addWidget(history_title)
        header_layout.addStretch()
        
        # Botão para alternar entre 1 e 2 colunas (ícone)
        self.toggle_columns_btn = QPushButton()
        self.toggle_columns_btn.setFixedSize(30, 30)
        # Ícone para alternar colunas - você pode usar grid_icon.png ou columns_icon.png
        columns_icon = QIcon("images/icons/table_icon.png")  # Coloque seu ícone aqui
        self.toggle_columns_btn.setIcon(columns_icon)
        self.toggle_columns_btn.setIconSize(self.toggle_columns_btn.size())
        self.toggle_columns_btn.setStyleSheet(HistoryStyleSheet.toggle_button_style())
        self.toggle_columns_btn.clicked.connect(self.toggle_columns)
        header_layout.addWidget(self.toggle_columns_btn)
        
        # Botão de toggle (expandir/recolher)
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(30, 30)
        toggle_icon = QIcon("images/icons/down_icon.png")
        self.toggle_btn.setIcon(toggle_icon)
        self.toggle_btn.setIconSize(self.toggle_btn.size())
        self.toggle_btn.setStyleSheet(HistoryStyleSheet.toggle_button_style())
        self.toggle_btn.clicked.connect(self.toggle_history)
        header_layout.addWidget(self.toggle_btn)
        
        return header_bar
    
    def create_history_content(self):
        content_widget = QWidget()
        content_widget.setStyleSheet(HistoryStyleSheet.history_content_style())
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        # Container com scroll para os cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(HistoryStyleSheet.scroll_area_style())

        # Definir altura fixa para a área de scroll
        # scroll_area.setFixedHeight(250)  # Altura para mostrar ~4 cards em 2 colunas

        # Widget interno do scroll
        self.scroll_widget = QWidget()
        self.create_cards_layout()

        scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(scroll_area)

        return content_widget
    
    def create_cards_layout(self):
        """Cria o layout dos cards baseado no modo (1 ou 2 colunas)"""
        # Limpar layout existente
        if self.scroll_widget.layout():
            QWidget().setLayout(self.scroll_widget.layout())
        
        if self.is_two_columns:
            # Layout em grid (2 colunas)
            grid_layout = QGridLayout(self.scroll_widget)
            grid_layout.setSpacing(10)
            grid_layout.setContentsMargins(0, 0, 10, 0)
            
            # Calcular altura necessária para 4 cards (2 linhas x 2 colunas)
            card_height = 70  # Altura de cada card
            spacing = 10      # Espaçamento entre cards
            rows_visible = 2  # Número de linhas visíveis
            
            # Altura total necessária para mostrar 4 cards
            total_height = (rows_visible * card_height) + ((rows_visible - 1) * spacing)
            
            # Definir altura fixa para o scroll widget mostrar apenas 4 cards
            self.scroll_widget.setMinimumHeight(total_height + 20)  # +20 para padding
            
        else:
            # Layout vertical (1 coluna)
            grid_layout = QVBoxLayout(self.scroll_widget)
            grid_layout.setSpacing(10)
            grid_layout.setContentsMargins(0, 0, 10, 0)
            
            # Para 1 coluna, permitir altura automática
            self.scroll_widget.setMinimumHeight(0)

        # Dados de exemplo (mais itens para testar o scroll)
        example_files = [
            {
                "title": "Video 1",
                "format": "MP4 - 1080P",
                "time": "01:00",
                "size": "450Mb"
            },
            {
                "title": "Video 2",
                "format": "MP4 - 720P",
                "time": "02:30",
                "size": "320Mb"
            },
            {
                "title": "Video 3",
                "format": "MP4 - 1080P",
                "time": "03:45",
                "size": "680Mb"
            },
            {
                "title": "Video 4",
                "format": "MP4 - 720P",
                "time": "01:15",
                "size": "280Mb"
            },
            {
                "title": "Video 5",
                "format": "MP4 - 1080P",
                "time": "04:20",
                "size": "720Mb"
            },
            {
                "title": "Video 6",
                "format": "MP4 - 720P",
                "time": "02:10",
                "size": "340Mb"
            },
            {
                "title": "Video 7",
                "format": "MP4 - 1080P",
                "time": "05:30",
                "size": "890Mb"
            },
            {
                "title": "Video 8",
                "format": "MP4 - 720P",
                "time": "01:45",
                "size": "260Mb"
            }
        ]

        # Adicionar cards ao layout
        for i, file_data in enumerate(example_files):
            card = self.create_file_card(file_data)
            
            if self.is_two_columns:
                row = i // 2
                col = i % 2
                grid_layout.addWidget(card, row, col)
            else:
                grid_layout.addWidget(card)

        if self.is_two_columns:
            # Adicionar stretch no final para grid
            grid_layout.setRowStretch(grid_layout.rowCount(), 1)
        else:
            # Adicionar stretch no final para layout vertical
            grid_layout.addStretch()
    
    def create_file_card(self, file_data):
        """Cria um card individual para cada arquivo"""
        card = QWidget()
        card.setFixedHeight(70)  # Altura ajustada
        card.setStyleSheet(HistoryStyleSheet.file_card_style())
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # Ícone de play com imagem
        play_icon = QLabel()
        play_icon.setFixedSize(50, 50)
        play_icon.setStyleSheet(HistoryStyleSheet.play_icon_style())
        
        # Carregar ícone da pasta
        pixmap = QPixmap("images/icons/play_icon.png")
        if not pixmap.isNull():
            play_icon.setPixmap(pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            play_icon.setText("▶")
        
        play_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(play_icon)

        # Informações do arquivo - Layout vertical
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        info_layout.setContentsMargins(0, 0, 0, 0)

        # Título
        title_label = QLabel(file_data["title"])
        title_label.setStyleSheet(HistoryStyleSheet.file_title_style())
        info_layout.addWidget(title_label)
        
        # Linha com formato e tempo
        first_line = QHBoxLayout()
        first_line.setSpacing(20)
        first_line.setContentsMargins(0, 0, 0, 0)
        
        format_label = QLabel(file_data['format'])
        format_label.setStyleSheet(HistoryStyleSheet.file_details_style())
        
        time_label = QLabel(f"Time: {file_data['time']}")
        time_label.setStyleSheet(HistoryStyleSheet.file_details_style())
        
        first_line.addWidget(format_label)
        first_line.addWidget(time_label)
        first_line.addStretch()
        
        # Linha com tamanho
        size_label = QLabel(f"Size: {file_data['size']}")
        size_label.setStyleSheet(HistoryStyleSheet.file_details_style())
        
        info_layout.addLayout(first_line)
        info_layout.addWidget(size_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()

        # Botão de deletar com ícone
        delete_btn = QPushButton()
        delete_btn.setFixedSize(30, 30)
        
        # Carregar ícone da lixeira
        delete_pixmap = QPixmap("images/icons/delete_icon.png")
        if not delete_pixmap.isNull():
            delete_icon = QIcon(delete_pixmap)
            delete_btn.setIcon(delete_icon)
            delete_btn.setIconSize(delete_btn.size())
        else:
            delete_btn.setText("🗑️")
            
        delete_btn.setStyleSheet(HistoryStyleSheet.delete_button_style())
        layout.addWidget(delete_btn)

        return card
    
    def toggle_columns(self):
        """Alterna entre layout de 1 e 2 colunas"""
        self.is_two_columns = not self.is_two_columns
        self.create_cards_layout()
    
    def toggle_history(self):   
        if self.history_content.isVisible():
            # Esconder o histórico
            self.history_content.hide()
            # Alterar ícone para seta para baixo (indicando expandir)
            down_icon = QIcon("images/icons/down_icon.png")
            self.toggle_btn.setIcon(down_icon)
            
            # Emitir sinal que o histórico foi recolhido
            self.history_collapsed.emit()
        else:
            # Mostrar o histórico expandido
            main_app = self
            while main_app.parent() is not None:
                main_app = main_app.parent()
            
            # Calcular altura disponível subtraindo apenas a altura da barra de título
            title_bar_height = 30  # Altura da barra de título
            
            # Calcular altura disponível (altura total - barra de título - altura do header_bar)
            # Subtrai a altura da barra de título (navbar) para não sobrepô-la
            available_height = main_app.height() - title_bar_height - self.header_bar.height()
            
            # Definir altura do conteúdo para preencher todo o espaço disponível abaixo do navbar
            self.history_content.setFixedHeight(available_height)
            
            # Mostrar o conteúdo
            self.history_content.show()
            
            # Alterar ícone para seta para cima (indicando recolher)
            up_icon = QIcon("images/icons/up_icon.png")
            self.toggle_btn.setIcon(up_icon)
            
            # Não usamos raise_() para não sobrepor o navbar
            
            # Emitir sinal que o histórico foi expandido
            self.history_expanded.emit()