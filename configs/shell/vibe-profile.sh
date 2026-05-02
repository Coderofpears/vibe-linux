export VIBE_LINUX=1
export EDITOR="${EDITOR:-nano}"

# Plugin shortcuts
alias vibe-update='vibectl update'
alias vibe-diagnostics='vibectl diagnostics'
alias vibe-monitor='vibectl plugins run vibe.system-monitor'
alias vibe-settings='vibectl plugins run vibe.quick-settings'
alias vibe-clean='vibectl plugins run vibe.system-cleaner'

# System shortcuts
alias vibe='vibectl'
alias ll='ls -lah'
alias diskspace='df -h'
alias memuse='free -h'

# Package management
alias pacman-update='sudo pacman -Syu'
alias pacman-search='pacman -Ss'

# Git shortcuts (if available)
if command -v git &> /dev/null; then
    alias ga='git add'
    alias gc='git commit'
    alias gs='git status'
fi

# Helpful functions
vibe-theme() {
    case "$1" in
        windows11)
            cp -r /opt/vibe-linux/configs/windows11/* ~/.config/ && echo "Windows 11 theme applied"
            ;;
        macos)
            cp -r /opt/vibe-linux/configs/macos/* ~/.config/ && echo "macOS theme applied"
            ;;
        *)
            echo "Usage: vibe-theme [windows11|macos]"
            ;;
    esac
}

# Welcome banner
if [ -n "$VIBE_LINUX" ] && [ -z "$VIBE_WELCOME_SHOWN" ]; then
    export VIBE_WELCOME_SHOWN=1
    echo "🚀 Welcome to Vibe-Linux!"
    echo "   Type 'vibectl --help' for commands"
fi


