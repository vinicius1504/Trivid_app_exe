import subprocess
import os


def baixar_video_twitch(url, resolucao, pasta_destino, formato='mp4'):
    """
    Baixa vídeo do Twitch usando yt-dlp
    """
    try:
        os.makedirs(pasta_destino, exist_ok=True)
        
        # Mapear resolução para formato do yt-dlp
        format_selector = "best"
        if resolucao != "best":
            format_selector = f"best[height<={resolucao.replace('p', '')}]"
        
        cmd = [
            "yt-dlp",
            "-o", f"{pasta_destino}/%(title)s.%(ext)s",
            "--format", format_selector,
            "--concurrent-fragments", "8",
            url
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Procura o arquivo baixado
        files = os.listdir(pasta_destino)
        video_files = [f for f in files if f.endswith(('.mp4', '.mkv', '.webm', '.avi'))]
        
        if video_files:
            return os.path.join(pasta_destino, video_files[-1])
        return None
        
    except Exception as e:
        print(f"Erro ao baixar vídeo do Twitch: {e}")
        return None


def baixar_audio_twitch(url, pasta_destino, formato="mp3"):
    """
    Baixa apenas o áudio do Twitch
    """
    try:
        os.makedirs(pasta_destino, exist_ok=True)
        
        cmd = [
            "yt-dlp",
            "-o", f"{pasta_destino}/%(title)s.%(ext)s",
            "--extract-audio",
            "--audio-format", formato,
            "--concurrent-fragments", "8",
            url
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        files = os.listdir(pasta_destino)
        audio_files = [f for f in files if f.endswith(('.mp3', '.wav', '.aac', '.flac'))]
        
        if audio_files:
            return os.path.join(pasta_destino, audio_files[-1])
        return None
        
    except Exception as e:
        print(f"Erro ao baixar áudio do Twitch: {e}")
        return None


def baixar_thumbnail_twitch(url, pasta_destino, formato="jpg"):
    """
    Baixa thumbnail do Twitch
    """
    try:
        os.makedirs(pasta_destino, exist_ok=True)
        
        cmd = [
            "yt-dlp",
            "--write-thumbnail",
            "--skip-download",
            "-o", f"{pasta_destino}/%(title)s.%(ext)s",
            url
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        files = os.listdir(pasta_destino)
        image_files = [f for f in files if f.endswith(('.jpg', '.png', '.webp'))]
        
        if image_files:
            return os.path.join(pasta_destino, image_files[-1])
        return None
        
    except Exception as e:
        print(f"Erro ao baixar thumbnail do Twitch: {e}")
        return None