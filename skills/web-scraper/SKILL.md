---
name: web-scraper
description: Web scraping toolkit for content extraction and analysis. Use this when users need to crawl web pages, extract structured data, scrape multiple pages, or analyze web content. Supports both Python (requests/BeautifulSoup) and Node.js (Puppeteer/Playwright) implementations.
license: Apache-2.0
---

# Web Scraper

A comprehensive web scraping skill for extracting and analyzing content from websites. This skill provides ready-to-use scripts and patterns for common scraping tasks.

## Core Principles

- **Respect robots.txt** - Always check and honor site restrictions
- **Rate limiting** - Never overload servers with rapid requests
- **User-Agent identification** - Identify your bot clearly
- **Error handling** - Handle network errors, timeouts, and parsing failures gracefully
- **Legal compliance** - Only scrape publicly accessible data, respect Terms of Service

## Quick Start Templates

Choose the appropriate template based on your needs:

- **Static HTML pages** - Use Python requests + BeautifulSoup or Node.js cheerio
- **Dynamic/JavaScript pages** - Use Python Selenium or Node.js Puppeteer/Playwright
- **Large-scale crawling** - Use Python Scrapy framework

## Python Templates

### Basic Static Page Scraper

```python
import requests
from bs4 import BeautifulSoup
import time
import csv
from typing import List, Dict
from urllib.parse import urljoin, urlparse

class WebScraper:
    """Basic web scraper with rate limiting and error handling."""

    def __init__(self, base_url: str, min_delay: float = 1.0):
        self.base_url = base_url
        self.min_delay = min_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebScraper/1.0; +https://example.com/bot)'
        })

    def fetch(self, url: str, retries: int = 3) -> str | None:
        """Fetch page content with retry logic."""
        full_url = urljoin(self.base_url, url)
        for attempt in range(retries):
            try:
                response = self.session.get(full_url, timeout=10)
                response.raise_for_status()
                time.sleep(self.min_delay)
                return response.text
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    return None
                time.sleep(2 ** attempt)
        return None

    def parse_content(self, html: str) -> Dict[str, any]:
        """Extract structured content from HTML."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()

        return {
            'title': soup.find('h1') or soup.find('title'),
            'content': soup.find('main') or soup.find('article') or soup.body,
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'images': [img.get('src') for img in soup.find_all('img', src=True)],
            'metadata': {
                'description': soup.find('meta', attrs={'name': 'description'}),
                'keywords': soup.find('meta', attrs={'name': 'keywords'}),
            }
        }

    def scrape_page(self, url: str) -> Dict[str, any]:
        """Scrape a single page and return structured data."""
        html = self.fetch(url)
        if not html:
            return None

        data = self.parse_content(html)
        data['url'] = urljoin(self.base_url, url)
        return data


# Usage example
if __name__ == "__main__":
    scraper = WebScraper("https://example.com", min_delay=1.0)
    result = scraper.scrape_page("/")
    print(result)
```

### Dynamic Page Scraper (Selenium)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class DynamicScraper:
    """Scraper for JavaScript-heavy pages using Selenium."""

    def __init__(self, headless: bool = True):
        options = Options()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        self.driver = webdriver.Chrome(options=options)
        self.wait = None

    def fetch(self, url: str, wait_selector: str = None, wait_time: int = 10):
        """Fetch dynamic page and wait for element."""
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, wait_time)

        if wait_selector:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
            )

        # Wait for potential lazy-loaded content
        time.sleep(2)

        return self.driver.page_source

    def scroll_and_load(self, scrolls: int = 3):
        """Scroll down to trigger lazy-loaded content."""
        for _ in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

    def extract_content(self) -> dict:
        """Extract structured content from loaded page."""
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        return {
            'title': soup.find('h1'),
            'content': soup.find_all(['p', 'h1', 'h2', 'h3', 'article']),
            'links': soup.find_all('a', href=True),
            'images': soup.find_all('img', src=True),
            'url': self.driver.current_url
        }

    def close(self):
        """Clean up resources."""
        self.driver.quit()


