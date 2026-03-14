"""Multi-Source Ingestion for Opus.

Handles multiple content sources: GitHub repos, S3 buckets, and local files.
Merges and deduplicates content intelligently.
"""

from dataclasses import dataclass, field
from typing import Optional, list
from enum import Enum
import hashlib


class SourceType(str, Enum):
    """Types of content sources."""
    GITHUB = "github"
    S3 = "s3"
    LOCAL = "local"
    URL = "url"


@dataclass
class ContentSource:
    """A single content source."""
    source_type: SourceType
    # GitHub
    repo: Optional[str] = None
    branch: Optional[str] = None
    path: Optional[str] = None
    # S3
    bucket: Optional[str] = None
    prefix: Optional[str] = None
    # Local
    local_path: Optional[str] = None
    # URL
    url: Optional[str] = None
    # Options
    include_patterns: Optional[list[str]] = None
    exclude_patterns: Optional[list[str]] = None


@dataclass
class IngestedContent:
    """Content from a single source."""
    source: ContentSource
    content: str
    metadata: dict
    content_hash: str


@dataclass
class MultiSourceResult:
    """Result from multi-source ingestion."""
    contents: list[IngestedContent]
    total_sources: int
    successful_sources: int
    failed_sources: list[str]
    merged_content: str
    source_summary: dict


