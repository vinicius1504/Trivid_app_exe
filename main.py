from PySide6.QtWidgets import QApplication
import sys
from src.GUI.home_GUI import MediaDownloaderPro  # Importa sua interface principal

def main():
    app = QApplication(sys.argv)  # Inicia o app Qt
    window = MediaDownloaderPro()  # Cria a janela principal (com abas: Home e Settings)
    window.show()  # Mostra a janela
    sys.exit(app.exec())  # Executa o app
    
if __name__ == "__main__":
    main()