# Usage example for infinite scroll pages
if __name__ == "__main__":
    scraper = DynamicScraper(headless=True)
    try:
        scraper.fetch("https://example.com")
        scraper.scroll_and_load(scrolls=5)
        content = scraper.extract_content()
        print(content)
    finally:
        scraper.close()
```

### Content Analyzer

```python
import re
from collections import Counter
from typing import List, Dict
import html

class ContentAnalyzer:
    """Analyze scraped web content."""

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        # Decode HTML entities
        text = html.unescape(text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_keywords(self, text: str, min_length: int = 3, top_n: int = 20) -> List[tuple]:
        """Extract most common words/phrases from text."""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        # Filter common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
                      'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'with', 'this',
                      'that', 'from', 'they', 'will', 'would', 'there', 'their', 'what', 'about'}
        words = [w for w in words if w not in stop_words]
        return Counter(words).most_common(top_n)

    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)

    def extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        patterns = [
            r'\b\d{3}-\d{3}-\d{4}\b',
            r'\b\(\d{3}\)\s*\d{3}-\d{4}\b',
            r'\b\d{3}\.\d{3}\.\d{4}\b'
        ]
        results = []
        for pattern in patterns:
            results.extend(re.findall(pattern, text))
        return results

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(pattern, text)

    def summarize_content(self, soup_content) -> Dict:
        """Create a summary of parsed BeautifulSoup content."""
        texts = []
        if hasattr(soup_content, '__iter__'):
            for elem in soup_content:
                texts.append(elem.get_text())
        else:
            texts.append(soup_content.get_text())

        full_text = ' '.join(texts)
        clean = self.clean_text(full_text)

        return {
            'word_count': len(clean.split()),
            'char_count': len(clean),
            'keywords': self.extract_keywords(clean),
            'emails': self.extract_emails(clean),
            'phones': self.extract_phone_numbers(clean),
            'urls': self.extract_urls(clean),
            'preview': clean[:500] + '...' if len(clean) > 500 else clean
        }

    def analyze_multiple_pages(self, pages: List[Dict]) -> Dict:
        """Analyze multiple scraped pages and aggregate results."""
        all_keywords = Counter()
        all_emails = set()
        all_phones = set()

        for page in pages:
            summary = self.summarize_content(page.get('content', ''))
            for keyword, count in summary.get('keywords', []):
                all_keywords[keyword] += count
            all_emails.update(summary.get('emails', []))
            all_phones.update(summary.get('phones', []))

        return {
            'total_pages': len(pages),
            'top_keywords': all_keywords.most_common(50),
            'unique_emails': list(all_emails),
            'unique_phones': list(all_phones)
        }
```

### Multi-Page Crawler

```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

class AsyncCrawler:
    """Asynchronous web crawler for multiple pages."""

    def __init__(self, base_url: str, max_concurrent: int = 5):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.queue = asyncio.Queue()
        self.max_concurrent = max_concurrent

    def is_valid_url(self, url: str) -> bool:
        """Check if URL should be crawled."""
        parsed = urlparse(url)
        return (
            parsed.netloc == self.domain and
            url not in self.visited and
            parsed.scheme in ('http', 'https')
        )

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str | None:
        """Fetch a single page asynchronously."""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            full_url = urljoin(base_url, a['href'])
            if self.is_valid_url(full_url):
                links.append(full_url)
        return links

    async def crawl_worker(self, session: aiohttp.ClientSession, results: list):
        """Worker that processes URLs from the queue."""
        while True:
            url = await self.queue.get()
            if url is None:  # Sentinel value to stop
                self.queue.task_done()
                break

            html = await self.fetch(session, url)
            if html:
                self.visited.add(url)
                results.append({'url': url, 'html': html})

                # Add new links to queue
                for link in self.extract_links(html, url):
                    if link not in self.visited:
                        await self.queue.put(link)

            self.queue.task_done()

    async def crawl(self, start_url: str, max_pages: int = 50) -> List[Dict]:
        """Crawl website starting from given URL."""
        await self.queue.put(start_url)

        results = []
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)

        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [
                asyncio.create_task(self.crawl_worker(session, results))
                for _ in range(self.max_concurrent)
            ]

            # Wait for queue to empty or max_pages reached
            while len(results) < max_pages and not self.queue.empty():
                await asyncio.sleep(0.1)

            # Stop workers
            for _ in range(self.max_concurrent):
                await self.queue.put(None)
            await asyncio.gather(*tasks)

        return results[:max_pages]


