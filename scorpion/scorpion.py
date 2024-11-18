# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joeberle <joeberle@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 16:51:58 by joeberle          #+#    #+#              #
#    Updated: 2024/11/18 17:38:57 by joeberle         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS

# Function to get exif data and group them
def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if exif_data is not None:
            print(f"\nEXIF-Data for {image_path}:")
            
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
                print("\n-- Image Information --")
                for key, value in image_info.items():
                    print(f"{key}: {value}")
            
            if camera_settings:
                print("\n-- Camera Settings --")
                for key, value in camera_settings.items():
                    print(f"{key}: {value}")
            
            if gps_info:
                print("\n-- GPS Information --")
                for key, value in gps_info.items():
                    print(f"{key}: {value}")
            
            if other_info:
                print("\n-- Other Information --")
                for key, value in other_info.items():
                    print(f"{key}: {value}")
            
        else:
            print(f"No EXIF data for {image_path}.")
    
    except Exception as e:
        print(f"Error while processing file {image_path}: {e}")

# Function to scan a directory for images
def process_images_from_path(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    file_path = os.path.join(root, file)
                    get_exif_data(file_path)
    else:
        print(f"{path} is not a directory or does not exist.")

# Main function for parsing arguments
def main():
    if len(sys.argv) < 2:
        print("Usage: ./scorpion <FILE1> [FILE2 ...] or <PATH>")
        sys.exit(1)

    path_or_files = sys.argv[1:]
    
    if os.path.isdir(path_or_files[0]):
        process_images_from_path(path_or_files[0])
    else:
        for file in path_or_files:
            if os.path.isfile(file):
                get_exif_data(file)
            else:
                print(f"File {file} not found.")

if __name__ == "__main__":
    main()