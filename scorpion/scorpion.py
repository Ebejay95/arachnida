# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joeberle <joeberle@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 16:51:58 by joeberle          #+#    #+#              #
#    Updated: 2024/11/18 20:22:47 by joeberle         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from colorama import init, Fore, Style

# Initialize colorama
init()

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if exif_data is not None and len(exif_data) > 0:
            print(f"\n{Fore.CYAN}EXIF-Data for {Fore.YELLOW}{image_path}{Style.RESET_ALL}:")
            
            # Grouped output for EXIF data
            image_info = {}
            camera_settings = {}
            gps_info = {}
            other_info = {}
            
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                
                if tag_name in ["Make", "Model", "ExposureTime", "FNumber", "ISOSpeedRatings", "FocalLength", "WhiteBalance"]:
                    camera_settings[tag_name] = value
                elif tag_name in ["DateTime", "Software", "ImageWidth", "ImageHeight"]:
                    image_info[tag_name] = value
                elif tag_name in ["GPSLatitude", "GPSLongitude"]:
                    gps_info[tag_name] = value
                else:
                    other_info[tag_name] = value
            
            # Print grouped categories
            if image_info:
                print(f"\n{Fore.GREEN}-- Image Information --{Style.RESET_ALL}")
                for key, value in image_info.items():
                    print(f"{Fore.WHITE}{key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")
            
            if camera_settings:
                print(f"\n{Fore.GREEN}-- Camera Settings --{Style.RESET_ALL}")
                for key, value in camera_settings.items():
                    print(f"{Fore.WHITE}{key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")
            
            if gps_info:
                print(f"\n{Fore.GREEN}-- GPS Information --{Style.RESET_ALL}")
                for key, value in gps_info.items():
                    print(f"{Fore.WHITE}{key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")
            
            if other_info:
                print(f"\n{Fore.GREEN}-- Other Information --{Style.RESET_ALL}")
                for key, value in other_info.items():
                    print(f"{Fore.WHITE}{key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")
        
        else:
            print(f"{Fore.RED}No EXIF data for {image_path}.{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}Error while processing file {image_path}: {e}{Style.RESET_ALL}")

def process_images_from_path(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    file_path = os.path.join(root, file)
                    get_exif_data(file_path)
    else:
        print(f"{Fore.RED}{path} is not a directory or does not exist.{Style.RESET_ALL}")

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: ./scorpion <FILE1> [FILE2 ...] or <PATH>{Style.RESET_ALL}")
        sys.exit(1)
    
    path_or_files = sys.argv[1:]
    
    if os.path.isdir(path_or_files[0]):
        process_images_from_path(path_or_files[0])
    else:
        for file in path_or_files:
            if os.path.isfile(file):
                get_exif_data(file)
            else:
                print(f"{Fore.RED}File {file} not found.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()