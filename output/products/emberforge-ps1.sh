# Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen.
# Bron: compiler/terminal_theme_renderer.py (opgelost EmberForge-materiaalthema)
# Source dit bestand na __venv_ps1 in ~/.bashrc.
PS1="\[\e]0;\${debian_chroot:+(\$debian_chroot)}\u@\h: \w\a\]"'${debian_chroot:+($debian_chroot)}$(__venv_ps1)'
PS1+='\[\033[38;2;201;137;91;1m\]\u@\h\[\033[0m\]'
PS1+='\[\033[38;2;184;197;214m\]:\[\033[0m\]'
PS1+='\[\033[38;2;125;211;252;1m\]\w\[\033[0m\]'
PS1+='\[\033[38;2;74;222;128m\]\$\[\033[0m\] '
export PS1
