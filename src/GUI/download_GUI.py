import sys
import os
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QComboBox, QRadioButton, 
                               QButtonGroup, QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QPixmap
from pytubefix import YouTube

# Importar todos os downloaders
from src.core.downloders.youtube_downloader import baixar_video_audio_mesclar, baixar_audio, baixar_thumbnail
from src.core.downloders.twitch_downloader import baixar_video_twitch, baixar_audio_twitch, baixar_thumbnail_twitch
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
    
    def handle_spotify_download(self, selected_id, output_folder):
        # Spotify só tem áudio (e imagem de capa)
        if selected_id == 0:  # Tentou baixar vídeo
            QMessageBox.warning(self, "Aviso", "Spotify não suporta vídeos. Tentando baixar áudio...")
            selected_id = 1
        
        # AUDIO
        if selected_id == 1:
            try:
                format_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                formato = format_combo.currentText().lower()
            except Exception:
                formato = "mp3"
            # Substitua esta linha quando implementar o módulo de spotify
            # caminho = baixar_audio_spotify(self.video_url, output_folder, formato)
            caminho = None
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download de áudio concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download de áudio do Spotify.")

        # IMAGEM
        elif selected_id == 2:
            try:
                format_combo = self.options_layout.itemAt(0).layout().itemAt(0).layout().itemAt(1).widget()
                formato = format_combo.currentText().lower()
            except Exception:
                formato = "jpg"
            # Substitua esta linha quando implementar o módulo de spotify
            # caminho = baixar_thumbnail_spotify(self.video_url, output_folder, formato)
            caminho = None
            if caminho:
                QMessageBox.information(self, "Sucesso", f"Download da capa concluído:\n{caminho}")
            else:
                QMessageBox.critical(self, "Erro", "Falha no download da capa do Spotify.")

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
        
    def update_options_section(self):
        """
        Atualiza as opções com base no tipo de conteúdo selecionado
        """
        # Limpa todos os widgets e sublayouts do options_layout
        while self.options_layout.count():
            item = self.options_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
        
        # Adiciona a nova seção de opções
        selected_id = self.button_group.checkedId()
        
        if selected_id == 0:  # Vídeo
            self.add_video_options()
        elif selected_id == 1:  # Áudio
            self.add_audio_options()
        elif selected_id == 2:  # Imagem
            self.add_image_options()

    def clear_layout(self, layout):
        """
        Remove todos os itens de um layout
        """
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def add_video_options(self):
        """
        Adiciona opções para download de vídeo
        """
        # Primeira linha de opções
        first_row = QHBoxLayout()
        first_row.setSpacing(8)
        
        # Resolução
        resolution_layout = QVBoxLayout()
        resolution_label = QLabel("Resolution")
        resolution_label.setStyleSheet("font-weight: bold;")
        resolution_combo = QComboBox()
        
        if self.platform == 'youtube':
            resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        elif self.platform == 'twitch':
            resolutions = ["160p", "360p", "480p", "720p", "1080p",]
        else:
            resolutions = ["360p", "480p", "720p", "1080p"]
            
        resolution_combo.addItems(resolutions)
        resolution_combo.setFixedWidth(120)
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(resolution_combo)
        
        # Formato
        format_layout = QVBoxLayout()
        format_label = QLabel("Format")
        format_label.setStyleSheet("font-weight: bold;")
        format_combo = QComboBox()
        format_combo.addItems(["MP4", "MKV", "AVI", "WEBM"])
        format_combo.setFixedWidth(120)
        format_layout.addWidget(format_label)
        format_layout.addWidget(format_combo)
        
        first_row.addLayout(resolution_layout)
        first_row.addLayout(format_layout)
        first_row.addStretch()
        
        self.options_layout.addLayout(first_row)
        
    def add_audio_options(self):
        """
        Adiciona opções para download de áudio
        """
        # Primeira linha de opções
        first_row = QHBoxLayout()
        first_row.setSpacing(8)
        
        # Formato de áudio
        format_layout = QVBoxLayout()
        format_label = QLabel("Format")
        format_label.setStyleSheet("font-weight: bold;")
        format_combo = QComboBox()
        format_combo.addItems(["MP3", "WAV", "AAC", "FLAC", "OGG"])
        format_combo.setFixedWidth(120)
        format_layout.addWidget(format_label)
        format_layout.addWidget(format_combo)
        
        # Bitrate
        bitrate_layout = QVBoxLayout()
        bitrate_label = QLabel("Bitrate")
        bitrate_label.setStyleSheet("font-weight: bold;")
        bitrate_combo = QComboBox()
        bitrate_combo.addItems(["128 kbps", "192 kbps", "256 kbps", "320 kbps"])
        bitrate_combo.setFixedWidth(120)
        bitrate_layout.addWidget(bitrate_label)
        bitrate_layout.addWidget(bitrate_combo)
        
        first_row.addLayout(format_layout)
        first_row.addLayout(bitrate_layout)
        first_row.addStretch()
        
        self.options_layout.addLayout(first_row)
    
    def add_image_options(self):
        """
        Adiciona opções para download de imagem
        """
        row = QHBoxLayout()
        row.setSpacing(8)
        
        # Formato de imagem
        format_layout = QVBoxLayout()
        format_label = QLabel("Format")
        format_label.setStyleSheet("font-weight: bold;")
        format_combo = QComboBox()
        format_combo.addItems(["JPG", "PNG", "WEBP"])
        format_combo.setFixedWidth(120)
        format_layout.addWidget(format_label)
        format_layout.addWidget(format_combo)
        
        
        row.addLayout(format_layout)
        row.addStretch()
        
        self.options_layout.addLayout(row)
    
    def create_destination_section(self):
        layout = QVBoxLayout()
        title_label = QLabel("Destination Folder")
        title_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(title_label)

        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit(self.output_folder)
        self.folder_input.setFixedHeight(35)
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(80, 35)
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        browse_button.clicked.connect(self.browse_folder)

        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_button)
        layout.addLayout(folder_layout)
        return layout

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.folder_input.text())
        if folder:
            self.folder_input.setText(folder)
            self.output_folder = folder

    def load_video_info(self, url):
        """
        Carrega informações do vídeo de acordo com a plataforma
        """
        try:
            if self.platform == 'youtube':
                self.yt = YouTube(url)
                self.update_youtube_info()
            # Implementar para outras plataformas
            # elif self.platform == 'twitch':
            #    self.update_twitch_info()
            # elif self.platform == 'spotify':
            #    self.update_spotify_info()
            
            # Inicializa as opções baseadas no tipo de conteúdo selecionado
            self.update_options_section()
        except Exception as e:
            print(f"Erro ao carregar informações: {e}")

    def update_youtube_info(self):
        """
        Atualiza a interface com informações do YouTube
        """
        if not self.yt:
            return
            
        try:
            self.title_label.setText(self.yt.title)
            self.channel_label.setText(self.yt.author)
            
            # Formata a duração
            duration = self.yt.length
            mins, secs = divmod(duration, 60)
            self.duration_label.setText(f"Duration: {mins}:{secs:02d}")
            
            # Carrega a thumbnail
            try:
                response = requests.get(self.yt.thumbnail_url)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(QByteArray(response.content))
                    pixmap = pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.thumbnail_label.setPixmap(pixmap)
            except Exception as e:
                print(f"Erro ao carregar thumbnail: {e}")
        except Exception as e:
            print(f"Erro ao atualizar informações do YouTube: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()