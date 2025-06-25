from pytubefix import YouTube
import os
import re
import subprocess
from PIL import Image
import requests


def listar_resolucoes_disponiveis(url):
    yt = YouTube(url)
    resolucoes = set()
    # Streams de vídeo (sem áudio)
    for stream in yt.streams.filter(only_video=True, file_extension='mp4'):
        if stream.resolution:
            resolucoes.add(stream.resolution)
    # Streams progressivos (com áudio)
    for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
        if stream.resolution:
            resolucoes.add(stream.resolution)
    return sorted(resolucoes, key=lambda x: int(x.replace('p','')))

def baixar_video_audio_mesclar(url, resolucao, pasta_destino="videos", formato='mp4'):
    try:
        yt = YouTube(url)
        # Tenta pegar stream progressivo (vídeo+áudio)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolucao).first()
        if stream:
            os.makedirs(pasta_destino, exist_ok=True)
            titulo_limpo = re.sub(r'[\\/*?:"<>|]', '', yt.title)
            filename = titulo_limpo.replace(" ", "_") + f"_{resolucao}.{formato}"
            path = stream.download(output_path=pasta_destino, filename=filename)
            return path
        # Se não for progressivo, baixa separado e mescla
        video_stream = yt.streams.filter(only_video=True, file_extension='mp4', resolution=resolucao).first()
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
        if not video_stream or not audio_stream:
            print("❌ Não encontrou vídeo ou áudio para a resolução desejada.")
            return None
        os.makedirs(pasta_destino, exist_ok=True)
        titulo_limpo = re.sub(r'[\\/*?:"<>|]', '', yt.title)
        base_filename = titulo_limpo.replace(" ", "_") + f"_{resolucao}"
        video_path = os.path.join(pasta_destino, base_filename + "_video.mp4")
        audio_path = os.path.join(pasta_destino, base_filename + "_audio.mp4")
        output_path = os.path.join(pasta_destino, base_filename + ".mp4")
        video_stream.download(output_path=pasta_destino, filename=base_filename + "_video.mp4")
        audio_stream.download(output_path=pasta_destino, filename=base_filename + "_audio.mp4")
        caminho_ffmpeg = r"C:\Users\Vinicius Leite\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
        comando = [
            caminho_ffmpeg, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            output_path
        ]
        subprocess.run(comando, check=True)
        os.remove(video_path)
        os.remove(audio_path)
        return output_path
    except Exception as e:
        print(f"❌ Erro ao baixar/mesclar: {e}")
        return None
    
def baixar_audio(url, pasta_destino="audios", formato="mp3"):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if not audio_stream:
            print("❌ Não encontrou stream de áudio.")
            return None
        os.makedirs(pasta_destino, exist_ok=True)
        titulo_limpo = re.sub(r'[\\/*?:"<>|]', '', yt.title)
        base_filename = titulo_limpo.replace(" ", "_")
        temp_path = os.path.join(pasta_destino, base_filename + "_audio.mp4")
        final_path = os.path.join(pasta_destino, base_filename + f".{formato}")
        audio_stream.download(output_path=pasta_destino, filename=base_filename + "_audio.mp4")
        caminho_ffmpeg = r"C:\Users\Vinicius Leite\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
        comando = [
            caminho_ffmpeg, "-y",
            "-i", temp_path,
            final_path
        ]
        subprocess.run(comando, check=True)
        os.remove(temp_path)
        return final_path
    except Exception as e:
        print(f"❌ Erro ao baixar/convert audio: {e}")
        return None

def baixar_thumbnail(url, pasta_destino="thumbnails", formato="jpg"):
    try:
        yt = YouTube(url)
        thumb_url = yt.thumbnail_url
        os.makedirs(pasta_destino, exist_ok=True)
        titulo_limpo = re.sub(r'[\\/*?:"<>|]', '', yt.title)
        base_filename = titulo_limpo.replace(" ", "_")
        temp_path = os.path.join(pasta_destino, base_filename + "_thumb.jpg")
        final_path = os.path.join(pasta_destino, base_filename + f"_thumb.{formato.lower()}")
        # Baixa a thumbnail como jpg
        response = requests.get(thumb_url)
        if response.status_code == 200:
            with open(temp_path, "wb") as f:
                f.write(response.content)
            # Converte para o formato desejado usando PIL
            img = Image.open(temp_path)
            img.convert("RGB").save(final_path, formato.upper())
            os.remove(temp_path)
            return final_path
        else:
            print("❌ Não foi possível baixar a thumbnail.")
            return None
    except Exception as e:
        print(f"❌ Erro ao baixar/converter thumbnail: {e}")
        return None