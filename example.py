"""
Example usage of the Web Crawler

This script demonstrates how to use the WebCrawler class
"""

from crawler import WebCrawler
import json


def crawl_example_site():
    """Crawl example.com and display results."""
    print("Starting web crawler...")
    print("-" * 60)
    
    # Create a crawler instance
    crawler = WebCrawler(
        start_url='https://example.com',
        max_depth=1,
        max_pages=5,
        delay=1.0
    )
    
    # Start crawling
    print(f"Crawling: {crawler.start_url}")
    print(f"Max depth: {crawler.max_depth}")
    print(f"Max pages: {crawler.max_pages}")
    print("-" * 60)
    
    pages = crawler.crawl()
    
    # Display results
    print("\n" + "=" * 60)
    print("CRAWL RESULTS")
    print("=" * 60)
    
    results = crawler.get_results()
    print(f"\nTotal pages crawled: {results['total_pages_crawled']}")
    print(f"\nVisited URLs:")
    for url in results['visited_urls']:
        print(f"  - {url}")
    
    print("\n" + "-" * 60)
    print("Page Details:")
    print("-" * 60)
    
    for i, page in enumerate(pages, 1):
        print(f"\n{i}. {page['title']}")
        print(f"   URL: {page['url']}")
        if page['description']:
            print(f"   Description: {page['description']}")
        print(f"   Content preview: {page['content_preview'][:150]}...")
    
    # Optionally save to JSON file
    output_file = 'crawl_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nResults saved to {output_file}")


def crawl_custom_site(url, max_depth=2, max_pages=20):
    """
    Crawl a custom website.
    
    Args:
        url: The URL to crawl
        max_depth: Maximum crawling depth
        max_pages: Maximum number of pages to crawl
    """
    print(f"Crawling {url}...")
    
    crawler = WebCrawler(
        start_url=url,
        max_depth=max_depth,
        max_pages=max_pages,
        delay=1.0
    )
    
    pages = crawler.crawl()
    results = crawler.get_results()
    
    print(f"\nCrawled {results['total_pages_crawled']} pages from {url}")
    
    return results


if __name__ == '__main__':
    # Run the example
    crawl_example_site()
    
    # Uncomment to crawl a different site:
    # crawl_custom_site('https://your-website.com', max_depth=2, max_pages=10)
