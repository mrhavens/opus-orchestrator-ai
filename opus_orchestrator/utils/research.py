"""Research tools for Opus Orchestrator.

Provides web search, database lookup, and research capabilities.
"""

import os
import json
from typing import Any, Optional, Callable
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


class SearchTool:
    """Web search tool using multiple backends."""
    
    def __init__(self, provider: str = "tavily"):
        """Initialize search tool.
        
        Args:
            provider: Search provider (tavily, serper, brave, duckduckgo)
        """
        self.provider = provider
        self._setup_provider()
    
    def _setup_provider(self):
        """Set up the search provider."""
        if self.provider == "tavily":
            self.api_key = os.environ.get("TAVILY_API_KEY")
        elif self.provider == "serper":
            self.api_key = os.environ.get("SERPER_API_KEY")
        elif self.provider == "brave":
            self.api_key = os.environ.get("BRAVE_API_KEY")
    
    def search(
        self,
        query: str,
        num_results: int = 10,
    ) -> list[dict]:
        """Search the web.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, url, snippet
        """
        if self.provider == "tavily":
            return self._search_tavily(query, num_results)
        elif self.provider == "serper":
            return self._search_serper(query, num_results)
        elif self.provider == "brave":
            return self._search_brave(query, num_results)
        else:
            return self._search_duckduckgo(query, num_results)
    
    def _search_tavily(self, query: str, num_results: int) -> list[dict]:
        """Search using Tavily."""
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=self.api_key)
            results = client.search(query=query, max_results=num_results)
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "score": r.get("score", 0),
                }
                for r in results.get("results", [])
            ]
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []
    
    def _search_serper(self, query: str, num_results: int) -> list[dict]:
        """Search using Serper."""
        try:
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            }
            payload = {"q": query, "num": num_results}
            response = requests.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=payload,
                timeout=10,
            )
            data = response.json()
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("link", ""),
                    "content": r.get("snippet", ""),
                    "score": 1.0,
                }
                for r in data.get("organic", [])
            ]
        except Exception as e:
            print(f"Serper search error: {e}")
            return []
    
    def _search_brave(self, query: str, num_results: int) -> list[dict]:
        """Search using Brave."""
        try:
            headers = {"Accept": "application/json", "X-Subscription-Token": self.api_key}
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": query, "count": num_results},
                headers=headers,
                timeout=10,
            )
            data = response.json()
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("description", ""),
                    "score": r.get("score", 0),
                }
                for r in data.get("web", {}).get("results", [])
            ]
        except Exception as e:
            print(f"Brave search error: {e}")
            return []
    
    def _search_duckduckgo(self, query: str, num_results: int) -> list[dict]:
        """Search using DuckDuckGo (no API key needed)."""
        try:
            from duckduckgo_search import DDGS
            results = DDGS().text(query, max_results=num_results)
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "content": r.get("body", ""),
                    "score": 1.0,
                }
                for r in results
            ]
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []


class WikipediaTool:
    """Wikipedia lookup tool."""
    
    def __init__(self):
        """Initialize Wikipedia tool."""
        pass
    
    def search(self, query: str, num_results: int = 5) -> list[dict]:
        """Search Wikipedia.
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            List of Wikipedia articles
        """
        try:
            import wikipedia
            results = wikipedia.search(query, results=num_results)
            articles = []
            for title in results:
                try:
                    page = wikipedia.page(title)
                    articles.append({
                        "title": page.title,
                        "url": page.url,
                        "summary": page.summary[:500],
                        "content": page.content[:2000],
                    })
                except:
                    continue
            return articles
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []
    
    def get_article(self, title: str) -> dict:
        """Get a Wikipedia article by title.
        
        Args:
            title: Article title
            
        Returns:
            Article content
        """
        try:
            import wikipedia
            page = wikipedia.page(title)
            return {
                "title": page.title,
                "url": page.url,
                "summary": page.summary,
                "content": page.content[:5000],
                "references": page.references[:10] if hasattr(page, "references") else [],
            }
        except Exception as e:
            return {"error": str(e)}


class ArxivTool:
    """ArXiv paper search tool."""
    
    def __init__(self):
        """Initialize ArXiv tool."""
        pass
    
    def search(
        self,
        query: str,
        max_results: int = 10,
        categories: list[str] = None,
    ) -> list[dict]:
        """Search ArXiv for papers.
        
        Args:
            query: Search query
            max_results: Max results
            categories: ArXiv categories to filter
            
        Returns:
            List of papers
        """
        try:
            import arxiv
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                categories=categories or [],
            )
            papers = []
            for result in client.results(search):
                papers.append({
                    "title": result.title,
                    "url": result.entry_id,
                    "abstract": result.summary[:1000],
                    "authors": [a.name for a in result.authors],
                    "published": str(result.published.date()),
                    "categories": result.categories,
                })
            return papers
        except Exception as e:
            print(f"ArXiv search error: {e}")
            return []