# Usage
async def main():
    crawler = AsyncCrawler("https://example.com", max_concurrent=3)
    results = await crawler.crawl("https://example.com", max_pages=20)
    print(f"Crawled {len(results)} pages")

if __name__ == "__main__":
    asyncio.run(main())
```

### Results Exporter

```python
import json
import csv
from datetime import datetime
from pathlib import Path

class ResultsExporter:
    """Export scraping results to various formats."""

    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def to_json(self, data: List[Dict], filename: str = None) -> str:
        """Export data to JSON file."""
        if filename is None:
            filename = f"scrape_{self.timestamp}.json"
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return str(filepath)

    def to_csv(self, data: List[Dict], filename: str = None) -> str:
        """Export data to CSV file."""
        if filename is None:
            filename = f"scrape_{self.timestamp}.csv"
        filepath = self.output_dir / filename

        if not data:
            return None

        # Flatten nested dicts for CSV
        flat_data = []
        for item in data:
            flat = {}
            for key, value in item.items():
                if isinstance(value, (list, dict)):
                    flat[key] = json.dumps(value, ensure_ascii=False)
                elif value is None:
                    flat[key] = ""
                else:
                    flat[key] = str(value)
            flat_data.append(flat)

        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=flat_data[0].keys())
            writer.writeheader()
            writer.writerows(flat_data)

        return str(filepath)

    def to_markdown(self, data: List[Dict], filename: str = None) -> str:
        """Export data to Markdown report."""
        if filename is None:
            filename = f"report_{self.timestamp}.md"
        filepath = self.output_dir / filename

        md_content = f"# Web Scraping Report\n\n"
        md_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"Total pages scraped: {len(data)}\n\n---\n\n"

        for i, item in enumerate(data, 1):
            md_content += f"## Page {i}\n\n"
            if 'url' in item:
                md_content += f"**URL:** {item['url']}\n\n"
            if 'title' in item and item['title']:
                title = item['title'].get_text() if hasattr(item['title'], 'get_text') else str(item['title'])
                md_content += f"**Title:** {title}\n\n"
            md_content += f"**Content Preview:**\n\n"
            md_content += "```\n"
            content_text = item.get('content', '')[:500]
            if hasattr(content_text, 'get_text'):
                content_text = content_text.get_text()[:500]
            md_content += str(content_text) + "\n"
            md_content += "```\n\n---\n\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return str(filepath)
```

## Node.js Templates

### Basic Scraper (axios + cheerio)

```javascript
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const path = require('path');

class WebScraper {
    constructor(baseUrl, options = {}) {
        this.baseUrl = baseUrl;
        this.minDelay = options.minDelay || 1000;
        this.retries = options.retries || 3;
        this.client = axios.create({
            headers: {
                'User-Agent': 'Mozilla/5.0 (compatible; WebScraper/1.0)'
            },
            timeout: options.timeout || 10000
        });
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async fetch(url, retries = this.retries) {
        const fullUrl = new URL(url, this.baseUrl).href;

        for (let attempt = 1; attempt <= retries; attempt++) {
            try {
                const response = await this.client.get(fullUrl);
                await this.sleep(this.minDelay);
                return response.data;
            } catch (error) {
                console.log(`Attempt ${attempt} failed: ${error.message}`);
                if (attempt === retries) return null;
                await this.sleep(1000 * attempt);
            }
        }
        return null;
    }

    parseContent(html) {
        const $ = cheerio.load(html);

        // Remove script and style elements
        $('script, style, nav, footer').remove();

        return {
            title: $('h1').text() || $('title').text(),
            content: $('main, article, body').text().trim(),
            links: $('a[href]').map((i, el) => $(el).attr('href')).get(),
            images: $('img[src]').map((i, el) => $(el).attr('src')).get(),
            metadata: {
                description: $('meta[name="description"]').attr('content'),
                keywords: $('meta[name="keywords"]').attr('content'),
                ogTitle: $('meta[property="og:title"]').attr('content'),
                ogImage: $('meta[property="og:image"]').attr('content')
            }
        };
    }

    async scrapePage(url) {
        const html = await this.fetch(url);
        if (!html) return null;

        const data = this.parseContent(html);
        data.url = new URL(url, this.baseUrl).href;
        return data;
    }

    async scrapeMultiplePages(urls) {
        const results = [];
        for (const url of urls) {
            const data = await this.scrapePage(url);
            if (data) results.push(data);
        }
        return results;
    }
}

// Usage
(async () => {
    const scraper = new WebScraper('https://example.com', { minDelay: 1000 });
    const result = await scraper.scrapePage('/');
    console.log(result);
})();
```

### Dynamic Scraper (Puppeteer)

```javascript
const puppeteer = require('puppeteer');
const fs = require('fs').promises;

class DynamicScraper {
    constructor(options = {}) {
        this.headless = options.headless !== false;
        this.timeout = options.timeout || 30000;
    }

