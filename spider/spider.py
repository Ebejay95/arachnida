# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joeberle <joeberle@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 11:37:35 by joeberle          #+#    #+#              #
#    Updated: 2024/11/18 12:26:17 by joeberle         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

def is_valid_url(url):
    """Check if a URL is valid."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def validate_depth(value):
    """Validate that the depth argument is a positive integer."""
    try:
        ivalue = int(value)
        if ivalue < 1:
            raise argparse.ArgumentTypeError(f"{value} is not a valid positive integer.")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer.")

def fetch_links(url):
    """Fetch all links from a given URL."""
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
        print(f"Error fetching {url}: {e}")
        return set()

def fetch_images(url, output_path, indent_level=0):
    """Fetch and download all images from a given URL."""
    indent = "\t" * indent_level
    images_found = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")
        
        if img_tags:
            print(f"{indent}Images detected on {url}:")
        
        for img in img_tags:
            img_url = img.get("src")
            if img_url:
                full_url = urljoin(url, img_url)
                if is_valid_url(full_url):
                    images_found.append(full_url)
                    print(f"{indent}\t→ {full_url}")
                    success = download_image(full_url, output_path)
                    status = "✓" if success else "✗"
                    print(f"{indent}\t  {status} {'Downloaded' if success else 'Error downloading'}")
        
        if not img_tags:
            print(f"{indent}No images found here!")
            
        return images_found
            
    except requests.RequestException as e:
        print(f"{indent}Error fetching images from {url}: {e}")
        return images_found

def download_image(img_url, output_path):
    """Download an image and save it to the output path."""
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        filename = os.path.basename(urlparse(img_url).path)
        filepath = os.path.join(output_path, filename)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {filepath}")
    except requests.RequestException as e:
        print(f"Error downloading {img_url}: {e}")


def crawl(url, depth, visited=None, output_path="./data/"):
    if visited is None:
        visited = set()

    if depth == 0 or url in visited:
        return

    print(f"Crawling: {url} (depth {depth})")
    visited.add(url)

    # Fetch images from current page
    fetch_images(url, output_path)

    # Fetch links and crawl them
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

    # Check if -l is used without -r
    if args.l and not args.r:
        print("Error: The -l option requires the -r option to be enabled.", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.abspath(args.p)
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except OSError as e:
            print(f"Error creating directory {output_path}: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Recursive: {args.r}")
    print(f"Depth: {args.l if args.l else 5}")
    print(f"Output Path: {output_path}")
    print(f"Target URL: {args.URL}")

    print("Downloading images...")

    if args.r and args.l:
        crawl(args.URL, args.l)
    else:
        crawl(args.URL, 1)

if __name__ == "__main__":
    main()