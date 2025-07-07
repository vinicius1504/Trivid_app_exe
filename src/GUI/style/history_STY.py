class HistoryStyleSheet:
    """Classe para centralizar todos os estilos da History GUI"""
    
    # Cores principais da aplicação
    PRIMARY_COLOR = "#008080"      # Cor principal (verde-azulado)
    PRIMARY_HOVER = "#006666"      # Cor quando passa o mouse por cima
    SECONDARY_COLOR = "#01716F"    # Cor secundária
    BACKGROUND_COLOR = "#f5f5f5"   # Cor de fundo geral
    WHITE_COLOR = "#ffffff"        # Branco puro
    TEXT_COLOR = "#666"            # Cor do texto padrão (cinza médio)
    DARK_TEXT = "#343434"          # Texto escuro
    BORDER_COLOR = "#cccccc"       # Cor das bordas (cinza claro)
    FOCUS_COLOR = "#008080"        # Cor quando elemento está em foco
    CARD_BG = "#f8f9fa"           # Cor de fundo dos cards
    CARD_HOVER = "#e9ecef"        # Cor dos cards quando passa o mouse
    CARD_BORDER = "#e9ecef"       # Cor da borda dos cards
    DELETE_HOVER = "#dc3545"      # Cor vermelha para botão deletar
    ICON_BG = "#6c757d"           # Cor de fundo dos ícones (cinza)
    
    @staticmethod
    def header_bar_style():
        """Barra superior do painel - cor de fundo e bordas arredondadas superiores"""
        return f"""
            QWidget {{
                background-color: {HistoryStyleSheet.PRIMARY_COLOR};  /* Fundo verde-azulado */
                border-top-left-radius: 10px;   /* Borda arredondada superior esquerda */
                border-top-right-radius: 10px;  /* Borda arredondada superior direita */
            }}
        """
    
    @staticmethod
    def history_title_style():
        """Estilo do texto 'History' - cor branca, negrito e tamanho"""
        return """
            QLabel {
                color: white;           /* Texto branco */
                font-weight: bold;      /* Texto em negrito */
                font-size: 16px;        /* Tamanho da fonte */
            }
        """
    
    @staticmethod
    def toggle_button_style():
        """Botão de expandir/recolher - transparente com hover sutil"""
        return """
            QPushButton {
                background: transparent;    /* Fundo transparente */
                border: none;              /* Sem borda */
            }   
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);  /* Fundo branco translúcido ao passar mouse */
                border-radius: 15px;       /* Bordas arredondadas */
            }
        """
    
    @staticmethod
    def history_content_style():
        """Container do conteúdo - fundo branco com bordas arredondadas inferiores"""
        return f"""
            QWidget {{
                background-color: {HistoryStyleSheet.WHITE_COLOR};  /* Fundo branco */
                border-bottom-left-radius: 10px;   /* Borda arredondada inferior esquerda */
                border-bottom-right-radius: 10px;  /* Borda arredondada inferior direita */
            }}
        """
    
    @staticmethod
    def scroll_area_style():
        """Área de scroll personalizada - barra de rolagem customizada"""
        return f"""
            QScrollArea {{
                border: none;              /* Sem borda na área de scroll */
                background: transparent;   /* Fundo transparente */
            }}
            QScrollBar:vertical {{
                background: #f0f0f0;      /* Fundo da barra de rolagem */
                width: 8px;               /* Largura da barra */
                border-radius: 4px;       /* Bordas arredondadas */
            }}
            QScrollBar::handle:vertical {{
                background: {HistoryStyleSheet.BORDER_COLOR};  /* Cor do "handle" (parte que arrasta) */
                border-radius: 4px;       /* Bordas arredondadas do handle */
            }}
        """
    
    @staticmethod
    def file_card_style():
        """Cards dos arquivos - fundo branco, bordas e hover"""
        return f"""
            QWidget {{
                background-color: {HistoryStyleSheet.WHITE_COLOR};  /* Fundo branco */
                border-radius: 10px;      /* Bordas arredondadas */
                border: 1px solid {HistoryStyleSheet.CARD_BORDER};  /* Borda cinza clara */
                height: 100px;            /* Altura fixa (ERRO: deveria ser height minúsculo) */
            }}
            QWidget:hover {{
                background-color: {HistoryStyleSheet.CARD_HOVER};  /* Cor quando passa o mouse */
            }}
        """

    @staticmethod
    def play_icon_style():
        """Ícone de play - círculo cinza com texto branco"""
        return f"""
            QLabel {{
                background-color: {HistoryStyleSheet.ICON_BG};  /* Fundo cinza */
                border-radius: 25px;      /* Formato circular (50x50 = raio 25) */
                color: white;             /* Cor do ícone/texto */
                font-size: 18px;          /* Tamanho do ícone */
            }}
        """

    @staticmethod
    def file_title_style():
        """Título do arquivo - texto em negrito e escuro"""
        return """
            QLabel {
                font-size: 14px;          /* Tamanho da fonte */
                font-weight: bold;        /* Texto em negrito */
                color: #212529;           /* Cor escura */
            }
        """

    @staticmethod
    def file_details_style():
        """Detalhes do arquivo - texto pequeno e cinza"""
        return f"""
            QLabel {{
                font-size: 12px;          /* Fonte pequena */
                color: {HistoryStyleSheet.ICON_BG};  /* Cor cinza */
                margin: 0px;              /* Sem margens */
                padding: 5px;            /* Sem padding */
            }}
        """

    @staticmethod
    def delete_button_style():
        """Botão de deletar - transparente com hover vermelho"""
        return f"""
            QPushButton {{
                background: transparent;   /* Fundo transparente */
                border: none;             /* Sem borda */
                border-radius: 12px;      /* Bordas arredondadas */
            }}
            QPushButton:hover {{
                background-color: {HistoryStyleSheet.DELETE_HOVER};  /* Fundo vermelho ao passar mouse */
            }}
        """

    @staticmethod
    def grid_container_style():
        """Container em grid - fundo transparente"""
        return """
            QWidget {
                background: transparent;   /* Fundo transparente para não interferir */
            }
        """