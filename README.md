# Web Crawler for Horse Breeds and Colors

This web crawler fetches information about Herd Management Areas (HMA) and horse breeds from the Bureau of Land Management (BLM) website. The extracted data is saved into an Excel file.

## Features

- Fetches and parses web pages from the BLM website.
- Extracts links to state pages and canonical links.
- Extracts HMA names, horse breeds, and horse colors.
- Logs each step of the crawling process.
- Handles errors and continues execution.
- Saves the extracted data into an Excel file.

## Requirements

- Python 3.7+
- `requests` library
- `beautifulsoup4` library
- `openpyxl` library

## Installation

1. Clone the repository or download the source code.
2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On Unix or MacOS
    ```
3. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:
    ```sh
    python src/main.py
    ```
2. The script will log the progress and save the output to `data/output.xlsx`.

## Logging

The script uses the `logging` module to log the progress and errors. The log messages include timestamps and log levels.

## Error Handling

The script includes error handling to continue execution even if an error occurs. The total number of errors is printed at the end of the program.

## Output

The output is saved in an Excel file located at `data/output.xlsx`. The file contains the following columns:
- State
- HMA
- Breeds
- Colors

## License

This project is licensed under the MIT License.
