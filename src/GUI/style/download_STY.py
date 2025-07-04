class StyleSheet:
    """Classe para centralizar todos os estilos da aplicação"""
    
    # Cores da aplicação
    PRIMARY_COLOR = "#006666"
    SECONDARY_COLOR = "#008080"
    HOVER_COLOR = "#004d4d"
    BACKGROUND_COLOR = "#f5f5f5"
    TEXT_COLOR = "#333"
    BORDER_COLOR = "#ccc"
    
    @staticmethod
    def radio_button_style():
        """Estilo para radio buttons sem hover azul"""
        return """
            QRadioButton {
                color: black;
                font-size: 14px;
                padding: 5px;
            }
            QRadioButton:hover {
                background-color: transparent;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #999;
                border-radius: 7px;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #006666;
                border-radius: 7px;
                background-color: #006666;
            }
            QRadioButton::indicator:hover {
                border-color: #006666;
            }
        """
    
    @staticmethod
    def primary_button_style(color=None):
        """Estilo para botões primários com cor customizável"""
        button_color = color or StyleSheet.PRIMARY_COLOR
        return f"""
            QPushButton {{  
                background-color: {button_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {button_color}CC;
            }}
        """
    
    @staticmethod
    def secondary_button_style():
        """Estilo para botões secundários"""
        return f"""
            QPushButton {{
                background-color: {StyleSheet.BACKGROUND_COLOR};
                color: {StyleSheet.TEXT_COLOR};
                border: 1px solid {StyleSheet.BORDER_COLOR};
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
        """
    
    @staticmethod
    def browse_button_style():
        """Estilo para botão Browse"""
        return f"""
            QPushButton {{
                background-color: {StyleSheet.BACKGROUND_COLOR};
                border: 1px solid {StyleSheet.BORDER_COLOR};
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
        """
    
    @staticmethod
    def label_bold_style():
        """Estilo para labels em negrito"""
        return "font-weight: bold;"
    
    @staticmethod
    def label_title_style():
        """Estilo para títulos de seções"""
        return "font-weight: bold; margin-top: 10px;"
    
    @staticmethod
    def platform_icon_style(color):
        """Estilo para ícones de plataforma"""
        return f"color: {color}; font-size: 16px;"
    
    @staticmethod
    def platform_value_style(color):
        """Estilo para valores de plataforma"""
        return f"font-weight: bold; margin-left: 5px; color: {color};"