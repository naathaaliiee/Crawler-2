"""
Web Crawler Module

A simple web crawler that can traverse websites and extract information.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, List, Optional
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebCrawler:
    """
    A simple web crawler that can fetch and parse web pages.
    
    Attributes:
        start_url (str): The starting URL for crawling
        max_depth (int): Maximum depth to crawl
        max_pages (int): Maximum number of pages to crawl
        delay (float): Delay between requests in seconds
        allowed_domains (List[str]): List of allowed domains to crawl
    """
    
    def __init__(
        self,
        start_url: str,
        max_depth: int = 2,
        max_pages: int = 50,
        delay: float = 1.0,
        allowed_domains: Optional[List[str]] = None
    ):
        """
        Initialize the web crawler.
        
        Args:
            start_url: The URL to start crawling from
            max_depth: Maximum depth to crawl (default: 2)
            max_pages: Maximum number of pages to crawl (default: 50)
            delay: Delay between requests in seconds (default: 1.0)
            allowed_domains: List of allowed domains, defaults to start_url domain
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        
        # Parse the start URL domain
        parsed_url = urlparse(start_url)
        self.allowed_domains = allowed_domains or [parsed_url.netloc]
        
        # Track visited URLs and pages to visit
        self.visited_urls: Set[str] = set()
        self.pages_data: List[dict] = []
        
    def is_valid_url(self, url: str) -> bool:
        """
        Check if a URL is valid and within allowed domains.
        
        Args:
            url: The URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            parsed = urlparse(url)
            
            # Check if URL has a scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Check if domain is allowed
            if self.allowed_domains and parsed.netloc not in self.allowed_domains:
                return False
            
            # Check if URL has already been visited
            if url in self.visited_urls:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return False
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch the content of a web page.
        
        Args:
            url: The URL to fetch
            
        Returns:
            str: The HTML content of the page, or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; WebCrawler/1.0)'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_links(self, html: str, base_url: str) -> Set[str]:
        """
        Extract all links from HTML content.
        
        Args:
            html: The HTML content to parse
            base_url: The base URL for resolving relative links
            
        Returns:
            Set[str]: Set of absolute URLs found in the page
        """
        links = set()
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                # Convert relative URLs to absolute
                absolute_url = urljoin(base_url, href)
                
                # Remove fragment identifiers
                absolute_url = absolute_url.split('#')[0]
                
                if self.is_valid_url(absolute_url):
                    links.add(absolute_url)
        except Exception as e:
            logger.error(f"Error extracting links from {base_url}: {e}")
        
        return links
    
    def extract_page_data(self, html: str, url: str) -> dict:
        """
        Extract useful data from a page.
        
        Args:
            html: The HTML content to parse
            url: The URL of the page
            
        Returns:
            dict: Dictionary containing page data
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else 'No title'
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '').strip() if meta_desc else ''
            
            # Extract all text content (first 500 characters)
            text_content = soup.get_text()
            text_content = ' '.join(text_content.split())[:500]
            
            return {
                'url': url,
                'title': title_text,
                'description': description,
                'content_preview': text_content
            }
        except Exception as e:
            logger.error(f"Error extracting data from {url}: {e}")
            return {
                'url': url,
                'title': 'Error',
                'description': '',
                'content_preview': ''
            }
    
    def crawl(self) -> List[dict]:
        """
        Start crawling from the start URL.
        
        Returns:
            List[dict]: List of dictionaries containing data from crawled pages
        """
        # Initialize the queue with the start URL and depth 0
        queue = [(self.start_url, 0)]
        
        logger.info(f"Starting crawl from {self.start_url}")
        logger.info(f"Max depth: {self.max_depth}, Max pages: {self.max_pages}")
        
        while queue and len(self.visited_urls) < self.max_pages:
            url, depth = queue.pop(0)
            
            # Skip if already visited or exceeded max depth
            if url in self.visited_urls or depth > self.max_depth:
                continue
            
            logger.info(f"Crawling ({len(self.visited_urls) + 1}/{self.max_pages}): {url} (depth: {depth})")
            
            # Mark as visited
            self.visited_urls.add(url)
            
            # Fetch the page
            html = self.fetch_page(url)
            if not html:
                continue
            
            # Extract and store page data
            page_data = self.extract_page_data(html, url)
            self.pages_data.append(page_data)
            
            # Extract links and add to queue if not at max depth
            if depth < self.max_depth:
                links = self.extract_links(html, url)
                for link in links:
                    if link not in self.visited_urls:
                        queue.append((link, depth + 1))
            
            # Be polite - delay between requests
            time.sleep(self.delay)
        
        logger.info(f"Crawling complete. Visited {len(self.visited_urls)} pages")
        return self.pages_data
    
    def get_results(self) -> dict:
        """
        Get crawling results as a dictionary.
        
        Returns:
            dict: Dictionary containing crawl statistics and page data
        """
        return {
            'start_url': self.start_url,
            'total_pages_crawled': len(self.visited_urls),
            'pages': self.pages_data,
            'visited_urls': list(self.visited_urls)
        }


def main():
    """Example usage of the WebCrawler."""
    # Example: Crawl a website
    crawler = WebCrawler(
        start_url='https://example.com',
        max_depth=2,
        max_pages=10,
        delay=1.0
    )
    
    # Start crawling
    results = crawler.crawl()
    
    # Print results
    print(f"\nCrawled {len(results)} pages:")
    for page in results:
        print(f"\nTitle: {page['title']}")
        print(f"URL: {page['url']}")
        print(f"Description: {page['description']}")
        print(f"Content preview: {page['content_preview'][:100]}...")


if __name__ == '__main__':
    main()
