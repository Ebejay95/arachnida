# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joeberle <joeberle@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 11:37:35 by joeberle          #+#    #+#              #
#    Updated: 2024/11/18 13:25:55 by joeberle         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Imports
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import sys
from colorama import init, Fore, Style

# Inits
init(autoreset=True)
downloaded_images = set()

# Check if a URL is valid.
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Validate that the depth argument is a positive integer.
def validate_depth(value):
    try:
        ivalue = int(value)
        if ivalue < 1:
            raise argparse.ArgumentTypeError(f"{value} is not a valid positive integer.")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer.")

# Fetch all links from a given URL.
def fetch_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href")
            full_url = urljoin(url, href)
            if is_valid_url(full_url):
                links.add(full_url)
        return links
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching {url}: {e}{Style.RESET_ALL}")
        return set()

# Check if the URL has a valid image extension.
def is_valid_image_extension(url):
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    filename = os.path.basename(urlparse(url).path).lower()
    return any(filename.endswith(ext) for ext in valid_extensions)

# Fetch and download all images from a given URL.
def fetch_images(url, output_path, indent_level=0):
    indent = "  " * indent_level
    images_found = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")
        
        if img_tags:
            print(f"{indent}{Fore.CYAN}Images detected on {Fore.YELLOW}{url}{Style.RESET_ALL}:")
        
        for img in img_tags:
            img_url = img.get("src")
            if img_url:
                full_url = urljoin(url, img_url)
                if is_valid_url(full_url) and is_valid_image_extension(full_url):
                    images_found.append(full_url)
                    if full_url not in downloaded_images:
                        print(f"{indent}→ {Fore.BLUE}{full_url}{Style.RESET_ALL}")
                    success = download_image(full_url, output_path)
                    if success and not full_url in downloaded_images:
                        print(f"{indent}  {Fore.GREEN}✓ Downloaded successfully{Style.RESET_ALL}")
                    elif not success and not full_url in downloaded_images:
                        print(f"{indent}  {Fore.RED}✗ Download failed{Style.RESET_ALL}")
        
        if not img_tags:
            print(f"{indent}{Fore.YELLOW}No images found here!{Style.RESET_ALL}")
            
        return images_found
            
    except requests.RequestException as e:
        print(f"{indent}{Fore.RED}Error fetching images from {url}: {e}{Style.RESET_ALL}")
        return images_found

# Download an image and save it to the output path.
def download_image(img_url, output_path):
    global downloaded_images

    if not is_valid_image_extension(img_url):
        print(f"{Fore.YELLOW}Skipping {img_url}: Not a supported image format{Style.RESET_ALL}")
        return False
    
    if img_url in downloaded_images:
        print(f"{Fore.YELLOW}Skipping {img_url}: Already downloaded{Style.RESET_ALL}")
        return False
        
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        filename = os.path.basename(urlparse(img_url).path)
        filepath = os.path.join(output_path, filename)
        
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
                
        downloaded_images.add(img_url)
        print(f"{Fore.GREEN}Downloaded: {filepath}{Style.RESET_ALL}")
        return True
        
    except requests.RequestException as e:
        if img_url not in downloaded_imar.add_argument(
        "-l",

def crawl(url, depth, visited=None, output_path="./data/"):
    if visited is None:
        visited = set()

    if depth == 0 or url in visited:
        return

    print(f"\n{Fore.MAGENTA}Crawling: {url} (depth {depth}){Style.RESET_ALL}")
    visited.add(url)

    fetch_images(url, output_path)

    links = fetch_links(url)
    for link in links:
        crawl(link, depth - 1, visited, output_path)

def main():
    parser = argparse.ArgumentParser(
        description="Spider program to recursively download images from a website."
    )
    parser.add_argument(
        "-r",
        action="store_true",
        help="Enable recursive download."
    )
    parser.add_argument(
        "-l",
        type=validate_depth,
        metavar="N",
        help="Maximum depth level for recursive download (default: 5)."
    )
    parser.add_argument(
        "-p",
        type=str,
        metavar="PATH",
        default="./data/",
        help="Path to save downloaded files (default: ./data/)."
    )
    parser.add_argument(
        "URL",
        type=str,
        help="The URL to crawl for images."
    )

    args = parser.parse_args()

    if args.l and not args.r:
        print(f"{Fore.RED}Error: The -l option requires the -r option to be enabled.{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.abspath(args.p)
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except OSError as e:
            print(f"{Fore.RED}Error creating directory {output_path}: {e}{Style.RESET_ALL}", file=sys.stderr)
            sys.exit(1)

    print(f"\n{Fore.CYAN}Configuration:{Style.RESET_ALL}")
    print(f"Recursive: {Fore.YELLOW}{args.r}{Style.RESET_ALL}")
    print(f"Depth: {Fore.YELLOW}{args.l if args.l else 5}{Style.RESET_ALL}")
    print(f"Output Path: {Fore.YELLOW}{output_path}{Style.RESET_ALL}")
    print(f"Target URL: {Fore.YELLOW}{args.URL}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}Starting download...{Style.RESET_ALL}")

    if args.r and args.l:
        crawl(args.URL, args.l)
    else:
        crawl(args.URL, 1)

if __name__ == "__main__":
    main()