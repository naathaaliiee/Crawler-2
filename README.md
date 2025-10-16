# Crawler-2

A simple and efficient web crawler built with Python that can traverse websites, extract links, and gather information from web pages.

## Features

- 🕷️ Crawl websites starting from a given URL
- 🔗 Extract and follow links automatically
- 📊 Collect page data (title, description, content)
- ⚙️ Configurable crawling depth and page limits
- 🛡️ Domain filtering to stay within allowed domains
- ⏱️ Polite crawling with configurable delays
- 📝 Comprehensive logging
- ✅ Unit tests included

## Installation

1. Clone the repository:
```bash
git clone https://github.com/naathaaliiee/Crawler-2.git
cd Crawler-2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from crawler import WebCrawler

# Create a crawler instance
crawler = WebCrawler(
    start_url='https://example.com',
    max_depth=2,        # How many links deep to crawl
    max_pages=50,       # Maximum number of pages to crawl
    delay=1.0           # Delay between requests (seconds)
)

# Start crawling
pages = crawler.crawl()

# Get results
results = crawler.get_results()
print(f"Crawled {results['total_pages_crawled']} pages")
```

### Running the Example

Run the included example script:
```bash
python example.py
```

This will crawl example.com and save results to `crawl_results.json`.

### Configuration

You can customize the crawler behavior by passing parameters:

```python
crawler = WebCrawler(
    start_url='https://example.com',
    max_depth=3,                              # Crawl up to 3 links deep
    max_pages=100,                            # Crawl up to 100 pages
    delay=2.0,                                # 2 second delay between requests
    allowed_domains=['example.com', 'test.com']  # Only crawl these domains
)
```

### Output Format

The crawler returns data in the following format:

```python
{
    'start_url': 'https://example.com',
    'total_pages_crawled': 10,
    'visited_urls': ['url1', 'url2', ...],
    'pages': [
        {
            'url': 'https://example.com',
            'title': 'Page Title',
            'description': 'Meta description',
            'content_preview': 'First 500 characters of content...'
        },
        ...
    ]
}
```

## Running Tests

Run the test suite with pytest:
```bash
pytest test_crawler.py -v
```

## Project Structure

```
Crawler-2/
├── crawler.py          # Main crawler implementation
├── example.py          # Example usage script
├── config.py           # Configuration file
├── test_crawler.py     # Unit tests
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Features in Detail

### Link Extraction
The crawler automatically extracts all links from pages and follows them up to the specified depth.

### Domain Filtering
By default, the crawler only follows links within the same domain as the start URL. You can specify multiple allowed domains.

### Polite Crawling
The crawler includes a configurable delay between requests to avoid overwhelming servers.

### Error Handling
The crawler handles common errors gracefully:
- Network timeouts
- Invalid URLs
- HTTP errors
- Parsing errors

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- urllib3
- pytest (for running tests)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.