"""Renderdoelrenderers voor het EmberForge-terminalthema (dircolors, PS1)."""
from __future__ import annotations

from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.theme_resolution import resolveer_thema

WERELD_ID = "beckeringh-palace"

ARCHIEF_EXTENSIES = (
    ".tar", ".tgz", ".arc", ".arj", ".taz", ".lha", ".lz4", ".lzh", ".lzma",
    ".tlz", ".txz", ".tzo", ".t7z", ".zip", ".z", ".dz", ".gz", ".lrz",
    ".lz", ".lzo", ".xz", ".zst", ".tzst", ".bz2", ".bz", ".tbz", ".tbz2",
    ".tz", ".deb", ".rpm", ".jar", ".war", ".ear", ".sar", ".rar", ".alz",
    ".ace", ".zoo", ".cpio", ".7z", ".rz", ".cab", ".wim", ".swm", ".dwm",
    ".esd",
)
BEELD_EXTENSIES = (
    ".jpg", ".jpeg", ".mjpg", ".mjpeg", ".gif", ".bmp", ".pbm", ".pgm",
    ".ppm", ".tga", ".xbm", ".xpm", ".tif", ".tiff", ".png", ".svg",
    ".svgz", ".mng", ".pcx", ".mov", ".mpg", ".mpeg", ".m2v", ".mkv",
    ".webm", ".webp", ".ogm", ".mp4", ".m4v", ".mp4v", ".vob", ".qt",
    ".nuv", ".wmv", ".asf", ".rm", ".rmvb", ".flc", ".avi", ".fli",
    ".flv", ".gl", ".dl", ".xcf", ".xwd", ".yuv", ".cgm", ".emf", ".ogv",
    ".ogx",
)
AUDIO_EXTENSIES = (
    ".aac", ".au", ".flac", ".m4a", ".mid", ".midi", ".mka", ".mp3",
    ".mpc", ".ogg", ".ra", ".wav", ".oga", ".opus", ".spx", ".xspf",
)


def _rgb(hex_waarde: str) -> str:
    return ";".join(
        str(int(hex_waarde[index:index + 2], 16))
        for index in (1, 3, 5)
    )


def _materiaal(objecten: Iterable[Architectuurobject], rol: str) -> str:
    thema = resolveer_thema(objecten, WERELD_ID)
    if thema.materiaal is None:
        raise ValueError("EmberForge-terminalthema vereist een opgelost materiaal")
    kleur = thema.materiaal.kleur(rol)
    if kleur is None:
        raise ValueError(f"EmberForge-terminalthema vereist materiaalrol '{rol}'")
    return _rgb(kleur.waarde)


def naar_dircolors(objecten: Iterable[Architectuurobject]) -> str:
    """Render het opgeloste materiaalthema deterministisch naar GNU dircolors."""

    objecten = tuple(objecten)
    interactie = _materiaal(objecten, "interaction")
    interactie_hover = _materiaal(objecten, "interaction-hover")
    accent = _materiaal(objecten, "accent")
    accent_hover = _materiaal(objecten, "accent-hover")
    muted = _materiaal(objecten, "muted")
    fout = _materiaal(objecten, "error")
    succes = _materiaal(objecten, "success")

    regels = [
        "# Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen.",
        "# Bron: compiler/terminal_theme_renderer.py (opgelost EmberForge-materiaalthema)",
        "",
        "TERM *",
        "",
        "NORMAL 0",
        "FILE 0",
        "RESET 0",
        f"DIR 38;2;{interactie};01",
        f"LINK 38;2;{interactie_hover};01",
        "MULTIHARDLINK 0",
        f"FIFO 38;2;{accent_hover}",
        f"SOCK 38;2;{accent};01",
        f"DOOR 38;2;{accent};01",
        f"BLK 38;2;{accent_hover};01",
        f"CHR 38;2;{accent_hover};01",
        f"ORPHAN 38;2;{fout};01",
        "MISSING 0",
        "SETUID 37;41",
        "SETGID 30;43",
        "CAPABILITY 30;41",
        "STICKY_OTHER_WRITABLE 30;42",
        "OTHER_WRITABLE 34;42",
        "STICKY 37;44",
        f"EXEC 38;2;{succes};01",
        "",
        "# Archieven",
    ]
    regels.extend(f"{ext} 38;2;{accent};01" for ext in ARCHIEF_EXTENSIES)
    regels.append("")
    regels.append("# Beeld/video")
    regels.extend(f"{ext} 38;2;{accent_hover}" for ext in BEELD_EXTENSIES)
    regels.append("")
    regels.append("# Audio")
    regels.extend(f"{ext} 38;2;{muted}" for ext in AUDIO_EXTENSIES)
    regels.append("")
    return "\n".join(regels)


def naar_ps1(objecten: Iterable[Architectuurobject]) -> str:
    """Render het opgeloste materiaalthema deterministisch naar een bash PS1-snippet."""

    objecten = tuple(objecten)
    accent = _materiaal(objecten, "accent")
    muted = _materiaal(objecten, "muted")
    interactie = _materiaal(objecten, "interaction")
    succes = _materiaal(objecten, "success")

    regels = [
        "# Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen.",
        "# Bron: compiler/terminal_theme_renderer.py (opgelost EmberForge-materiaalthema)",
        "# Source dit bestand na __venv_ps1 in ~/.bashrc.",
        (
            'PS1="\\[\\e]0;\\${debian_chroot:+(\\$debian_chroot)}'
            '\\u@\\h: \\w\\a\\]"'
            "'${debian_chroot:+($debian_chroot)}$(__venv_ps1)'"
        ),
        f"PS1+='\\[\\033[38;2;{accent};1m\\]\\u@\\h\\[\\033[0m\\]'",
        f"PS1+='\\[\\033[38;2;{muted}m\\]:\\[\\033[0m\\]'",
        f"PS1+='\\[\\033[38;2;{interactie};1m\\]\\w\\[\\033[0m\\]'",
        f"PS1+='\\[\\033[38;2;{succes}m\\]\\$\\[\\033[0m\\] '",
        "export PS1",
        "",
    ]
    return "\n".join(regels)
