import subprocess
import os
import json


def listar_resolucoes_twitch(url):
    """
    Lista todas as resoluções disponíveis para um stream/vídeo do Twitch
    """
    try:
        cmd = [
            "yt-dlp",
            "--list-formats",
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Extrair resoluções das linhas de formato
        resolutions = []
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'x' in line and ('mp4' in line or 'webm' in line):
                # Procurar por padrões como "1920x1080", "1280x720", etc.
                import re
                resolution_match = re.search(r'(\d+)x(\d+)', line)
                if resolution_match:
                    height = resolution_match.group(2)
                    resolution_str = f"{height}p"
                    if resolution_str not in resolutions:
                        resolutions.append(resolution_str)
        
        # Ordenar do maior para o menor
        resolution_order = ['1080p', '720p', '480p', '360p', '160p']
        sorted_resolutions = [r for r in resolution_order if r in resolutions]
        
        return sorted_resolutions if sorted_resolutions else ['720p', '480p', '360p']
        
    except Exception as e:
        print(f"Erro ao listar resoluções: {e}")
        return ['1080p', '720p', '480p', '360p', '160p']


def baixar_video_twitch(url, resolucao, pasta_destino, formato='mp4'):
    """
    Baixa vídeo do Twitch usando yt-dlp com resolução específica
    """
    try:
        if not url:
            print("Error: No URL provided!")
            return None
            
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino, exist_ok=True)
        
        # Extrair apenas o número da resolução (ex: "1080p" -> "1080")
        height = resolucao.replace('p', '')
        
        # Construir seletor de formato mais específico para Twitch
        # Tenta primeiro a resolução exata, depois fallback para resoluções menores
        format_selectors = [
            f"best[height={height}]",                    # Resolução exata
            f"best[height<={height}]",                   # Até a resolução especificada
            f"best[height>={height}]/best[height<={height}]", # Preferir maior, mas aceitar menor
            "best"                                       # Fallback para melhor disponível
        ]
        
        for format_selector in format_selectors:
            try:
                cmd = [
                    "yt-dlp",
                    "-f", format_selector,
                    "-o", f"{pasta_destino}/%(title)s.%(ext)s" if pasta_destino else "%(title)s.%(ext)s",
                    "--concurrent-fragments", "8",
                    "--merge-output-format", formato,
                    url
                ]
                
                print(f"Tentando baixar com formato: {format_selector}")
                subprocess.run(cmd, check=True)
                print("✅ Download complete!")
                
                # Procura o arquivo baixado
                if pasta_destino:
                    files = os.listdir(pasta_destino)
                    video_files = [f for f in files if f.endswith(('.mp4', '.mkv', '.webm', '.avi'))]
                    if video_files:
                        return os.path.join(pasta_destino, video_files[-1])
                
                return None
                
            except subprocess.CalledProcessError:
                print(f"Formato {format_selector} falhou, tentando próximo...")
                continue
        
        print("❌ Todos os formatos falharam")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def obter_info_twitch(url):
    """
    Obtém informações do vídeo/stream do Twitch usando yt-dlp
    """
    try:
        if not url:
            return None
            
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-download",
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        
        return {
            'title': info.get('title', 'Título não disponível'),
            'uploader': info.get('uploader', 'Canal não disponível'),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail', ''),
            'description': info.get('description', ''),
            'view_count': info.get('view_count', 0),
            'upload_date': info.get('upload_date', ''),
        }
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao obter informações: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


def baixar_audio_twitch(url, pasta_destino, formato="mp3"):
    """
    Baixa apenas o áudio do Twitch
    """
    try:
        if not url:
            print("Error: No URL provided!")
            return None
            
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino, exist_ok=True)
        
        cmd = [
            "yt-dlp",
            "-o", f"{pasta_destino}/%(title)s.%(ext)s" if pasta_destino else "%(title)s.%(ext)s",
            "--extract-audio",
            "--audio-format", formato,
            "--concurrent-fragments", "8",
            url
        ]
        
        print("Downloading audio... (This may take a while)")
        subprocess.run(cmd, check=True)
        print("✅ Audio download complete!")
        
        if pasta_destino:
            files = os.listdir(pasta_destino)
            audio_files = [f for f in files if f.endswith(('.mp3', '.wav', '.aac', '.flac'))]
            if audio_files:
                return os.path.join(pasta_destino, audio_files[-1])
        
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Audio download failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def baixar_thumbnail_twitch(url, pasta_destino, formato="jpg"):
    """
    Baixa thumbnail do Twitch
    """
    try:
        if not url:
            print("Error: No URL provided!")
            return None
            
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino, exist_ok=True)
        
        cmd = [
            "yt-dlp",
            "--write-thumbnail",
            "--skip-download",
            "-o", f"{pasta_destino}/%(title)s.%(ext)s" if pasta_destino else "%(title)s.%(ext)s",
            url
        ]
        
        print("Downloading thumbnail...")
        subprocess.run(cmd, check=True)
        print("✅ Thumbnail download complete!")
        
        if pasta_destino:
            files = os.listdir(pasta_destino)
            image_files = [f for f in files if f.endswith(('.jpg', '.png', '.webp'))]
            if image_files:
                return os.path.join(pasta_destino, image_files[-1])
        
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Thumbnail download failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None