    async init() {
        this.browser = await puppeteer.launch({
            headless: this.headless,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
    }

    async fetch(url, options = {}) {
        if (!this.browser) await this.init();

        const page = await this.browser.newPage();

        // Set viewport
        await page.setViewport(options.viewport || { width: 1920, height: 1080 });

        // Navigate to URL
        await page.goto(url, {
            waitUntil: options.waitUntil || 'networkidle2',
            timeout: this.timeout
        });

        // Wait for specific selector if provided
        if (options.waitForSelector) {
            await page.waitForSelector(options.waitForSelector, { timeout: 10000 });
        }

        // Handle infinite scroll
        if (options.infiniteScroll) {
            await this.handleInfiniteScroll(page, options.scrollCount || 3);
        }

        const html = await page.content();
        await page.close();

        return html;
    }

    async handleInfiniteScroll(page, scrollCount = 3) {
        for (let i = 0; i < scrollCount; i++) {
            await page.evaluate(() => {
                window.scrollTo(0, document.body.scrollHeight);
            });
            await this.sleep(1000);
        }
    }

    async extractContent(page) {
        return await page.evaluate(() => {
            return {
                title: document.querySelector('h1')?.textContent ||
                       document.title,
                content: Array.from(document.querySelectorAll('main p, article p, body p'))
                    .map(p => p.textContent).join('\n'),
                links: Array.from(document.querySelectorAll('a[href]'))
                    .map(a => a.href),
                images: Array.from(document.querySelectorAll('img[src]'))
                    .map(img => img.src),
                url: window.location.href
            };
        });
    }

    async scrapeWithActions(url, actions = []) {
        if (!this.browser) await this.init();
        const page = await this.browser.newPage();

        await page.goto(url, { waitUntil: 'networkidle2' });

        // Execute custom actions
        for (const action of actions) {
            switch (action.type) {
                case 'click':
                    await page.click(action.selector);
                    break;
                case 'type':
                    await page.type(action.selector, action.text);
                    break;
                case 'waitFor':
                    await page.waitForSelector(action.selector);
                    break;
                case 'scroll':
                    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
                    break;
            }
            await this.sleep(500);
        }

        const content = await this.extractContent(page);
        await page.close();

        return content;
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async close() {
        if (this.browser) {
            await this.browser.close();
        }
    }
}

// Usage
(async () => {
    const scraper = new DynamicScraper({ headless: true });
    try {
        await scraper.init();

        // Basic fetch
        const html = await scraper.fetch('https://example.com', {
            infiniteScroll: true,
            scrollCount: 5
        });

        // Or with actions
        const content = await scraper.scrapeWithActions('https://example.com', [
            { type: 'waitFor', selector: '.content' },
            { type: 'click', selector: '.load-more' },
            { type: 'scroll' }
        ]);

        console.log(content);
    } finally {
        await scraper.close();
    }
})();
```

### Content Analyzer (Node.js)

```javascript
const natural = require('natural');

class ContentAnalyzer {
    constructor() {
        this.stopWords = new Set([
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'with',
            'this', 'that', 'from', 'they', 'will', 'would', 'there', 'their',
            'what', 'about', 'which', 'their', 'said', 'each', 'does', 'did'
        ]);
    }

    cleanText(text) {
        if (!text) return '';
        return text
            .replace(/\s+/g, ' ')
            .replace(/[\r\n\t]/g, ' ')
            .trim();
    }

    extractKeywords(text, topN = 20) {
        const words = text.toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length >= 3 && !this.stopWords.has(word));

        const frequency = {};
        words.forEach(word => {
            frequency[word] = (frequency[word] || 0) + 1;
        });

        return Object.entries(frequency)
            .sort((a, b) => b[1] - a[1])
            .slice(0, topN);
    }

    extractEmails(text) {
        const pattern = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;
        return text.match(pattern) || [];
    }

    extractPhoneNumbers(text) {
        const patterns = [
            /\b\d{3}-\d{3}-\d{4}\b/g,
            /\b\(\d{3}\)\s*\d{3}-\d{4}\b/g,
            /\b\d{3}\.\d{3}\.\d{4}\b/g
        ];

        const results = new Set();
        patterns.forEach(pattern => {
            const matches = text.match(pattern) || [];
            matches.forEach(m => results.add(m));
        });

        return Array.from(results);
    }

    extractUrls(text) {
        const pattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/g;
        return text.match(pattern) || [];
    }

    summarizeContent(content) {
        const clean = this.cleanText(content);

        return {
            wordCount: clean.split(/\s+/).length,
            charCount: clean.length,
            keywords: this.extractKeywords(clean),
            emails: this.extractEmails(clean),
            phones: this.extractPhoneNumbers(clean),
            urls: this.extractUrls(clean),
            preview: clean.length > 500 ? clean.slice(0, 500) + '...' : clean
        };
    }

    analyzeMultiplePages(pages) {
        const allKeywords = {};
        const allEmails = new Set();
        const allPhones = new Set();

        pages.forEach(page => {
            const summary = this.summarizeContent(page.content || '');

            summary.keywords.forEach(([keyword, count]) => {
                allKeywords[keyword] = (allKeywords[keyword] || 0) + count;
            });

            summary.emails.forEach(e => allEmails.add(e));
            summary.phones.forEach(p => allPhones.add(p));
        });

        return {
            totalPages: pages.length,
            topKeywords: Object.entries(allKeywords)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 50),
            uniqueEmails: Array.from(allEmails),
            uniquePhones: Array.from(allPhones)
        };
    }
}

// Usage
const analyzer = new ContentAnalyzer();
const summary = analyzer.summarizeContent(pageContent);
console.log(summary);
```

### Results Exporter (Node.js)

```javascript
const fs = require('fs').promises;
const path = require('path');

class ResultsExporter {
    constructor(outputDir = 'results') {
        this.outputDir = outputDir;
        this.timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    }

