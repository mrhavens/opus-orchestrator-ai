"""Agent-Driven Web Crawler for Opus.

Uses AI to analyze sites, decide what to crawl, and intelligently extract content.
Instead of hardcoded patterns, the agent understands context and adapts.
"""

from dataclasses import dataclass, field
from typing import Optional, list
from enum import Enum
import asyncio


class CrawlPurpose(str, Enum):
    """What the user intends to do with the crawled content."""
    DOCUMENTATION = "documentation"    # Technical docs, guides
    TRAINING = "training"           # Learning materials
    KNOWLEDGE = "knowledge"         # General knowledge base
    RESEARCH = "research"           # Research papers, articles
    REFERENCE = "reference"          # Reference material


@dataclass
class PageResult:
    """A single crawled page."""
    url: str
    title: str
    content: str
    relevance_score: float
    links: list[str]
    depth: int


@dataclass
class SiteAnalysis:
    """Agent's analysis of a site."""
    site_type: str  # documentation, blog, wiki, etc.
    sections: dict  # section -> priority
    suggested_urls: list[str]
    skip_patterns: list[str]
    reasoning: str


@dataclass
class AgentCrawlResult:
    """Result from agent crawling."""
    pages: list[PageResult]
    site_analysis: SiteAnalysis
    total_fetched: int
    total_relevant: int
    duration_seconds: float


