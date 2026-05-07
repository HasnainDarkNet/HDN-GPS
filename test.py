#!/usr/bin/env python3

# ==========================================================
# ██╗  ██╗ █████╗ ███████╗███╗   ██╗ █████╗ ██╗███╗   ██╗
# ██║  ██║██╔══██╗██╔════╝████╗  ██║██╔══██╗██║████╗  ██║
# ███████║███████║███████╗██╔██╗ ██║███████║██║██╔██╗ ██║
# ██╔══██║██╔══██║╚════██║██║╚██╗██║██╔══██║██║██║╚██╗██║
# ██║  ██║██║  ██║███████║██║ ╚████║██║  ██║██║██║ ╚████║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#
#              HASNAIN DARK NET
#         PROFESSIONAL METADATA TOOL
# ==========================================================

import os
import sys
import time

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    print("\n[!] Pillow Library Not Installed!")
    print("[+] Install Using: pip install pillow\n")
    sys.exit()

# ==========================================================
# COLORS
# ==========================================================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Windows Color Fix
if os.name == "nt":
    os.system("")

# ==========================================================
# CLEAR SCREEN
# ==========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ==========================================================
# BANNER
# ==========================================================

def banner():
    clear()

    print(f"""{RED}

██╗  ██╗ █████╗ ███████╗███╗   ██╗ █████╗ ██╗███╗   ██╗
██║  ██║██╔══██╗██╔════╝████╗  ██║██╔══██╗██║████╗  ██║
███████║███████║███████╗██╔██╗ ██║███████║██║██╔██╗ ██║
██╔══██║██╔══██║╚════██║██║╚██╗██║██╔══██║██║██║╚██╗██║
██║  ██║██║  ██║███████║██║ ╚████║██║  ██║██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

{CYAN}==========================================================
              HASNAIN DARK NET
         PROFESSIONAL METADATA TOOL
=========================================================={RESET}
""")

# ==========================================================
# GPS CONVERTER
# ==========================================================

def convert_to_degrees(value):

    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])

        return d + (m / 60.0) + (s / 3600.0)

    except:
        return None

# ==========================================================
# GPS EXTRACTION
# ==========================================================

def extract_gps(gps_info):

    gps_data = {}

    for key in gps_info.keys():
        decoded = GPSTAGS.get(key, key)
        gps_data[decoded] = gps_info[key]

    try:
        lat = convert_to_degrees(gps_data["GPSLatitude"])
        lat_ref = gps_data["GPSLatitudeRef"]

        lon = convert_to_degrees(gps_data["GPSLongitude"])
        lon_ref = gps_data["GPSLongitudeRef"]

        if lat_ref != "N":
            lat = -lat

        if lon_ref != "E":
            lon = -lon

        return lat, lon

    except:
        return None, None

# ==========================================================
# METADATA EXTRACTOR
# ==========================================================

def extract_metadata(image_path):

    if not os.path.isfile(image_path):
        print(f"{RED}[!] Invalid File Path!{RESET}")
        return

    try:

        image = Image.open(image_path)

        print(f"\n{GREEN}[+] Scanning Image Metadata...{RESET}")
        time.sleep(1)

        print(f"""
{CYAN}==========================================================
                    BASIC INFORMATION
=========================================================={RESET}
""")

        print(f"{YELLOW}File Name      : {WHITE}{os.path.basename(image_path)}")
        print(f"{YELLOW}File Path      : {WHITE}{os.path.abspath(image_path)}")
        print(f"{YELLOW}Format         : {WHITE}{image.format}")
        print(f"{YELLOW}Mode           : {WHITE}{image.mode}")
        print(f"{YELLOW}Resolution     : {WHITE}{image.size[0]} x {image.size[1]}")

        size = os.path.getsize(image_path) / 1024
        print(f"{YELLOW}File Size      : {WHITE}{size:.2f} KB")

        exif_data = image.getexif()

        if not exif_data:
            print(f"\n{RED}[!] No EXIF Metadata Found!{RESET}")
            return

        print(f"""
{CYAN}==========================================================
                      EXIF METADATA
=========================================================={RESET}
""")

        gps_info = None

        for tag_id in exif_data:

            value = exif_data.get(tag_id)
            tag = TAGS.get(tag_id, tag_id)

            if tag == "GPSInfo":
                gps_info = value
                continue

            try:
                print(f"{GREEN}{tag:<25}:{WHITE} {value}")
            except:
                pass

        # GPS
        if gps_info:

            print(f"""
{CYAN}==========================================================
                     GPS INFORMATION
=========================================================={RESET}
""")

            latitude, longitude = extract_gps(gps_info)

            if latitude and longitude:

                print(f"{GREEN}Latitude        : {WHITE}{latitude}")
                print(f"{GREEN}Longitude       : {WHITE}{longitude}")

                maps = f"https://www.google.com/maps?q={latitude},{longitude}"

                print(f"{GREEN}Google Maps     : {WHITE}{maps}")

            else:
                print(f"{RED}[!] Unable To Decode GPS Data!{RESET}")

        else:
            print(f"\n{RED}[!] No GPS Metadata Found!{RESET}")

    except Exception as e:
        print(f"\n{RED}[ERROR] {e}{RESET}")

# ==========================================================
# MAIN
# ==========================================================

def main():

    banner()

    path = input(f"{CYAN}[?] Enter Image Path : {WHITE}").strip()

    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]

    extract_metadata(path)

    print(f"\n{GREEN}[✓] Scan Completed Successfully!{RESET}\n")

# ==========================================================

if __name__ == "__main__":
    main()
