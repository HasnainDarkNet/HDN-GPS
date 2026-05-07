#!/usr/bin/env python3

# =====================================================
#        ██╗  ██╗██████╗ ███╗   ██╗
#        ██║  ██║██╔══██╗████╗  ██║
#        ███████║██║  ██║██╔██╗ ██║
#        ██╔══██║██║  ██║██║╚██╗██║
#        ██║  ██║██████╔╝██║ ╚████║
#        ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝
#
#      H A S N A I N   D A R K   N E T
# ---------------------------------------------
#        PROFESSIONAL METADATA TOOL
# =====================================================

import os
import time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# =====================================================
# COLORS
# =====================================================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# =====================================================
# BANNER
# =====================================================

def banner():
    os.system("cls" if os.name == "nt" else "clear")

    print(f"""{RED}
██╗  ██╗ █████╗ ███████╗███╗   ██╗ █████╗ ██╗███╗   ██╗
██║  ██║██╔══██╗██╔════╝████╗  ██║██╔══██╗██║████╗  ██║
███████║███████║███████╗██╔██╗ ██║███████║██║██╔██╗ ██║
██╔══██║██╔══██║╚════██║██║╚██╗██║██╔══██║██║██║╚██╗██║
██║  ██║██║  ██║███████║██║ ╚████║██║  ██║██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
{RESET}
""")

    print(f"{CYAN}{'='*65}")
    print(f"        🔒 HASNAIN DARK NET TOOL")
    print(f"        📡 PROFESSIONAL METADATA ANALYZER")
    print(f"{'='*65}{RESET}\n")

# =====================================================
# FIX PATH (ALL OS SUPPORT)
# =====================================================

def fix_path(path):
    path = path.strip().replace('"', '').replace("'", "")

    # Windows → Linux/WSL
    if ":" in path and "\\" in path:
        drive = path[0].lower()
        path = path.replace(f"{path[0]}:\\", f"/mnt/{drive}/")
        path = path.replace("\\", "/")

    return path

# =====================================================
# GPS CONVERTER
# =====================================================

def convert_to_degrees(value):
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except:
        return None

# =====================================================
# SAFE GPS PARSER
# =====================================================

def extract_gps_info(gps_info):

    if not isinstance(gps_info, dict):
        return None, None

    gps_data = {}

    for key in gps_info:
        decode = GPSTAGS.get(key, key)
        gps_data[decode] = gps_info[key]

    try:
        lat = convert_to_degrees(gps_data.get("GPSLatitude"))
        lat_ref = gps_data.get("GPSLatitudeRef")

        lon = convert_to_degrees(gps_data.get("GPSLongitude"))
        lon_ref = gps_data.get("GPSLongitudeRef")

        if lat is None or lon is None:
            return None, None

        if lat_ref != "N":
            lat = -lat

        if lon_ref != "E":
            lon = -lon

        return lat, lon

    except:
        return None, None

# =====================================================
# METADATA EXTRACTOR
# =====================================================

def extract_metadata(image_path):

    image_path = fix_path(image_path)

    if not os.path.exists(image_path):
        print(f"{RED}[!] File Not Found!{RESET}")
        return

    try:
        image = Image.open(image_path)

        print(f"{GREEN}[+] Loading Image Metadata...{RESET}")
        time.sleep(0.5)

        # ---------------- BASIC INFO ----------------
        print(f"""
{CYAN}
╔════════════════════════════════════╗
║        📌 BASIC INFORMATION        ║
╚════════════════════════════════════╝
{RESET}
""")

        print(f"{YELLOW}File Name     : {WHITE}{os.path.basename(image_path)}")
        print(f"{YELLOW}Format        : {WHITE}{image.format}")
        print(f"{YELLOW}Mode          : {WHITE}{image.mode}")
        print(f"{YELLOW}Resolution    : {WHITE}{image.size}")
        print(f"{YELLOW}File Size     : {WHITE}{os.path.getsize(image_path)/1024:.2f} KB")

        exif = image._getexif()

        if not exif:
            print(f"{RED}[!] No EXIF Data Found!{RESET}")
            return

        # ---------------- EXIF INFO ----------------
        print(f"""
{CYAN}
╔════════════════════════════════════╗
║          📷 EXIF METADATA          ║
╚════════════════════════════════════╝
{RESET}
""")

        gps_info = None

        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag == "GPSInfo":
                gps_info = value
                continue

            print(f"{GREEN}{tag:<20}:{WHITE} {value}")

        # ---------------- GPS INFO ----------------
        print(f"""
{CYAN}
╔════════════════════════════════════╗
║        🌍 GPS INFORMATION          ║
╚════════════════════════════════════╝
{RESET}
""")

        lat, lon = extract_gps_info(gps_info)

        if lat and lon:
            print(f"{GREEN}Latitude      : {WHITE}{lat}")
            print(f"{GREEN}Longitude     : {WHITE}{lon}")
            print(f"{GREEN}Google Maps   : {WHITE}https://www.google.com/maps?q={lat},{lon}")
        else:
            print(f"{RED}[!] No Valid GPS Data Found{RESET}")

    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    banner()

    image_path = input(f"""
{CYAN}┌────────────────────────────────────────────┐
│  📁 Enter Image Path                       │
└────────────────────────────────────────────┘
{WHITE}➤ """)

    extract_metadata(image_path)

    print(f"\n{GREEN}[✓] Scan Completed Successfully!{RESET}\n")
