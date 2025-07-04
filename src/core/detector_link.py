import re


def detect_platform(url):
    """
    Detecta a plataforma baseada na URL
    Retorna: 'youtube', 'twitch', 'spotify', ou 'unknown'
    """
    url = url.lower().strip()
    
    # YouTube patterns
    youtube_patterns = [
        r'(?:youtube\.com|youtu\.be)',
        r'youtube\.com/watch\?v=',
        r'youtu\.be/',
        r'youtube\.com/embed/',
        r'youtube\.com/v/'
    ]
    
    # Twitch patterns
    twitch_patterns = [
        r'twitch\.tv/videos/',
        r'twitch\.tv/\w+/clip/',
        r'clips\.twitch\.tv/',
        r'twitch\.tv/\w+$'
    ]
    
    # Spotify patterns
    spotify_patterns = [
        r'open\.spotify\.com/track/',
        r'open\.spotify\.com/album/',
        r'open\.spotify\.com/playlist/',
        r'spotify\.com/track/',
        r'spotify\.com/album/',
        r'spotify\.com/playlist/'
    ]
    
    # Check YouTube
    for pattern in youtube_patterns:
        if re.search(pattern, url):
            return 'youtube'
    
    # Check Twitch
    for pattern in twitch_patterns:
        if re.search(pattern, url):
            return 'twitch'
    
    # Check Spotify
    for pattern in spotify_patterns:
        if re.search(pattern, url):
            return 'spotify'
    
    return 'unknown'


def get_platform_info(platform):
    """
    Retorna informações específicas da plataforma
    """
    platforms = {
        'youtube': {
            'name': 'YouTube',
            'icon': '🎥',
            'color': '#FF0000',
            'button_color': "#850000"
        },
        'twitch': {
            'name': 'Twitch',
            'icon': '📺',
            'color': '#9146FF',
            'button_color': '#9146FF'
        },
        'spotify': {
            'name': 'Spotify',
            'icon': '🎵',
            'color': '#1DB954',
            'button_color': '#1DB954'
        }
    }
    
    return platforms.get(platform, {
        'name': 'Unknown',
        'icon': '❓',
        'color': '#666666',
        'button_color': '#008080'
    })


def is_valid_url(url):
    """
    Verifica se a URL é válida
    """
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None