"""
Sistema de música de fondo usando pygame.mixer.
Maneja la reproducción de tracks según la escena/arco actual.
Si pygame no está instalado o no hay archivos de música, funciona sin sonido.
"""

import os
import sys
from pathlib import Path

# Determinar la carpeta de música (funciona tanto en dev como en exe)
if getattr(sys, 'frozen', False):
    # PyInstaller --onefile extrae datos a _MEIPASS
    BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent))
else:
    BASE_DIR = Path(__file__).parent

CARPETA_MUSICA = BASE_DIR / "musica"

# Fallback: buscar junto al exe si no está en _MEIPASS
if not CARPETA_MUSICA.exists() and getattr(sys, 'frozen', False):
    CARPETA_MUSICA = Path(sys.executable).parent / "musica"

# Mapeo de escenas a tracks de música
TRACKS = {
    "menu": "menu.ogg",
    "aldea": "aldea.ogg",
    "exploracion": "exploracion.ogg",
    "combate": "combate.ogg",
    "boss": "boss.ogg",
    "victoria": "victoria.ogg",
}

# Mapeo de escenas del juego a tracks
ESCENA_A_TRACK = {
    "1_intro": "aldea",
    "1_aldea": "aldea",
    "1_mision": "aldea",
    "1_bosque": "exploracion",
    "1_combate_cultistas": "combate",
    "1_ruinas_puertas": "exploracion",
    "2_intro": "exploracion",
    "2_trampa": "exploracion",
    "2_camara_eco": "combate",
    "2_artefacto": "victoria",
    "3_intro": "exploracion",
    "3_torre_entrada": "exploracion",
    "3_combate_golem": "boss",
    "3_escalada": "exploracion",
    "3_camara_final": "boss",
    "3_combate_malachar": "boss",
    "3_epilogo": "victoria",
    "game_over": "menu",
}

_mixer_disponible = False
_track_actual = None
_volumen = 0.4


def inicializar():
    """Intenta inicializar pygame.mixer. Si falla, funciona sin sonido."""
    global _mixer_disponible
    try:
        import pygame
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        _mixer_disponible = True
    except Exception:
        _mixer_disponible = False


def reproducir(nombre_track: str, loop: bool = True):
    """Reproduce un track por nombre. Si ya está sonando el mismo, no reinicia."""
    global _track_actual
    if not _mixer_disponible:
        return

    if nombre_track == _track_actual:
        return  # Ya está sonando

    archivo = CARPETA_MUSICA / TRACKS.get(nombre_track, "")
    if not archivo.exists():
        return

    try:
        import pygame
        pygame.mixer.music.load(str(archivo))
        pygame.mixer.music.set_volume(_volumen)
        pygame.mixer.music.play(-1 if loop else 0)
        _track_actual = nombre_track
    except Exception:
        pass


def reproducir_para_escena(id_escena: str):
    """Reproduce el track correspondiente a una escena del juego."""
    track = ESCENA_A_TRACK.get(id_escena)
    if track:
        reproducir(track)


def detener():
    """Detiene la música."""
    global _track_actual
    if not _mixer_disponible:
        return
    try:
        import pygame
        pygame.mixer.music.fadeout(1000)
        _track_actual = None
    except Exception:
        pass


def pausar():
    if not _mixer_disponible:
        return
    try:
        import pygame
        pygame.mixer.music.pause()
    except Exception:
        pass


def reanudar():
    if not _mixer_disponible:
        return
    try:
        import pygame
        pygame.mixer.music.unpause()
    except Exception:
        pass


def set_volumen(vol: float):
    """Ajusta el volumen (0.0 a 1.0)."""
    global _volumen
    _volumen = max(0.0, min(1.0, vol))
    if not _mixer_disponible:
        return
    try:
        import pygame
        pygame.mixer.music.set_volume(_volumen)
    except Exception:
        pass


def volumen_actual() -> float:
    return _volumen


def hay_musica() -> bool:
    """Retorna True si hay al menos un archivo de música disponible."""
    if not CARPETA_MUSICA.exists():
        return False
    return any(CARPETA_MUSICA.glob("*.ogg")) or any(CARPETA_MUSICA.glob("*.ogg"))
