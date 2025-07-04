class HomeStyleSheet:
    """Classe para centralizar todos os estilos da Home GUI"""
    
    # Cores principais da aplicação
    PRIMARY_COLOR = "#008080"
    PRIMARY_HOVER = "#006666"
    SECONDARY_COLOR = "#01716F"
    BACKGROUND_COLOR = "#f5f5f5"
    WHITE_COLOR = "#ffffff"
    TEXT_COLOR = "#666"
    DARK_TEXT = "#343434"
    BORDER_COLOR = "#cccccc"
    FOCUS_COLOR = "#008080"
    
    @staticmethod
    def main_widget_style():
        """Estilo principal da aplicação"""
        return f"""
            QWidget {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
                background-color: {HomeStyleSheet.BACKGROUND_COLOR};
            }}
            QLabel {{
                font-weight: 500;
                margin-bottom: 0px;
            }}
        """
    
    @staticmethod
    def tab_widget_style():
        """Estilo para o widget de abas"""
        return f"""
            QTabWidget::pane {{
                border: none;
                background-color: {HomeStyleSheet.BACKGROUND_COLOR};
            }}
            QTabBar::tab {{
                padding: 10px 20px;
                background: #f8f8f8;
                border-bottom: 2px solid transparent;
                color: {HomeStyleSheet.TEXT_COLOR};
            }}
            QTabBar::tab:selected {{
                border-bottom: 2px solid {HomeStyleSheet.PRIMARY_COLOR};
                color: {HomeStyleSheet.PRIMARY_COLOR};
                font-weight: bold;
                color: {HomeStyleSheet.DARK_TEXT};
            }}
        """
    
    @staticmethod
    def line_edit_style():
        """Estilo para campos de entrada de texto"""
        return f"""
            QLineEdit {{
                padding: 8px;
                border: 1px solid {HomeStyleSheet.BORDER_COLOR};
                border-radius: 7px;
                background: #e9e9e9;
                color: #888;
                font-size: 15px;
            }}
            QLineEdit:focus {{
                outline: none;
                border: 1.5px solid {HomeStyleSheet.FOCUS_COLOR};
                background: #f8f8f8;
                color: #222;
            }}
        """
    
    @staticmethod
    def primary_button_style():
        """Estilo para botões primários"""
        return f"""
            QPushButton {{
                padding: 10px 28px;
                background-color: {HomeStyleSheet.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 7px;
                font-size: 15px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {HomeStyleSheet.PRIMARY_HOVER};
            }}
        """
    
    @staticmethod
    def title_bar_style():
        """Estilo para a barra de título personalizada"""
        return f"""
            QWidget {{
                background: {HomeStyleSheet.SECONDARY_COLOR};
            }}
        """
    
    @staticmethod
    def title_bar_button_style():
        """Estilo para botões da barra de título"""
        return """
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """
    
    @staticmethod
    def paste_button_style():
        """Estilo específico para o botão Paste Here"""
        return f"""
            QPushButton {{
                background-color: {HomeStyleSheet.PRIMARY_COLOR};
                border: none;
                border-radius: 7px;
            }}
            QPushButton:hover {{
                background-color: {HomeStyleSheet.PRIMARY_HOVER};
            }}
        """
    
    @staticmethod
    def paste_button_text_style():
        """Estilo para o texto dentro do botão Paste"""
        return "color: white; background: transparent; font-weight: 500;"
    
    @staticmethod
    def home_label_style():
        """Estilo para o label da home"""
        return f"""
            QLabel {{
                font-size: 16px;
                color: {HomeStyleSheet.TEXT_COLOR};
                margin-top: 10px;
            }}
        """
    
    @staticmethod
    def account_box_style():
        """Estilo para a caixa de informações da conta"""
        return f"""
            QWidget {{
                background-color: {HomeStyleSheet.WHITE_COLOR};
                border-radius: 10px;
            }}
        """
    
    @staticmethod
    def status_badge_style():
        """Estilo para o badge de status Premium"""
        return """
            QLabel {
                background-color: #d1fae5;
                color: #065f46;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 13px;
            }
        """
    
    @staticmethod
    def manage_subscription_button_style():
        """Estilo para o botão de gerenciar assinatura"""
        return f"""
            QPushButton {{
                background-color: {HomeStyleSheet.PRIMARY_HOVER};
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #004d4d;
            }}
        """
    
    @staticmethod
    def icon_transparent_style():
        """Estilo para ícones com fundo transparente"""
        return "background: transparent;"