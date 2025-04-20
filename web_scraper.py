import requests
from bs4 import BeautifulSoup
import time
import logging
from urllib.parse import urljoin
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, base_url, delay=1):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        # Set a realistic user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_page_content(self, url):
        """
        Fetches and parses a web page with error handling
        """
        try:
            # Implement rate limiting
            time.sleep(self.delay)
            
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def extract_text(self, url):
        """
        Extracts clean text content from a webpage
        """
        content = self.get_page_content(url)
        if not content:
            return None

        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.select('script, style, meta, [class*="ad"], [id*="ad"], .advertisement'):
                element.decompose()

            # Extract text from main content area
            # Adjust these selectors based on the target website's structure
            main_content = soup.select('article, .content, .main, main, #main')
            
            if main_content:
                text_content = main_content[0].get_text(separator='\n', strip=True)
            else:
                text_content = soup.get_text(separator='\n', strip=True)

            return text_content

        except Exception as e:
            logger.error(f"Error parsing {url}: {str(e)}")
            return None

    def save_to_markdown(self, content, output_file):
        """
        Saves the extracted content to a markdown file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Scraped Content\n\n")
                f.write(f"Source: {self.base_url}\n\n")
                f.write(content)
            logger.info(f"Content saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving to file: {str(e)}")

def main():
    # Example usage
    url = "https://blog.apify.com/the-definitive-guide-to-text-scraping/"
    scraper = WebScraper(url)
    content = scraper.extract_text(url)
    
    if content:
        scraper.save_to_markdown(content, 'scraped_content.md')

if __name__ == "__main__":
    main()