    async ensureDir() {
        try {
            await fs.mkdir(this.outputDir, { recursive: true });
        } catch (err) {
            // Directory already exists
        }
    }

    async toJSON(data, filename) {
        await this.ensureDir();
        const filepath = path.join(this.outputDir, filename || `scrape_${this.timestamp}.json`);
        await fs.writeFile(filepath, JSON.stringify(data, null, 2), 'utf-8');
        return filepath;
    }

    async toCSV(data, filename) {
        await this.ensureDir();
        const filepath = path.join(this.outputDir, filename || `scrape_${this.timestamp}.csv`);

        if (!data.length) return null;

        // Flatten objects
        const flatten = (obj) => {
            const flat = {};
            for (const [key, value] of Object.entries(obj)) {
                if (value && typeof value === 'object') {
                    flat[key] = JSON.stringify(value);
                } else if (value === null || value === undefined) {
                    flat[key] = '';
                } else {
                    flat[key] = String(value);
                }
            }
            return flat;
        };

        const headers = Object.keys(flatten(data[0]));
        const csvContent = [
            headers.join(','),
            ...data.map(row => {
                const flat = flatten(row);
                return headers.map(h => {
                    const val = flat[h] || '';
                    return val.includes(',') ? `"${val}"` : val;
                }).join(',');
            })
        ].join('\n');

        await fs.writeFile(filepath, csvContent, 'utf-8');
        return filepath;
    }