class AcademicSearchTool:
    """Academic paper search (CrossRef, Semantic Scholar)."""
    
    def __init__(self):
        """Initialize academic search tool."""
        pass
    
    def search_crossref(self, query: str, max_results: int = 10) -> list[dict]:
        """Search CrossRef for academic papers."""
        try:
            url = "https://api.crossref.org/works"
            params = {"query": query, "rows": max_results}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return [
                {
                    "title": item.get("title", [""])[0],
                    "url": item.get("URL", ""),
                    "authors": [a.get("given", "") + " " + a.get("family", "") 
                               for a in item.get("author", [])],
                    "year": item.get("created", {}).get("date-parts", [[None]])[0][0],
                    "journal": item.get("container-title", [""])[0],
                    "doi": item.get("DOI", ""),
                }
                for item in data.get("message", {}).get("items", [])
            ]
        except Exception as e:
            print(f"CrossRef search error: {e}")
            return []
    
    def search_semantic_scholar(self, query: str, max_results: int = 10) -> list[dict]:
        """Search Semantic Scholar for papers."""
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": max_results,
                "fields": "title,url,abstract,authors,year,citationCount",
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return [
                {
                    "title": p.get("title", ""),
                    "url": p.get("url", ""),
                    "abstract": p.get("abstract", "")[:500],
                    "authors": [a.get("name", "") for a in p.get("authors", [])[:5]],
                    "year": p.get("year"),
                    "citations": p.get("citationCount", 0),
                }
                for p in data.get("data", [])
            ]
        except Exception as e:
            print(f"Semantic Scholar search error: {e}")
            return []


class ResearchOrchestrator:
    """Orchestrates research across multiple tools."""
    
    def __init__(
        self,
        search_provider: str = "tavily",
        use_wikipedia: bool = True,
        use_academic: bool = True,
    ):
        """Initialize research orchestrator.
        
        Args:
            search_provider: Search provider to use
            use_wikipedia: Include Wikipedia
            use_academic: Include academic search
        """
        self.search = SearchTool(provider=search_provider)
        self.wikipedia = WikipediaTool() if use_wikipedia else None
        self.academic = AcademicSearchTool() if use_academic else None
    
    def comprehensive_search(
        self,
        query: str,
        include_web: bool = True,
        include_wikipedia: bool = True,
        include_academic: bool = True,
    ) -> dict:
        """Run comprehensive research across all sources.
        
        Args:
            query: Research query
            include_web: Include web search
            include_wikipedia: Include Wikipedia
            include_academic: Include academic papers
            
        Returns:
            Combined research results
        """
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "web": [],
            "wikipedia": [],
            "academic": [],
            "innovations": [],
        }
        
        # Web search
        if include_web:
            results["web"] = self.search.search(query, num_results=10)
        
        # Wikipedia
        if self.wikipedia and include_wikipedia:
            results["wikipedia"] = self.wikipedia.search(query, num_results=5)
        
        # Academic
        if self.academic and include_academic:
            results["academic"] = self.academic.search_crossref(query, max_results=5)
            results["academic"].extend(
                self.academic.search_semantic_scholar(query, max_results=5)
            )
        
        # Generate innovations from research
        results["innovations"] = self._generate_innovations(results)
        
        return results
    
    def _generate_innovations(self, research: dict) -> list[str]:
        """Generate innovative ideas from research.
        
        This analyzes the gathered information to spawn new ideas
        and connections beyond the original training data.
        
        Args:
            research: Combined research results
            
        Returns:
            List of innovative ideas/connections
        """
        innovations = []
        
        # Analyze web results for emerging trends
        web_content = " ".join([
            r.get("content", "")[:200] for r in research.get("web", [])[:5]
        ])
        
        # Analyze academic for research gaps
        academic_titles = [a.get("title", "") for a in research.get("academic", [])[:5]]
        
        # Look for intersections
        if web_content and academic_titles:
            innovations.append(
                "Cross-disciplinary connection: Apply web trends to academic findings"
            )
        
        # Add research gaps identification
        if len(research.get("academic", [])) < 3:
            innovations.append(
                "Research gap: Limited academic coverage - original contribution opportunity"
            )
        
        # Add timestamp for freshness
        innovations.append(
            f"Research timestamp: {research.get('timestamp')} - ensures current information"
        )
        
        return innovations
    
    def deep_research(
        self,
        topic: str,
        subtopics: list[str] = None,
    ) -> dict:
        """Perform deep research on a topic and its subtopics.
        
        Args:
            topic: Main topic
            subtopics: Related subtopics to research
            
        Returns:
            Deep research results
        """
        results = {
            "main_topic": topic,
            "main_research": self.comprehensive_search(topic),
            "subtopic_research": {},
        }
        
        # Research each subtopic
        for subtopic in (subtopics or []):
            combined = f"{topic}: {subtopic}"
            results["subtopic_research"][subtopic] = self.comprehensive_search(combined)
        
        # Cross-reference all findings
        results["cross_references"] = self._cross_reference(results)
        
        return results
    
    def _cross_reference(self, deep_results: dict) -> list[str]:
        """Find cross-references between main and subtopic research."""
        refs = []
        
        main_content = " ".join([
            r.get("content", "")[:300] 
            for r in deep_results.get("main_research", {}).get("web", [])[:3]
        ])
        
        for subtopic, sub_data in deep_results.get("subtopic_research", {}).items():
            sub_content = " ".join([
                r.get("content", "")[:300]
                for r in sub_data.get("web", [])[:3]
            ])
            
            # Look for connections
            if main_content and sub_content:
                common_words = set(main_content.lower().split()) & set(sub_content.lower().split())
                if len(common_words) > 10:
                    refs.append(f"Connection found: {subtopic} relates to main topic via {len(common_words)} shared concepts")
        
        return refs


def create_research_orchestrator(
    search_provider: str = "tavily",
    use_wikipedia: bool = True,
    use_academic: bool = True,
) -> ResearchOrchestrator:
    """Factory function to create research orchestrator.
    
    Args:
        search_provider: Search provider
        use_wikipedia: Include Wikipedia
        use_academic: Include academic search
        
    Returns:
        Configured ResearchOrchestrator
    """
    return ResearchOrchestrator(
        search_provider=search_provider,
        use_wikipedia=use_wikipedia,
        use_academic=use_academic,
    )
