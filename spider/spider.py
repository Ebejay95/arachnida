# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joeberle <joeberle@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/18 11:37:35 by joeberle          #+#    #+#              #
#    Updated: 2024/11/18 12:07:08 by joeberle         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import argparse

def validate_depth(value):
    """Validate that the depth argument is a positive integer."""
    try:
        ivalue = int(value)
        if ivalue < 1:
            raise argparse.ArgumentTypeError(f"{value} is not a valid positive integer.")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer.")

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

    print("Downloading images... (to be implemented)")

if __name__ == "__main__":
    main()