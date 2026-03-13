"""GitHub ingestion for Opus Orchestrator.

Fetches content from GitHub repositories for use as source material.
"""

import os
import base64
import re
from typing import Any, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class GitHubIngestor:
    """Fetch and parse content from GitHub repositories."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN or pass token.")
        
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.base_url = "https://api.github.com"
    
    def get_contents(self, repo: str, path: str = "") -> list[dict]:
        """Get contents of a directory or file.
        
        Args:
            repo: "owner/repo" format
            path: directory path (default: root)
            
        Returns:
            List of content items
        """
        url = f"{self.base_url}/repos/{repo}/contents/{path}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_file_content(self, repo: str, path: str) -> str:
        """Get content of a single file.
        
        Args:
            repo: "owner/repo" format
            path: file path
            
        Returns:
            Decoded file content
        """
        url = f"{self.base_url}/repos/{repo}/contents/{path}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Decode base64 content
        if data.get("encoding") == "base64":
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content
        
        return data.get("content", "")
    
    def get_all_files(
        self,
        repo: str,
        extensions: Optional[list[str]] = None,
        exclude_dirs: Optional[list[str]] = None,
        include_all: bool = True,
    ) -> dict[str, str]:
        """Get all files from a repository - INCLUDING SOURCE CODE.
        
        The AI witnesses EVERYTHING and transforms it into documentation.
        Don't filter what the AI can see - let it decide what's relevant.
        
        Args:
            repo: "owner/repo" format
            extensions: File extensions to include (None = ALL files!)
            exclude_dirs: Directories to exclude (build artifacts, etc.)
            include_all: If True, include ALL files (default True!)
            
        Returns:
            Dictionary mapping file paths to content
        """
        # Default: include ALL files - the AI will witness everything!
        if include_all:
            extensions = None  # No extension filter
            exclude_dirs = exclude_dirs or [".git", "node_modules", "__pycache__", ".github", "dist", "build", "*.egg-info"]
        else:
            extensions = extensions or [".md", ".txt", ".text", ".notes", ".draft", ".rst"]
            exclude_dirs = exclude_dirs or [".git", "node_modules", "__pycache__", ".github"]
        
        files = {}
        
        def walk_directory(path: str = ""):
            contents = self.get_contents(repo, path)
            
            if isinstance(contents, dict):
                # Single file
                if contents.get("type") == "file":
                    content_path = contents["path"]
                    if self._should_include(content_path, extensions, exclude_dirs, include_all):
                        files[content_path] = self.get_file_content(repo, content_path)
                return
            
            for item in contents:
                item_path = item.get("path", "")
                item_type = item.get("type")
                
                if item_type == "dir":
                    # Check if excluded
                    if not any(excl in item_path for excl in exclude_dirs):
                        walk_directory(item_path)
                elif item_type == "file":
                    if self._should_include(item_path, extensions, exclude_dirs, include_all):
                        files[item_path] = self.get_file_content(repo, item_path)
        
        walk_directory()
        return files
    
    def _should_include(
        self,
        path: str,
        extensions: Optional[list[str]],
        exclude_dirs: list[str],
        include_all: bool = True,
    ) -> bool:
        """Check if file should be included.
        
        Args:
            path: File path to check
            extensions: List of extensions (None if include_all=True)
            exclude_dirs: Directories to exclude
            include_all: Include ALL files (ignore extensions)
        """
        # Exclude directories
        for excl in exclude_dirs:
            if excl in path:
                return False
        
        # If include_all, include everything
        if include_all:
            return True
        
        # Otherwise check extensions
        if extensions:
            return any(path.endswith(ext) for ext in extensions)
        
        return True
    
    def extract_text_from_files(self, files: dict[str, str]) -> str:
        """Combine all file contents into a single text blob.
        
        Args:
            files: Dictionary of filename -> content
            
        Returns:
            Combined text
        """
        combined = []
        
        for filename, content in sorted(files.items()):
            combined.append(f"=== {filename} ===\n")
            combined.append(content)
            combined.append("\n\n")
        
        return "".join(combined)
    
    def ingest_repo(
        self,
        repo: str,
        include_readme: bool = True,
    ) -> dict[str, Any]:
        """Ingest a complete repository.
        
        Args:
            repo: "owner/repo" format
            include_readme: Include README.md files
            
        Returns:
            Dictionary with files, combined_text, and metadata
        """
        # Get all markdown and text files
        files = self.get_all_files(repo)
        
        # Optionally exclude README
        if not include_readme:
            files = {k: v for k, v in files.items() if "README" not in k}
        
        # Combine into single text
        combined = self.extract_text_from_files(files)
        
        return {
            "repo": repo,
            "files": files,
            "combined_text": combined,
            "file_count": len(files),
            "total_chars": len(combined),
        }


def create_github_ingestor(token: Optional[str] = None) -> GitHubIngestor:
    """Factory function to create GitHub ingestor."""
    return GitHubIngestor(token=token)
