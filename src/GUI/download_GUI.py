import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QComboBox, QRadioButton, 
                               QButtonGroup, QLineEdit, QPushButton, QProgressBar, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pytubefix import YouTube
from src.core.youtube_downloader import baixar_video_audio_mesclar, baixar_audio, baixar_thumbnail



class VideoDownloaderWidget(QWidget):
    def __init__(self, video_url=None):
        super().__init__()
        self.yt = None
        self.video_streams = []
        self.audio_streams = []
        self.video_url = video_url
        self.output_folder = ""  # <-- Adicione esta linha antes de chamar init_ui
        self.init_ui()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Só mostra durante o download
        self.layout.addWidget(self.progress_bar)
        if self.video_url:
            self.load_video_info(self.video_url)
    
    def init_ui(self):
        self.layout = QVBoxLayout(self)
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
        # Add the button row here
        self.button_row = self.create_button_row()
        self.layout.addLayout(self.button_row)
        self.layout.addStretch()

    def create_button_row(self):
        layout = QHBoxLayout()
        download_btn = QPushButton("Download")
        cancel_btn = QPushButton("Cancel")
        # Estilo dos botões
        btn_style = """
            QPushButton {
                background-color: #008080;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #006666;
            }
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
        return layout

    def handle_download(self):
        if not self.video_url:
            return

        selected_id = self.button_group.checkedId()
        output_folder = self.folder_input.text().strip()
        if not output_folder:
            import os
            output_folder = os.path.expanduser("~/Downloads")

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

    def create_destination_section(self):
        layout = QVBoxLayout()
        title_label = QLabel("Destination Folder")
        title_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(title_label)

        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit(self.output_folder)  # Salve como atributo
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

        browse_button.clicked.connect(self.browse_folder)  # Conecte o botão

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
        try:
            self.yt = YouTube(url)
            self.video_streams = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            self.audio_streams = self.yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
            self.update_video_info_fields()
            self.create_options_section()  # <-- Adicione esta linha para mostrar as opções ao carregar o vídeo
        except Exception as e:
            print(f"Erro ao carregar vídeo: {e}")

    def update_video_info_fields(self):
        # Atualize os labels do vídeo com os dados reais
        if self.yt:
            self.title_label.setText(self.yt.title)
            self.channel_label.setText(self.yt.author)
            duration = self.yt.length
            mins, secs = divmod(duration, 60)
            self.duration_label.setText(f"Duration: {mins}:{secs:02d}")
            # Exibir thumbnail
            import requests
            from PySide6.QtCore import QByteArray
            thumb_url = self.yt.thumbnail_url
            try:
                response = requests.get(thumb_url)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(QByteArray(response.content))
                    pixmap = pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.thumbnail_label.setPixmap(pixmap)
            except Exception as e:
                print("Erro ao carregar thumbnail:", e)

    def create_video_info_section(self):
        layout = QHBoxLayout()
        self.thumbnail_label = QLabel()  # Salve como atributo
        self.thumbnail_label.setFixedSize(120, 90)
        self.thumbnail_label.setStyleSheet("background-color: #20B2AA; border-radius: 5px;")

        # Info
        info_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        youtube_icon = QLabel("🎥")
        youtube_icon.setStyleSheet("color: red; font-size: 16px;")
        self.title_label = QLabel("Carregando título...")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_layout.addWidget(youtube_icon)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        self.channel_label = QLabel("Carregando canal...")
        self.channel_label.setStyleSheet("color: gray; font-size: 12px;")
        self.duration_label = QLabel("Duration: --:--")
        self.duration_label.setStyleSheet("color: gray; font-size: 12px;")
        platform_layout = QHBoxLayout()
        platform_label = QLabel("Platform:")
        platform_value = QLabel("YouTube")
        platform_value.setStyleSheet("font-weight: bold; margin-left: 5px;")
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
        
        # Section title
        title_label = QLabel("Select content type:")
        title_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(title_label)
        
        # Radio buttons
        radio_layout = QHBoxLayout()
        self.button_group = QButtonGroup()
        
        video_radio = QRadioButton("Video")
        audio_radio = QRadioButton("Audio")
        image_radio = QRadioButton("Image")
        
        video_radio.setChecked(True)  # Default selection
        
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
        # Limpa todos os widgets e sublayouts do options_layout
        while self.options_layout.count():
            item = self.options_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
        # Adiciona a nova seção de opções
        self.create_options_section()

    def clear_layout(self, layout):
        # Função auxiliar para limpar layouts aninhados
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def create_options_section(self):
        # Detect selected content type
        selected_id = self.button_group.checkedId()
        if selected_id == 1:  # Audio
            self.add_audio_options()
        elif selected_id == 2:  # Image
            self.add_image_options()
        else:
            self.add_video_image_options()

    def add_audio_options(self):
        first_row = QHBoxLayout()
        first_row.setSpacing(8)
        # Format
        format_layout = QVBoxLayout()
        format_label = QLabel("Format")
        format_label.setStyleSheet("font-weight: bold;")
        format_combo = QComboBox()
        format_combo.addItems(["MP3", "WAV", "AAC", "FLAC"])
        format_combo.setFixedWidth(120)  # Mais compacto
        format_layout.addWidget(format_label)
        format_layout.addWidget(format_combo)
        # Bitrate
        bitrate_layout = QVBoxLayout()
        bitrate_label = QLabel("Bitrate")
        bitrate_label.setStyleSheet("font-weight: bold;")
        bitrate_combo = QComboBox()
        bitrate_combo.addItems(["320 kbps", "256 kbps", "192 kbps", "128 kbps"])
        bitrate_combo.setFixedWidth(120)
        bitrate_layout.addWidget(bitrate_label)
        bitrate_layout.addWidget(bitrate_combo)
        first_row.addLayout(format_layout)
        first_row.addSpacing(8)
        first_row.addLayout(bitrate_layout)
        first_row.addStretch()
        # Estimated Size
        size_layout = QVBoxLayout()
        size_label = QLabel("Estimated Size")
        size_label.setStyleSheet("font-weight: bold;")
        size_display = QLineEdit("~8 MB")
        size_display.setReadOnly(True)
        size_display.setFixedWidth(120)
        size_display.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        size_layout.addWidget(size_label)
        size_layout.addWidget(size_display)
        self.options_layout.addLayout(first_row)
        self.options_layout.addSpacing(6)
        self.options_layout.addLayout(size_layout)

    def add_video_image_options(self):
        first_row = QHBoxLayout()
        first_row.setSpacing(8)
        resolution_layout = QVBoxLayout()
        resolution_label = QLabel("Resolution")
        resolution_label.setStyleSheet("font-weight: bold;")
        resolution_combo = QComboBox()
        resolution_combo.setFixedWidth(120)  # Mais compacto
        # Preencher dinamicamente as resoluções disponíveis
        resolutions = set()
        if self.yt:
            # Streams progressivos (vídeo+áudio)
            for s in self.yt.streams.filter(progressive=True, file_extension='mp4'):
                if s.resolution:
                    resolutions.add(s.resolution)
            # Streams só vídeo (para 720p+)
            for s in self.yt.streams.filter(only_video=True, file_extension='mp4'):
                if s.resolution:
                    resolutions.add(s.resolution)
        # Ordenar resoluções do maior para o menor
        resolutions = sorted(resolutions, key=lambda x: int(x.replace('p','')), reverse=True)
        for res in resolutions:
            resolution_combo.addItem(res)
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(resolution_combo)
        format_layout = QVBoxLayout()
        format_label = QLabel("Format")
        format_label.setStyleSheet("font-weight: bold;")
        format_combo = QComboBox()
        format_combo.addItems([
            "MP4", "AVI", "MKV", "WEBM",
        ])
        format_combo.setFixedWidth(120)
        format_layout.addWidget(format_label)
        format_layout.addWidget(format_combo)
        first_row.addLayout(resolution_layout)
        first_row.addSpacing(8)
        first_row.addLayout(format_layout)
        first_row.addStretch()
        second_row = QHBoxLayout()
        second_row.setSpacing(8)
        codec_layout = QVBoxLayout()
        codec_label = QLabel("Codec")
        codec_label.setStyleSheet("font-weight: bold;")
        codec_combo = QComboBox()
        codec_combo.addItems([
            "H.264", "H.265", "VP9", "AV1",
            "MP3", "AAC", "WAV", "FLAC",
            "JPEG", "PNG", "BMP", "GIF"
        ])
        codec_combo.setFixedWidth(120)
        codec_layout.addWidget(codec_label)
        codec_layout.addWidget(codec_combo)
        size_layout = QVBoxLayout()
        size_label = QLabel("Estimated Size")
        size_label.setStyleSheet("font-weight: bold;")
        size_display = QLineEdit("~120 MB")
        size_display.setReadOnly(True)
        size_display.setFixedWidth(120)
        size_display.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        size_layout.addWidget(size_label)
        size_layout.addWidget(size_display)
        second_row.addLayout(codec_layout)
        second_row.addSpacing(8)
        second_row.addLayout(size_layout)
        second_row.addStretch()
        self.options_layout.addLayout(first_row)
        self.options_layout.addSpacing(6)
        self.options_layout.addLayout(second_row)

    def add_image_options(self):
        row = QHBoxLayout()
        row.setSpacing(8)
        format_layout = QVBoxLayout()
        format_label = QLabel("Format")
        format_label.setStyleSheet("font-weight: bold;")
        format_combo = QComboBox()
        format_combo.addItems(["JPG", "PNG", "BMP", "GIF"])
        format_combo.setFixedWidth(120)
        format_layout.addWidget(format_label)
        format_layout.addWidget(format_combo)
        size_layout = QVBoxLayout()
        size_label = QLabel("Estimated Size")
        size_label.setStyleSheet("font-weight: bold;")
        size_display = QLineEdit("~0.5 MB")
        size_display.setReadOnly(True)
        size_display.setFixedWidth(120)
        size_display.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        size_layout.addWidget(size_label)
        size_layout.addWidget(size_display)
        row.addLayout(format_layout)
        row.addLayout(size_layout)
        row.addStretch()
        self.options_layout.addLayout(row)

class MainWindow(QMainWindow):
    def __init__(self, video_url=None):
        super().__init__()
        self.setWindowTitle("Video Downloader")
        self.setFixedSize(500, 405)
        
        # Create central widget
        central_widget = VideoDownloaderWidget(video_url)
        self.setCentralWidget(central_widget)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLabel {
                font-family: Arial, sans-serif;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 5px;
            }
            QRadioButton {
                font-size: 12px;
                spacing: 5px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 12px;
            }
        """)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()