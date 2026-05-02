#!/usr/bin/env python3
"""System Cleaner plugin - clean and optimize system."""

import os
import shutil
from pathlib import Path


def get_directory_size(path: Path) -> int:
    """Calculate total size of directory in bytes."""
    total = 0
    try:
        for entry in path.rglob("*"):
            if entry.is_file():
                try:
                    total += entry.stat().st_size
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return total


def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def scan_package_cache() -> dict:
    """Analyze package manager cache."""
    cache_path = Path("/var/cache/pacman/pkg")
    size = 0
    count = 0
    
    if cache_path.exists():
        try:
            for pkg in cache_path.glob("*.pkg.tar.*"):
                count += 1
                size += pkg.stat().st_size
        except (OSError, PermissionError):
            pass
    
    return {
        "path": str(cache_path),
        "size_bytes": size,
        "size_human": format_size(size),
        "package_count": count
    }


def scan_user_cache() -> dict:
    """Analyze user cache directories."""
    home = Path.home()
    cache_path = home / ".cache"
    
    size = get_directory_size(cache_path) if cache_path.exists() else 0
    
    return {
        "path": str(cache_path),
        "size_bytes": size,
        "size_human": format_size(size)
    }


def scan_temp_files() -> dict:
    """Analyze temporary files."""
    temp_path = Path("/tmp")
    user_home = Path.home()
    size = 0
    count = 0
    
    if temp_path.exists():
        try:
            for item in temp_path.iterdir():
                try:
                    if item.is_file():
                        count += 1
                        size += item.stat().st_size
                except (OSError, PermissionError):
                    pass
        except (OSError, PermissionError):
            pass
    
    return {
        "path": str(temp_path),
        "size_bytes": size,
        "size_human": format_size(size),
        "file_count": count
    }


def main() -> None:
    """Analyze system and provide optimization recommendations."""
    print("\n╔══════════════════════════════════════════╗")
    print("║     VIBE SYSTEM CLEANER v1.0             ║")
    print("╚══════════════════════════════════════════╝")
    print()
    
    print("🔍 Analyzing system storage...")
    print()
    
    # Scan caches
    package_cache = scan_package_cache()
    user_cache = scan_user_cache()
    temp_files = scan_temp_files()
    
    total_reclaimable = (
        package_cache["size_bytes"] +
        user_cache["size_bytes"] +
        temp_files["size_bytes"]
    )
    
    # Display results
    print("📦 Package Cache:")
    print(f"   Location: {package_cache['path']}")
    print(f"   Size: {package_cache['size_human']} ({package_cache['package_count']} packages)")
    print()
    
    print("💾 User Cache:")
    print(f"   Location: {user_cache['path']}")
    print(f"   Size: {user_cache['size_human']}")
    print()
    
    print("📂 Temporary Files:")
    print(f"   Location: {temp_files['path']}")
    print(f"   Size: {temp_files['size_human']} ({temp_files['file_count']} files)")
    print()
    
    print("=" * 42)
    print(f"Total Reclaimable Space: {format_size(total_reclaimable)}")
    print("=" * 42)
    print()
    
    print("💡 Optimization Tips:")
    print("  • Run 'pacman -Scc' to clean package cache (requires sudo)")
    print("  • Run 'journalctl --vacuum=30d' to trim system logs")
    print("  • Use 'bleachbit' for advanced cleanup")
    print("  • Enable 'timeshift' for automated snapshots")
    print()
    
    print("ℹ️  To actually clean files, please run the commands above.")
    print("   This plugin is read-only for safety.")
    print()


if __name__ == "__main__":
    main()
