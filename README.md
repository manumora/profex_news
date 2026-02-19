# Profex News Extractor

## Overview
This Python script extracts the latest news from the **Profex** educational portal (Department of Education and Employment of Extremadura, Spain). It processes the web content to generate a custom HTML file with a modern and clean aesthetic, perfect for information displays or web browsers.

## Features
- Extracts the 5 most recent news items from the Profex portal.
- Generates a standalone HTML file with a responsive and modern design (Apple-inspired style).
- **Automatic Highlighting**: Visually identifies and highlights news published today with a subtle animation.
- **Auto-refresh**: The generated HTML includes a script to automatically refresh itself every 30 minutes.
- Light and dark mode support (system preference).
- Converts relative links to absolute URLs to ensure content accessibility from the generated file.

## Requirements
- Python 3.x
- Dependencies listed in `requirements.txt` (`requests`, `beautifulsoup4`)

## Installation

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Simply run the script:
```bash
python profex_noticias.py
```

The script will:
1. Connect to the Profex portal (`https://profex.educarex.es/`).
2. Parse the content and extract relevant information (date, category, and headline).
3. Generate a file named `profex.html` in the output directory (default is `/var/www/html/`).

## Configuration
At the top of the `profex_noticias.py` file, you can adjust variables such as:
- `output_dir`: The directory where the `profex.html` file will be saved.
- `headers`: The User-Agent used for the web request.
