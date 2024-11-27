# Cybersecurity Piscine – Arachnida

**Exploring web scraping and metadata manipulation.**

---

## Summary

**Arachnida** is an introductory project in the Cybersecurity Piscine that focuses on web scraping and metadata analysis. You will develop two programs: one to download images from websites and another to analyze the metadata of these files. This project emphasizes data processing, web requests, and understanding metadata.

---

## Features

### Core Functionality

1. **Spider Program**:
   - Extracts and downloads all images from a given website URL.
   - Supports recursive downloads with customizable depth.
   - Saves images in specified formats (`.jpg`, `.png`, `.gif`, `.bmp`).

2. **Scorpion Program**:
   - Parses and displays metadata from image files.
   - Handles attributes like creation date and EXIF data.
   - Compatible with the same file types as the Spider program.

---

## Structure

### Directories and Files

- **`spider/`**:
  - Contains the implementation of the `spider` program for web scraping.

- **`scorpion/`**:
  - Contains the implementation of the `scorpion` program for metadata analysis.

- **`Makefile`**:
  - Automates compilation (if applicable) and sets up the project environment.

---

## Usage

### Spider Program

The `spider` program extracts images from a website recursively.

**Command**:
```bash
./spider [-rlp] URL
```

## Options:

-r: Enables recursive downloading of images.
-r -l [N]: Sets the maximum depth level for recursion (default: 5).
-p [PATH]: Specifies the download directory (default: ./data/).

## Example:
```
./spider -r -l 3 -p ./images https://example.com
```

This command recursively downloads images from https://example.com up to a depth of 3 and saves them in the ./images directory.

## Scorpion Program
The scorpion program analyzes and displays metadata from image files.

### Command:
```
./scorpion FILE1 [FILE2 ...]
```
### Example:
```
./scorpion image1.jpg image2.png
```
This command parses metadata from image1.jpg and image2.png, displaying EXIF and creation date information.

### Requirements
Mandatory Part

## Spider Program:

Recursively downloads images with specified options.
Handles file extensions: .jpg, .jpeg, .png, .gif, .bmp.

### Scorpion Program:
Parses metadata from image files.
Displays attributes such as creation date and EXIF data.

### General Rules:
Use your own implementation for HTTP requests and file handling.
Avoid third-party tools like wget or scrapy.
Learning Outcomes

### Web Scraping Basics:
Learn to process and extract data from websites programmatically.

### Metadata Handling:
Understand and manipulate EXIF and other file metadata.

### Custom Implementations:
Build HTTP requests and file handling logic from scratch.

### Cybersecurity Awareness:
Gain insights into metadata security and its potential implications.

Arachnida – Unraveling the web of data and metadata! 🕸️