    async toMarkdown(data, filename) {
        await this.ensureDir();
        const filepath = path.join(this.outputDir, filename || `report_${this.timestamp}.md`);

        let md = `# Web Scraping Report\n\n`;
        md += `Generated: ${new Date().toLocaleString()}\n\n`;
        md += `Total pages scraped: ${data.length}\n\n---\n\n`;

        data.forEach((item, i) => {
            md += `## Page ${i + 1}\n\n`;
            if (item.url) md += `**URL:** ${item.url}\n\n`;
            if (item.title) md += `**Title:** ${item.title}\n\n`;
            md += `**Content Preview:**\n\n\`\`\`\n`;
            const preview = String(item.content || '').slice(0, 500);
            md += preview + '\n```\n\n---\n\n';
        });

        await fs.writeFile(filepath, md, 'utf-8');
        return filepath;
    }
}
```

## Best Practices

### Request Throttling

```python
# Python: Use time.sleep() between requests
import time
import random

def respectful_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))
```

```javascript
// Node.js: Use promises with delays
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function respectfulDelay(min = 1000, max = 3000) {
    const delay = Math.random() * (max - min) + min;
    await sleep(delay);
}
```

### Robots.txt Checking

```python
# Python: Check robots.txt
from urllib.robotparser import RobotFileParser

def can_fetch(url, user_agent='*'):
    rp = RobotFileParser()
    rp.set_url(url + '/robots.txt')
    rp.read()
    return rp.can_fetch(user_agent, url)
```

```javascript
// Node.js: Use robots-txt-parser
const robotsParser = require('robots-txt-parser');

async function canFetch(url) {
    const robots = await robotsParser(url);
    return robots.isAllowed(url);
}
```

### Error Handling Pattern

```python
# Python: Comprehensive error handling
def safe_scrape(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return parse_html(response.text)
    except requests.Timeout:
        log_error(f"Timeout: {url}")
    except requests.ConnectionError:
        log_error(f"Connection failed: {url}")
    except requests.HTTPError as e:
        log_error(f"HTTP {e.response.status_code}: {url}")
    except Exception as e:
        log_error(f"Unexpected error: {e}")
    return None
```

## Common Use Cases

### News Article Scraper

```python
def scrape_article(url):
    scraper = WebScraper(url)
    data = scraper.scrape_page(url)

    return {
        'headline': data['title'],
        'body': data['content'],
        'author': data.get('metadata', {}).get('author'),
        'publish_date': data.get('metadata', {}).get('published'),
        'tags': extract_keywords(data['content'])
    }
```

### Product Info Scraper

```python
def scrape_product(url):
    scraper = WebScraper(url)
    data = scraper.scrape_page(url)

    return {
        'name': extract_product_name(data),
        'price': extract_price(data),
        'description': extract_description(data),
        'images': data['images'],
        'availability': check_availability(data)
    }
```

### Contact Info Extractor

```python
def extract_contacts(url):
    scraper = WebScraper(url)
    analyzer = ContentAnalyzer()

    data = scraper.scrape_page(url)
    content = data['content'].get_text()

    return {
        'emails': analyzer.extract_emails(content),
        'phones': analyzer.extract_phone_numbers(content),
        'social_links': extract_social_links(data['links'])
    }
```

## Dependencies

### Python

```bash
pip install requests beautifulsoup4 selenium aiohttp
# For large scale:
pip install scrapy
```

### Node.js

```bash
npm install axios cheerio puppeteer
npm install natural  # for text analysis
npm install robots-txt-parser  # for robots.txt checking
```

## Output Formats

Results can be exported to:
- **JSON** - Structured data for further processing
- **CSV** - Spreadsheet compatible format
- **Markdown** - Human-readable reports
- **Database** - Direct insertion into SQLite/PostgreSQL

Choose format based on your use case.
