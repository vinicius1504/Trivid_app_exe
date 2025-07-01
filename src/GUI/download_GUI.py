import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QComboBox, QRadioButton, 
                               QButtonGroup, QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pytubefix import YouTube

# Importar todos os downloaders
from src.core.youtube_downloader import baixar_video_audio_mesclar, baixar_audio, baixar_thumbnail
from src.core.twitch_downloader import baixar_video_twitch, baixar_audio_twitch, baixar_thumbnail_twitch
# from src.core.spotify_downloader import baixar_audio_spotify, baixar_video_spotify, baixar_thumbnail_spotify
from src.core.detector_link import get_platform_info


class MainWindow(QMainWindow):
    def __init__(self, video_url=None, platform='youtube'):
        super().__init__()
        self.video_url = video_url
        self.platform = platform
        self.platform_info = get_platform_info(platform)
        self.yt = None
        self.output_folder = os.path.expanduser("~/Downloads")
        
        self.setWindowTitle(f"TriviD - {self.platform_info['name']} Downloader")
        self.setFixedSize(500, 405)
        
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Inicializar a UI
        self.setup_content_ui(central_widget)
        
        # Carregar informações do vídeo se URL foi fornecida
        if self.video_url:
            self.load_video_info(self.video_url)
    
    def setup_content_ui(self, parent_widget):
        """Configura a UI do conteúdo principal"""
        self.layout = QVBoxLayout(parent_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Seção de informações do vídeo
        self.video_info_section = self.create_video_info_section()
        self.layout.addLayout(self.video_info_section)
        
        # Seção de tipo de conteúdo (rádios)
        self.content_type_section = self.create_content_type_section()
        self.layout.addLayout(self.content_type_section)
        
        # Seção de opções
        self.options_layout = QVBoxLayout()
        self.layout.addLayout(self.options_layout)
        
        # Seção de destino
        self.destination_section = self.create_destination_section()
        self.layout.addLayout(self.destination_section)
        
        # Botões
        self.button_row = self.create_button_row()
        self.layout.addLayout(self.button_row)
        
        self.layout.addStretch()

    def create_button_row(self):
        layout = QHBoxLayout()
        download_btn = QPushButton("Download")
        cancel_btn = QPushButton("Cancel")
        
        # Usar cor da plataforma para o botão
        btn_style = f"""
            QPushButton {{
                background-color: {self.platform_info['button_color']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.platform_info['button_color']}CC;
            }}
        """
        download_btn.setStyleSheet(btn_style)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #333;
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        layout.addStretch()
        layout.addWidget(cancel_btn)
        layout.addWidget(download_btn)
        download_btn.clicked.connect(self.handle_download)
        cancel_btn.clicked.connect(self.close)
        return layout

    def handle_download(self):
        if not self.video_url:
            return

        selected_id = self.button_group.checkedId()
        output_folder = self.folder_input.text().strip()
        if not output_folder:
            output_folder = os.path.expanduser("~/Downloads")

        # Escolher o downloader baseado na plataforma
        if self.platform == 'youtube':
            self.handle_youtube_download(selected_id, output_folder)
        elif self.platform == 'twitch':
            self.handle_twitch_download(selected_id, output_folder)
        elif self.platform == 'spotify':
            self.handle_spotify_download(selected_id, output_folder)

    def handle_youtube_download(self, selected_id, output_folder):
        # VIDEO
        if selected_id == 0:
            try:
                resolution_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                format_combo = self.options_layout.itemAt(0).layout().itemAt(2).layout().itemAt(1).widget()
                resolucao = resolution_combo.currentText().split()[0]
                formato = format_combo.currentText().lower()
            except Exception:
                resolucao = "360p"
                formato = "mp4"
            caminho = baixar_video_audio_mesclar(self.video_url, resolucao, output_folder, formato)
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download de vídeo.")

        # AUDIO
        elif selected_id == 1:
            try:
                format_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                formato = format_combo.currentText().lower()
            except Exception:
                formato = "mp3"
            caminho = baixar_audio(self.video_url, output_folder, formato)
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download de áudio concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download de áudio.")

        # IMAGEM
        elif selected_id == 2:
            try:
                format_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                formato = format_combo.currentText().lower()
            except Exception:
                formato = "jpg"
            caminho = baixar_thumbnail(self.video_url, output_folder, formato)
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download da thumbnail concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download da thumbnail.")

    def handle_twitch_download(self, selected_id, output_folder):
        # VIDEO
        if selected_id == 0:
            try:
                resolution_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                format_combo = self.options_layout.itemAt(0).layout().itemAt(2).layout().itemAt(1).widget()
                resolucao = resolution_combo.currentText().split()[0]
                formato = format_combo.currentText().lower()
            except Exception:
                resolucao = "720p"
                formato = "mp4"
            caminho = baixar_video_twitch(self.video_url, resolucao, output_folder, formato)
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download de vídeo.")

        # AUDIO
        elif selected_id == 1:
            try:
                format_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                formato = format_combo.currentText().lower()
            except Exception:
                formato = "mp3"
            caminho = baixar_audio_twitch(self.video_url, output_folder, formato)
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download de áudio concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download de áudio.")

        # IMAGEM
        elif selected_id == 2:
            try:
                format_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                formato = format_combo.currentText().lower()
            except Exception:
                formato = "jpg"
            caminho = baixar_thumbnail_twitch(self.video_url, output_folder, formato)
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download da thumbnail concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download da thumbnail.")

    def create_video_info_section(self):
        layout = QHBoxLayout()
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(120, 90)
        # Usar cor da plataforma para o fundo
        self.thumbnail_label.setStyleSheet(f"background-color: {self.platform_info['color']}; border-radius: 5px;")

        # Info
        info_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        # Usar ícone da plataforma
        platform_icon = QLabel(self.platform_info['icon'])
        platform_icon.setStyleSheet(f"color: {self.platform_info['color']}; font-size: 16px;")
        self.title_label = QLabel("Carregando título...")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_layout.addWidget(platform_icon)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        self.channel_label = QLabel("Carregando canal...")
        self.channel_label.setStyleSheet("color: gray; font-size: 12px;")
        self.duration_label = QLabel("Duration: --:--")
        self.duration_label.setStyleSheet("color: gray; font-size: 12px;")
        
        platform_layout = QHBoxLayout()
        platform_label = QLabel("Platform:")
        # Usar nome e cor da plataforma
        platform_value = QLabel(self.platform_info['name'])
        platform_value.setStyleSheet(f"font-weight: bold; margin-left: 5px; color: {self.platform_info['color']};")
        platform_layout.addWidget(platform_label)
        platform_layout.addWidget(platform_value)
        platform_layout.addStretch()
        
        info_layout.addLayout(title_layout)
        info_layout.addWidget(self.channel_label)
        info_layout.addWidget(self.duration_label)
        info_layout.addSpacing(10)
        info_layout.addLayout(platform_layout)
        layout.addWidget(self.thumbnail_label)
        layout.addSpacing(15)
        layout.addLayout(info_layout)

        return layout

    def create_content_type_section(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("Select content type:")
        title_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(title_label)
        
        radio_layout = QHBoxLayout()
        self.button_group = QButtonGroup()
        
        video_radio = QRadioButton("Video")
        audio_radio = QRadioButton("Audio")
        image_radio = QRadioButton("Image")
        
        # Para Spotify, desabilitar vídeo por padrão
        if self.platform == 'spotify':
            audio_radio.setChecked(True)
            video_radio.setEnabled(False)
        else:
            video_radio.setChecked(True)
        
        self.button_group.addButton(video_radio, 0)
        self.button_group.addButton(audio_radio, 1)
        self.button_group.addButton(image_radio, 2)
        
        radio_layout.addWidget(video_radio)
        radio_layout.addWidget(audio_radio)
        radio_layout.addWidget(image_radio)
        radio_layout.addStretch()
        
        layout.addLayout(radio_layout)
        
        self.button_group.buttonClicked.connect(self.update_options_section)
        
        return layout

    # ... resto dos métodos permanecem iguais (create_destination_section, browse_folder, etc.)
    # ... métodos de opções (add_audio_options, add_video_options, etc.)