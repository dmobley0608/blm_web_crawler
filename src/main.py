import requests
from bs4 import BeautifulSoup
import openpyxl
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch and parse a URL
def fetch_page(url):
    logging.info(f"Fetching URL: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

# Function to extract links with a specific class
def extract_links(soup, class_name):
    return [a['href'] for a in soup.find_all('a', class_=class_name)]

# Function to extract links with a specific property
def extract_canonical_links(soup):
    return [li.find('a')['href'] for li in soup.find_all('li', class_=False) if li.find('a')]


# Function to extract HMA and horse breeds
def extract_hma_and_breeds(soup):
    hma = soup.find('h1').get_text(strip=True)
    breeds = [breed.get_text(strip=True) for breed in soup.find_all('p')]
    return hma, breeds

# Main function to run the crawler
def main():
    base_url = "https://www.blm.gov"
    start_url = f"{base_url}/programs/wild-horse-and-burro/herd-management/herd-management-areas"

    logging.info("Starting the web crawler")

    error_count = 0

    try:
        # Fetch and parse the main page
        main_soup = fetch_page(start_url)

        # Extract state links
        state_links = extract_links(main_soup, 'blm-state')
        logging.info(f"Found {len(state_links)} state links")

        # Prepare Excel workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Horse Breeds"
        sheet.append(["State","HMA", "Breeds", "Colors"])
        #Horse Breeds
        common_horse_breeds = [
            "Arabian", "Quarter", "Thoroughbred", "Tennessee Walker",
            "Morgan", "Paint", "Appaloosa", "Miniature Horse", "Warmblood",
            "Andalusian", "Friesian", "Gypsy Vanner", "Mustang", "Clydesdale",
            "Percheron", "Shire", "Belgian", "Shetland Pony", "Welsh Pony",
            "Haflinger", "Icelandic", "Lipizzaner", "Paso Fino",
            "Rocky Mountain", "Standardbred", "Ranch", "Calvary" "Draft", "Homestead"   ]

        # Horse Colors
        common_horse_colors = [
            "Bay", "Black", "Chestnut", "Gray", "Palomino", "Buckskin",
            "Dun", "Grullo", "Roan", "Cremello", "Perlino", "Pinto",
            "Appaloosa", "White", "Sorrel"
        ]

        # Process each state link
        for state_link in state_links:
            try:
                state_url = f"{base_url}{state_link}"
                logging.info(f"Processing state URL: {state_url}")
                state_soup = fetch_page(state_url)

                # Extract canonical links
                canonical_links = extract_canonical_links(state_soup)
                logging.info(f"Found {len(canonical_links)} canonical links in state URL: {state_url}")

                # Process each canonical link
                for canonical_link in canonical_links:
                    try:
                        canonical_url = f"{base_url}{canonical_link}"
                        logging.info(f"Processing canonical URL: {canonical_url}")
                        canonical_soup = fetch_page(canonical_url)

                        # Extract HMA and breeds
                        hma = canonical_soup.find('h1').get_text(strip=True)
                        breeds = [breed for breed in common_horse_breeds if breed.lower() in canonical_soup.get_text().lower()]
                        colors = [color for color in common_horse_colors if color.lower() in canonical_soup.get_text().lower()]
                        logging.info(f"Extracted HMA: {hma} with breeds: {', '.join(breeds)}")
                        sheet.append([hma, ", ".join(breeds)])
                        state_name = state_soup.find('a', href=state_link).get_text(strip=True)
                        sheet.append([state_name, hma, ", ".join(breeds), ", ".join(colors)])
                    except Exception as e:
                        logging.error(f"Error processing canonical URL {canonical_url}: {e}")
                        error_count += 1
            except Exception as e:
                logging.error(f"Error processing state URL {state_url}: {e}")
                error_count += 1

        # Ensure the data directory exists
        os.makedirs("data", exist_ok=True)

        # Save the workbook
        workbook.save("data/output.xlsx")
        logging.info("Saved the workbook to data/output.xlsx")
    except Exception as e:
        logging.error(f"Error during main processing: {e}")
        error_count += 1

    logging.info(f"Total number of errors: {error_count}")

if __name__ == "__main__":
    main()