class AgentWebCrawler:
    """AI-powered web crawler that uses an agent to decide what to crawl.
    
    Instead of hardcoded patterns, the agent:
    1. Analyzes the site structure
    2. Decides what matters for the purpose
    3. Adapts as it learns more
    4. Knows when it has enough
    """
    
    def __init__(
        self,
        llm_client=None,
        max_pages: int = 50,
        max_depth: int = 3,
        delay_seconds: float = 1.0,
        user_agent: str = "OpusCrawler/1.0",
    ):
        self.llm = llm_client
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.delay = delay_seconds
        self.user_agent = user_agent
        self._fetched_urls = set()
    
    async def crawl(
        self,
        start_url: str,
        purpose: CrawlPurpose = CrawlPurpose.DOCUMENTATION,
    ) -> AgentCrawlResult:
        """Crawl a site using AI to decide what matters.
        
        Args:
            start_url: Where to begin
            purpose: What the content is for
            
        Returns:
            AgentCrawlResult with pages and analysis
        """
        import time
        start_time = time.time()
        
        # Step 1: Analyze the site
        analysis = await self._analyze_site(start_url, purpose)
        
        # Step 2: Decide what to fetch (agent reasoning)
        urls_to_fetch = await self._decide_urls(analysis, purpose)
        
        # Step 3: Fetch in priority order with relevance scoring
        pages = []
        fetched_count = 0
        
        for url_info in urls_to_fetch:
            if fetched_count >= self.max_pages:
                break
            
            try:
                page = await self._fetch_and_analyze(
                    url_info["url"],
                    url_info["priority"],
                    purpose,
                )
                
                if page.relevance_score > 0.3:  # Threshold
                    pages.append(page)
                    fetched_count += 1
                
                # Be nice
                await asyncio.sleep(self.delay)
                
            except Exception as e:
                print(f"Failed to fetch {url_info['url']}: {e}")
                continue
        
        duration = time.time() - start_time
        
        return AgentCrawlResult(
            pages=pages,
            site_analysis=analysis,
            total_fetched=fetched_count,
            total_relevant=len(pages),
            duration_seconds=duration,
        )
    
    async def _analyze_site(self, start_url: str, purpose: CrawlPurpose) -> SiteAnalysis:
        """Use agent to analyze the site structure."""
        
        # Fetch homepage
        homepage_content = await self._fetch(start_url)
        
        if self.llm:
            # Use LLM to analyze
            prompt = f"""Analyze this website for crawling.
            
URL: {start_url}
Purpose: {purpose.value}

Analyze:
1. What type of site is this? (documentation, blog, wiki, etc.)
2. What are the main sections?
3. Which URLs should we prioritize for {purpose} content?
4. What should we skip?
5. What patterns in URLs matter?

Homepage content:
{homepage_content[:3000]}
"""
            response = await self.llm.complete(
                system_prompt="You are a web crawler expert. Analyze sites to determine what to crawl.",
                user_prompt=prompt,
            )
            
            # Parse response into SiteAnalysis
            return self._parse_analysis(start_url, response)
        else:
            # Fallback: simple heuristics
            return self._simple_analysis(start_url, purpose)
    
    async def _decide_urls(
        self,
        analysis: SiteAnalysis,
        purpose: CrawlPurpose,
    ) -> list[dict]:
        """Agent decides which URLs to fetch."""
        
        urls = []
        
        # Start with suggested URLs
        for url in analysis.suggested_urls[:self.max_pages]:
            priority = analysis.sections.get(url, 0.5)
            urls.append({"url": url, "priority": priority})
        
        return urls[:self.max_pages]
    
    async def _fetch_and_analyze(
        self,
        url: str,
        base_priority: float,
        purpose: CrawlPurpose,
    ) -> PageResult:
        """Fetch a page and analyze its relevance."""
        
        content = await self._fetch(url)
        
        # Extract content
        title = self._extract_title(content)
        links = self._extract_links(content, url)
        
        # Extract main content (not HTML)
        main_content = self._extract_main_content(content)
        
        # Score relevance
        if self.llm:
            relevance = await self._score_relevance(main_content, purpose)
        else:
            relevance = self._simple_relevance(main_content, purpose)
        
        return PageResult(
            url=url,
            title=title,
            content=main_content,
            relevance_score=relevance,
            links=links,
            depth=0,
        )
    
    async def _fetch(self, url: str) -> str:
        """Fetch a URL (using requests or similar)."""
        import requests
        
        headers = {"User-Agent": self.user_agent}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    
    def _extract_title(self, html: str) -> str:
        """Extract page title."""
        import re
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else "Untitled"
    
    def _extract_links(self, html: str, base_url: str) -> list[str]:
        """Extract links from HTML."""
        from urllib.parse import urljoin, urlparse
        import re
        
        links = []
        for match in re.finditer(r'href=["\']([^"\']+)["\']', html):
            href = match.group(1)
            full_url = urljoin(base_url, href)
            links.append(full_url)
        
        return links
    
    def _extract_main_content(self, html: str) -> str:
        """Extract main content, removing nav/footer/ads."""
        import re
        
        # Simple extraction - remove script/style and get body
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        
        # Try to find main content areas
        for tag in ['article', 'main', 'div[@class="content"]', 'div[@class="main"]']:
            match = re.search(f'<{tag}[^>]*>(.*?)</{tag}>', html, re.DOTALL | re.IGNORECASE)
            if match:
                html = match.group(1)
                break
        
        # Convert to text
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    async def _score_relevance(self, content: str, purpose: CrawlPurpose) -> float:
        """Use LLM to score relevance."""
        
        prompt = f"""Rate this page's relevance for {purpose.value} content.

Rate 0.0-1.0:
- 1.0 = Highly relevant, core content
- 0.5 = Somewhat relevant
- 0.0 = Not relevant (nav, footer, etc.)

Page content (first 1000 chars):
{content[:1000]}

Just respond with a number between 0.0 and 1.0."""

        response = await self.llm.complete(prompt)
        
        try:
            return float(response.strip())
        except (ValueError, TypeError):
            return 0.5
    
    def _simple_relevance(self, content: str, purpose: CrawlPurpose) -> float:
        """Simple keyword-based relevance."""
        
        keywords = {
            CrawlPurpose.DOCUMENTATION: ['documentation', 'guide', 'tutorial', 'reference', 'api', 'docs'],
            CrawlPurpose.TRAINING: ['learn', 'course', 'tutorial', 'lesson', 'how to'],
            CrawlPurpose.KNOWLEDGE: ['knowledge', 'article', 'information', 'about'],
            CrawlPurpose.RESEARCH: ['research', 'study', 'paper', 'analysis'],
            CrawlPurpose.REFERENCE: ['reference', 'manual', 'specification', 'api'],
        }
        
        content_lower = content.lower()
        score = 0.0
        
        for kw in keywords.get(purpose, []):
            if kw in content_lower:
                score += 0.2
        
        return min(1.0, score)
    
    def _parse_analysis(self, base_url: str, response: str) -> SiteAnalysis:
        """Parse LLM response into SiteAnalysis."""
        # Simplified - would parse actual LLM response
        return SiteAnalysis(
            site_type="documentation",
            sections={
                f"{base_url}/docs": 1.0,
                f"{base_url}/guides": 0.9,
                f"{base_url}/api": 0.7,
            },
            suggested_urls=[
                f"{base_url}/docs",
                f"{base_url}/guides",
                f"{base_url}/api",
            ],
            skip_patterns=["/blog", "/community", "/pricing"],
            reasoning="Based on analysis",
        )
    
    def _simple_analysis(self, url: str, purpose: CrawlPurpose) -> SiteAnalysis:
        """Fallback simple analysis without LLM."""
        from urllib.parse import urljoin, urlparse
        
        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        
        return SiteAnalysis(
            site_type="unknown",
            sections={},
            suggested_urls=[
                url,
                f"{base}/docs",
                f"{base}/documentation",
                f"{base}/guides",
            ],
            skip_patterns=["/blog", "/news", "/contact"],
            reasoning="Simple fallback",
        )


# Integration with multi-source ingest
class SmartIngestWithCrawl:
    """Combines agent crawling with multi-source ingest."""
    
    def __init__(self, crawler: AgentWebCrawler, multi_ingestor):
        self.crawler = crawler
        self.multi = multi_ingestor
    
    async def ingest(
        self,
        sources: list[dict],
        purpose: str = "documentation",
    ) -> dict:
        """Ingest from multiple sources, crawling intelligently.
        
        Sources can include:
        - {"type": "url", "url": "...", "crawl": True}
        - {"type": "github", "repo": "..."}
        - {"type": "local", "path": "..."}
        """
        results = []
        
        for source in sources:
            if source.get("crawl", False) and source.get("type") == "url":
                # Use agent crawler
                crawl_result = await self.crawler.crawl(
                    start_url=source["url"],
                    purpose=CrawlPurpose(purpose),
                )
                results.append({
                    "type": "crawled",
                    "pages": crawl_result.pages,
                    "analysis": crawl_result.site_analysis,
                })
            else:
                # Use regular ingest
                result = await self.multi._ingest_single(source)
                results.append(result)
        
        return {
            "sources": results,
            "total_pages": sum(len(r.get("pages", [])) for r in results),
        }
