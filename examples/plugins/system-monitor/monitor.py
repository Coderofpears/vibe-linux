#!/usr/bin/env python3
"""System monitor plugin - display real-time resource usage."""

import json
import re
from pathlib import Path


def read_cpu_usage() -> float:
    """Read CPU usage percentage."""
    try:
        with open("/proc/stat") as f:
            lines = f.readlines()
        
        # Simple CPU usage calculation
        cpu_line = lines[0].split()
        user = int(cpu_line[1])
        nice = int(cpu_line[2])
        system = int(cpu_line[3])
        idle = int(cpu_line[4])
        
        total = user + nice + system + idle
        used = user + nice + system
        
        return round((used / total) * 100, 1) if total > 0 else 0.0
    except (OSError, IndexError, ValueError):
        return 0.0


def read_memory_usage() -> dict:
    """Read memory usage."""
    try:
        with open("/proc/meminfo") as f:
            meminfo = {}
            for line in f:
                key, value = line.split(":", 1)
                meminfo[key.strip()] = int(value.split()[0])
        
        total = meminfo.get("MemTotal", 0)
        available = meminfo.get("MemAvailable", 0)
        used = total - available
        percent = round((used / total) * 100, 1) if total > 0 else 0.0
        
        return {
            "total_mb": round(total / 1024, 1),
            "used_mb": round(used / 1024, 1),
            "available_mb": round(available / 1024, 1),
            "percent": percent
        }
    except (OSError, KeyError, ValueError):
        return {"total_mb": 0, "used_mb": 0, "available_mb": 0, "percent": 0}


def read_disk_usage(path: str = "/") -> dict:
    """Read disk usage for a given path."""
    try:
        import os
        stat = os.statvfs(path)
        total = stat.f_blocks * stat.f_frsize
        available = stat.f_bavail * stat.f_frsize
        used = (stat.f_blocks - stat.f_bfree) * stat.f_frsize
        percent = round((used / total) * 100, 1) if total > 0 else 0.0
        
        return {
            "path": path,
            "total_gb": round(total / (1024**3), 1),
            "used_gb": round(used / (1024**3), 1),
            "available_gb": round(available / (1024**3), 1),
            "percent": percent
        }
    except (OSError, ZeroDivisionError):
        return {"path": path, "total_gb": 0, "used_gb": 0, "available_gb": 0, "percent": 0}


def read_cpu_temp() -> float:
    """Read CPU temperature if available."""
    try:
        # Try multiple common temperature paths
        temp_paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/devices/platform/coretemp.0/hwmon/hwmon0/temp1_input",
        ]
        
        for path in temp_paths:
            try:
                with open(path) as f:
                    temp = int(f.read().strip())
                    # Most thermal zones report in millidegrees Celsius
                    return round(temp / 1000, 1)
            except (OSError, ValueError):
                continue
        
        return 0.0
    except Exception:
        return 0.0


def main() -> None:
    """Display system monitoring information."""
    cpu = read_cpu_usage()
    memory = read_memory_usage()
    disk = read_disk_usage("/")
    temp = read_cpu_temp()
    
    # Format output
    print("\n╔══════════════════════════════════════════╗")
    print("║       VIBE SYSTEM MONITOR v1.0           ║")
    print("╚══════════════════════════════════════════╝")
    print()
    
    print(f"📊 CPU Usage:        {cpu}%")
    print(f"💾 Memory:           {memory['percent']}% ({memory['used_mb']} MB / {memory['total_mb']} MB)")
    print(f"💿 Disk (/):         {disk['percent']}% ({disk['used_gb']} GB / {disk['total_gb']} GB)")
    
    if temp > 0:
        print(f"🌡️  CPU Temperature: {temp}°C")
    
    print()
    
    # JSON output for integration
    output = {
        "cpu_percent": cpu,
        "memory": memory,
        "disk": disk,
        "cpu_temp_celsius": temp
    }
    
    print("Raw JSON output:")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