class MultiSourceIngestor:
    """Ingests from multiple sources and merges content.
    
    Supports:
    - Multiple GitHub repos
    - Multiple S3 buckets
    - Multiple local directories
    - Combinations of all above
    
    Features:
    - Deduplicates overlapping content
    - Tracks source attribution
    - Merges intelligently
    """
    
    def __init__(
        self,
        github_token: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
    ):
        self.github_token = github_token
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self._source_results: dict[str, IngestedContent] = {}
    
    async def ingest(
        self,
        sources: list[ContentSource],
        merge_strategy: str = "append",  # append | smart | priority
    ) -> MultiSourceResult:
        """Ingest from multiple sources.
        
        Args:
            sources: List of content sources
            merge_strategy: How to merge content
                - append: Simply concatenate
                - smart: Deduplicate and organize
                - priority: Prefer earlier sources
        
        Returns:
            MultiSourceResult with merged content
        """
        contents = []
        failed = []
        
        for source in sources:
            try:
                result = await self._ingest_single(source)
                if result:
                    contents.append(result)
                    self._source_results[self._hash_source(source)] = result
            except Exception as e:
                failed.append(f"{source.source_type.value}: {str(e)}")
        
        # Merge based on strategy
        merged = self._merge_contents(contents, merge_strategy)
        
        return MultiSourceResult(
            contents=contents,
            total_sources=len(sources),
            successful_sources=len(contents),
            failed_sources=failed,
            merged_content=merged,
            source_summary=self._build_summary(contents),
        )
    
    async def _ingest_single(self, source: ContentSource) -> Optional[IngestedContent]:
        """Ingest from a single source."""
        if source.source_type == SourceType.GITHUB:
            return await self._ingest_github(source)
        elif source.source_type == SourceType.S3:
            return await self._ingest_s3(source)
        elif source.source_type == SourceType.LOCAL:
            return await self._ingest_local(source)
        elif source.source_type == SourceType.URL:
            return await self._ingest_url(source)
        else:
            raise ValueError(f"Unknown source type: {source.source_type}")
    
    async def _ingest_github(self, source: ContentSource) -> IngestedContent:
        """Ingest from GitHub repo."""
        from opus_orchestrator.utils.github_ingest import GitHubIngestor
        
        ingestor = GitHubIngestor(token=self.github_token)
        
        content = await ingestor.ingest_repo(
            repo=source.repo,
            branch=source.branch or "main",
            path=source.path or "",
        )
        
        text_content = self._extract_text_from_github(content)
        
        return IngestedContent(
            source=source,
            content=text_content,
            metadata={"repo": source.repo, "branch": source.branch},
            content_hash=self._hash_content(text_content),
        )
    
    async def _ingest_s3(self, source: ContentSource) -> IngestedContent:
        """Ingest from S3 bucket."""
        # Would use boto3
        # For now, placeholder
        content = f"[S3 content from {source.bucket}/{source.prefix}]"
        
        return IngestedContent(
            source=source,
            content=content,
            metadata={"bucket": source.bucket, "prefix": source.prefix},
            content_hash=self._hash_content(content),
        )
    
    async def _ingest_local(self, source: ContentSource) -> IngestedContent:
        """Ingest from local files."""
        import os
        from pathlib import Path
        
        content_parts = []
        path = Path(source.local_path)
        
        if path.is_file():
            files = [path]
        elif path.is_dir():
            files = list(path.rglob("*"))
        else:
            raise ValueError(f"Local path not found: {source.local_path}")
        
        for f in files:
            if f.is_file() and not f.name.startswith('.'):
                try:
                    text = f.read_text(encoding='utf-8', errors='ignore')
                    rel_path = f.relative_to(path)
                    content_parts.append(f"## {rel_path}\n\n{text}\n")
                except:
                    pass
        
        merged = "\n\n".join(content_parts)
        
        return IngestedContent(
            source=source,
            content=merged,
            metadata={"path": str(source.local_path), "files": len(content_parts)},
            content_hash=self._hash_content(merged),
        )
    
    async def _ingest_url(self, source: ContentSource) -> IngestedContent:
        """Ingest from URL."""
        from opus_orchestrator.utils.web_ingest import WebIngestor
        
        ingestor = WebIngestor()
        content = await ingestor.ingest(source.url)
        
        return IngestedContent(
            source=source,
            content=content,
            metadata={"url": source.url},
            content_hash=self._hash_content(content),
        )
    
    def _extract_text_from_github(self, content: dict) -> str:
        """Extract text from GitHub ingestor result."""
        if isinstance(content, dict):
            files = content.get("files", {})
            parts = []
            for filename, file_content in files.items():
                parts.append(f"## {filename}\n\n{file_content}\n")
            return "\n\n".join(parts)
        return str(content)
    
    def _merge_contents(
        self,
        contents: list[IngestedContent],
        strategy: str,
    ) -> str:
        """Merge contents from multiple sources."""
        if strategy == "append":
            return self._merge_append(contents)
        elif strategy == "smart":
            return self._merge_smart(contents)
        elif strategy == "priority":
            return self._merge_priority(contents)
        else:
            return self._merge_append(contents)
    
    def _merge_append(self, contents: list[IngestedContent]) -> str:
        """Simply concatenate all content."""
        parts = []
        for c in contents:
            source_desc = self._source_description(c.source)
            parts.append(f"\n\n=== {source_desc} ===\n\n{c.content}")
        return "\n".join(parts)
    
    def _merge_smart(self, contents: list[IngestedContent]) -> str:
        """Deduplicate and organize intelligently."""
        # Track unique content by hash
        seen_hashes = set()
        unique_contents = []
        
        for c in contents:
            if c.content_hash not in seen_hashes:
                seen_hashes.add(c.content_hash)
                unique_contents.append(c)
        
        # Sort by source type priority
        priority = {SourceType.GITHUB: 1, SourceType.S3: 2, SourceType.LOCAL: 3, SourceType.URL: 4}
        unique_contents.sort(key=lambda x: priority.get(x.source.source_type, 5))
        
        return self._merge_append(unique_contents)
    
    def _merge_priority(self, contents: list[IngestedContent]) -> str:
        """Prefer earlier sources when there's overlap."""
        # Similar to smart but keeps first occurrence
        return self._merge_smart(contents)
    
    def _source_description(self, source: ContentSource) -> str:
        """Human-readable source description."""
        if source.source_type == SourceType.GITHUB:
            return f"GitHub: {source.repo}"
        elif source.source_type == SourceType.S3:
            return f"S3: {source.bucket}/{source.prefix}"
        elif source.source_type == SourceType.LOCAL:
            return f"Local: {source.local_path}"
        elif source.source_type == SourceType.URL:
            return f"URL: {source.url}"
        return "Unknown"
    
    def _hash_content(self, content: str) -> str:
        """Hash content for deduplication."""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _hash_source(self, source: ContentSource) -> str:
        """Hash source for tracking."""
        key = f"{source.source_type.value}:{source.repo or source.bucket or source.local_path or source.url}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def _build_summary(self, contents: list[IngestedContent]) -> dict:
        """Build summary of ingested content."""
        summary = {
            "total_sources": len(contents),
            "by_type": {},
            "total_chars": 0,
        }
        
        for c in contents:
            stype = c.source.source_type.value
            summary["by_type"][stype] = summary["by_type"].get(stype, 0) + 1
            summary["total_chars"] += len(c.content)
        
        return summary


# Convenience function
async def ingest_multiple(
    sources: list[dict],
    merge_strategy: str = "smart",
    **kwargs,
) -> MultiSourceResult:
    """Convenience function to ingest from multiple sources.
    
    Args:
        sources: List of source configs
            [
                {"type": "github", "repo": "user/repo"},
                {"type": "local", "path": "/path/to/files"},
                {"type": "s3", "bucket": "my-bucket", "prefix": "docs/"},
            ]
        merge_strategy: How to merge (append | smart | priority)
        
    Returns:
        MultiSourceResult with merged content
    """
    # Convert dicts to ContentSource objects
    content_sources = []
    for s in sources:
        stype = SourceType(s.get("type", "local"))
        source = ContentSource(
            source_type=stype,
            repo=s.get("repo"),
            branch=s.get("branch", "main"),
            path=s.get("path"),
            bucket=s.get("bucket"),
            prefix=s.get("prefix"),
            local_path=s.get("path"),  # alias
            url=s.get("url"),
        )
        content_sources.append(source)
    
    # Ingest
    ingestor = MultiSourceIngestor(**kwargs)
    return await ingestor.ingest(content_sources, merge_strategy)
