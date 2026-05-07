#!/usr/bin/env python3

# =====================================================
#        ██╗  ██╗██████╗ ███╗   ██╗
#        ██║  ██║██╔══██╗████╗  ██║
#        ███████║██║  ██║██╔██╗ ██║
#        ██╔══██║██║  ██║██║╚██╗██║
#        ██║  ██║██████╔╝██║ ╚████║
#        ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═══╝
#
#      H A S N A I N   D A R K N E T
# ---------------------------------------------
#        PROFESSIONAL METADATA EXTRACTOR
# =====================================================

# Install:
# pip install pillow

import os
import time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# =====================================================
# Colors
# =====================================================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# =====================================================
# Banner
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

{CYAN}========================================================
        H A S N A I N   D A R K N E T
--------------------------------------------------------
        PROFESSIONAL METADATA EXTRACTOR
========================================================
{RESET}
""")

# =====================================================
# GPS Converter
# =====================================================

def convert_to_degrees(value):

    d = float(value[0])
    m = float(value[1])
    s = float(value[2])

    return d + (m / 60.0) + (s / 3600.0)

# =====================================================
# GPS Extraction
# =====================================================

def extract_gps_info(gps_info):

    gps_data = {}

    for key in gps_info.keys():
        decode = GPSTAGS.get(key, key)
        gps_data[decode] = gps_info[key]

    try:
        latitude = convert_to_degrees(gps_data['GPSLatitude'])
        latitude_ref = gps_data['GPSLatitudeRef']

        longitude = convert_to_degrees(gps_data['GPSLongitude'])
        longitude_ref = gps_data['GPSLongitudeRef']

        if latitude_ref != "N":
            latitude = -latitude

        if longitude_ref != "E":
            longitude = -longitude

        return latitude, longitude

    except:
        return None, None

# =====================================================
# Metadata Extractor
# =====================================================

def extract_metadata(image_path):

    if not os.path.exists(image_path):
        print(f"{RED}[!] File Not Found!{RESET}")
        return

    try:

        image = Image.open(image_path)

        print(f"{GREEN}[+] Loading Image Metadata...{RESET}")
        time.sleep(1)

        print(f"""
{CYAN}========================================================
                    BASIC INFORMATION
========================================================{RESET}
""")

        print(f"{YELLOW}File Name      : {WHITE}{os.path.basename(image_path)}")
        print(f"{YELLOW}Image Format   : {WHITE}{image.format}")
        print(f"{YELLOW}Image Mode     : {WHITE}{image.mode}")
        print(f"{YELLOW}Resolution     : {WHITE}{image.size[0]} x {image.size[1]}")

        file_size = os.path.getsize(image_path) / 1024
        print(f"{YELLOW}File Size      : {WHITE}{file_size:.2f} KB")

        print()

        exif_data = image._getexif()

        if not exif_data:
            print(f"{RED}[!] No EXIF Metadata Found!{RESET}")
            return

        print(f"""
{CYAN}========================================================
                     EXIF METADATA
========================================================{RESET}
""")

        gps_data = None

        for tag_id, value in exif_data.items():

            tag = TAGS.get(tag_id, tag_id)

            if tag == "GPSInfo":
                gps_data = value
                continue

            print(f"{GREEN}{tag:<25}:{WHITE} {value}")

        # GPS Info
        if gps_data:

            print(f"""
{CYAN}========================================================
                     GPS INFORMATION
========================================================{RESET}
""")

            latitude, longitude = extract_gps_info(gps_data)

            if latitude and longitude:

                print(f"{GREEN}Latitude        : {WHITE}{latitude}")
                print(f"{GREEN}Longitude       : {WHITE}{longitude}")

                maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"

                print(f"{GREEN}Google Maps     : {WHITE}{maps_url}")

            else:
                print(f"{RED}[!] GPS Found But Unable To Decode!{RESET}")

        else:
            print(f"{RED}[!] No GPS Metadata Found!{RESET}")

    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    banner()

    image_path = input(f"{CYAN}[?] Enter Image Path : {WHITE}")

    extract_metadata(image_path)

    print(f"\n{GREEN}[✓] Scan Completed Successfully!{RESET}\n")
