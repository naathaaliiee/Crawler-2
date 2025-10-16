"""
Unit tests for the Web Crawler
"""

import pytest
from crawler import WebCrawler
from unittest.mock import Mock, patch, MagicMock


class TestWebCrawler:
    """Test cases for the WebCrawler class."""
    
    def test_initialization(self):
        """Test crawler initialization with default parameters."""
        crawler = WebCrawler('https://example.com')
        
        assert crawler.start_url == 'https://example.com'
        assert crawler.max_depth == 2
        assert crawler.max_pages == 50
        assert crawler.delay == 1.0
        # Verify domain was properly extracted from start_url
        assert crawler.allowed_domains == ['example.com']
        assert len(crawler.visited_urls) == 0
        assert len(crawler.pages_data) == 0
    
    def test_initialization_with_custom_params(self):
        """Test crawler initialization with custom parameters."""
        crawler = WebCrawler(
            'https://example.com',
            max_depth=3,
            max_pages=100,
            delay=2.0,
            allowed_domains=['example.com', 'test.com']
        )
        
        assert crawler.max_depth == 3
        assert crawler.max_pages == 100
        assert crawler.delay == 2.0
        assert crawler.allowed_domains == ['example.com', 'test.com']
    
    def test_is_valid_url_with_valid_url(self):
        """Test URL validation with a valid URL."""
        crawler = WebCrawler('https://example.com')
        
        assert crawler.is_valid_url('https://example.com/page1')
        assert crawler.is_valid_url('https://example.com/page2')
    
    def test_is_valid_url_with_invalid_domain(self):
        """Test URL validation with disallowed domain."""
        crawler = WebCrawler('https://example.com')
        
        # Different domain should not be valid
        assert not crawler.is_valid_url('https://otherdomain.com/page')
    
    def test_is_valid_url_with_visited_url(self):
        """Test URL validation with already visited URL."""
        crawler = WebCrawler('https://example.com')
        crawler.visited_urls.add('https://example.com/page1')
        
        assert not crawler.is_valid_url('https://example.com/page1')
    
    def test_is_valid_url_with_invalid_url(self):
        """Test URL validation with invalid URL format."""
        crawler = WebCrawler('https://example.com')
        
        assert not crawler.is_valid_url('not-a-valid-url')
        assert not crawler.is_valid_url('javascript:void(0)')
    
    @patch('crawler.requests.get')
    def test_fetch_page_success(self, mock_get):
        """Test successful page fetch."""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = '<html><body>Test content</body></html>'
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        crawler = WebCrawler('https://example.com')
        html = crawler.fetch_page('https://example.com')
        
        assert html == '<html><body>Test content</body></html>'
        mock_get.assert_called_once()
    
    @patch('crawler.requests.get')
    def test_fetch_page_failure(self, mock_get):
        """Test page fetch with network error."""
        # Mock failed response
        mock_get.side_effect = Exception('Network error')
        
        crawler = WebCrawler('https://example.com')
        html = crawler.fetch_page('https://example.com')
        
        assert html is None
    
    def test_extract_links(self):
        """Test link extraction from HTML."""
        html = '''
        <html>
            <body>
                <a href="https://example.com/page1">Page 1</a>
                <a href="/page2">Page 2</a>
                <a href="https://otherdomain.com/page3">Page 3</a>
            </body>
        </html>
        '''
        
        crawler = WebCrawler('https://example.com')
        links = crawler.extract_links(html, 'https://example.com')
        
        # Should extract valid links from same domain
        assert 'https://example.com/page1' in links
        assert 'https://example.com/page2' in links
        # Should not include links from other domains
        assert 'https://otherdomain.com/page3' not in links
    
    def test_extract_page_data(self):
        """Test page data extraction."""
        html = '''
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="This is a test page">
            </head>
            <body>
                <h1>Welcome</h1>
                <p>This is test content for the crawler.</p>
            </body>
        </html>
        '''
        
        crawler = WebCrawler('https://example.com')
        data = crawler.extract_page_data(html, 'https://example.com')
        
        assert data['url'] == 'https://example.com'
        assert data['title'] == 'Test Page'
        assert data['description'] == 'This is a test page'
        assert 'Welcome' in data['content_preview']
    
    @patch('crawler.WebCrawler.fetch_page')
    @patch('crawler.time.sleep')
    def test_crawl_basic(self, mock_sleep, mock_fetch):
        """Test basic crawling functionality."""
        # Mock HTML with links
        html = '''
        <html>
            <head><title>Test Page</title></head>
            <body>
                <a href="https://example.com/page1">Page 1</a>
            </body>
        </html>
        '''
        
        mock_fetch.return_value = html
        
        crawler = WebCrawler('https://example.com', max_depth=1, max_pages=2)
        results = crawler.crawl()
        
        assert len(results) > 0
        # Verify the start URL was visited
        assert len(crawler.visited_urls) > 0
        start_url_visited = any(url == 'https://example.com' for url in crawler.visited_urls)
        assert start_url_visited
    
    @patch('crawler.WebCrawler.fetch_page')
    @patch('crawler.time.sleep')
    def test_crawl_respects_max_pages(self, mock_sleep, mock_fetch):
        """Test that crawler respects max_pages limit."""
        html = '''
        <html>
            <head><title>Test Page</title></head>
            <body>
                <a href="https://example.com/page1">Page 1</a>
                <a href="https://example.com/page2">Page 2</a>
                <a href="https://example.com/page3">Page 3</a>
            </body>
        </html>
        '''
        
        mock_fetch.return_value = html
        
        crawler = WebCrawler('https://example.com', max_depth=2, max_pages=2)
        results = crawler.crawl()
        
        # Should not crawl more than max_pages
        assert len(crawler.visited_urls) <= 2
    
    def test_get_results(self):
        """Test getting crawl results."""
        crawler = WebCrawler('https://example.com')
        crawler.visited_urls.add('https://example.com')
        crawler.pages_data.append({
            'url': 'https://example.com',
            'title': 'Test',
            'description': 'Test page',
            'content_preview': 'Content'
        })
        
        results = crawler.get_results()
        
        assert results['start_url'] == 'https://example.com'
        assert results['total_pages_crawled'] == 1
        assert len(results['pages']) == 1
        assert len(results['visited_urls']) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
