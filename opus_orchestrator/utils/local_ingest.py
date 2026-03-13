"""Local file ingestion for Opus Orchestrator.

Fetches content from local files and directories - INCLUDING SOURCE CODE.
The AI witnesses ALL data and transforms it into documentation.
"""

import os
import fnmatch
from pathlib import Path
from typing import Any, Optional


class LocalIngestor:
    """Fetch and parse content from local files and directories.
    
    Supports:
    - ALL file types (including source code!)
    - Directories (recursive)
    - File pattern matching
    
    Philosophy: The AI witnesses everything and transforms it.
    Don't filter what the AI can see - let it decide what's relevant.
    """
    
    def __init__(
        self,
        root_path: Optional[str] = None,
        encoding: str = "utf-8",
    ):
        """Initialize local ingestor.
        
        Args:
            root_path: Root directory for relative paths
            encoding: Text file encoding
        """
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.encoding = encoding
        
        # INCLUDE ALL FILES - let the AI witness everything!
        # Only exclude build artifacts and version control
        self.exclude_patterns = [
            ".git",
            ".svn",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            ".env",
            "*.pyc",
            "*.so",
            "*.o",
            "*.a",
            "*.dylib",
            ".DS_Store",
            "*.swp",
            "*.tmp",
            ".cache",
            "dist",
            "build",
            "*.egg-info",
            ".pytest_cache",
            ".mypy_cache",
            ".tox",
        ]

    def is_excluded(self, path: Path) -> bool:
        """Check if a path should be excluded.
        
        Args:
            path: Path to check
            
        Returns:
            True if should be excluded
        """
        name = path.name
        
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        
        return False

    def get_files(
        self,
        path: str | Path,
        extensions: Optional[list[str]] = None,
        recursive: bool = True,
        max_files: int = 1000,
        include_all: bool = True,
    ) -> dict[Path, str]:
        """Get all files from a path - INCLUDING SOURCE CODE.
        
        The AI witnesses everything and transforms it into documentation.
        
        Args:
            path: File or directory path
            extensions: File extensions to include (None = ALL files!)
            recursive: Recursively scan directories
            max_files: Maximum number of files to read
            include_all: If True, include ALL files (default True!)
            
        Returns:
            Dict mapping file paths to content
        """
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        # Default: include ALL files (source code, configs, everything!)
        # The AI will witness and transform everything
        if include_all:
            extensions = None  # Include everything
        else:
            extensions = extensions or self.default_extensions
            extensions = [ext.lower() for ext in extensions]
        
        results = {}
        
        if path.is_file():
            # Single file
            if include_all or self._has_valid_extension(path, extensions or []):
                results[path] = self._read_file(path)
        else:
            # Directory
            files = self._scan_directory(
                path, 
                extensions, 
                recursive, 
                max_files - len(results),
                include_all=include_all,
            )
            
            for f in files:
                try:
                    results[f] = self._read_file(f)
                except Exception as e:
                    print(f"Warning: Could not read {f}: {e}")
        
        return results

    def _has_valid_extension(self, path: Path, extensions: list[str]) -> bool:
        """Check if file has a valid extension."""
        ext = path.suffix.lower()
        return ext in extensions or path.suffix == ""  # Allow no extension

    def _scan_directory(
        self,
        directory: Path,
        extensions: Optional[list[str]],
        recursive: bool,
        max_files: int,
        include_all: bool = True,
    ) -> list[Path]:
        """Scan directory for matching files."""
        files = []
        
        try:
            if recursive:
                for root, dirs, filenames in os.walk(directory):
                    # Filter out excluded directories
                    dirs[:] = [d for d in dirs if not self.is_excluded(Path(d))]
                    
                    for filename in filenames:
                        filepath = Path(root) / filename
                        
                        if self.is_excluded(filepath):
                            continue
                        
                        # Include ALL files (including source code!)
                        if include_all or self._has_valid_extension(filepath, extensions or []):
                            files.append(filepath)
                            
                            if len(files) >= max_files:
                                return files
            else:
                # Non-recursive
                for item in directory.iterdir():
                    if item.is_file() and not self.is_excluded(item):
                        if include_all or self._has_valid_extension(item, extensions or []):
                            files.append(item)
                            
                            if len(files) >= max_files:
                                break
        
        except PermissionError:
            print(f"Warning: Permission denied for {directory}")
        
        return files

    def _read_file(self, path: Path) -> str:
        """Read file content."""
        try:
            with open(path, "r", encoding=self.encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception:
                return f"[Binary file: {path}]"
        except Exception as e:
            return f"[Error reading {path}: {e}]"

    def ingest(
        self,
        path: str | Path,
        extensions: Optional[list[str]] = None,
        recursive: bool = True,
    ) -> dict[str, Any]:
        """Ingest content from local path.
        
        Args:
            path: File or directory path
            extensions: File extensions to include
            recursive: Recursively scan directories
            
        Returns:
            Dict with combined text and metadata
        """
        files = self.get_files(path, extensions, recursive)
        
        # Combine content with file separators
        combined_lines = []
        for filepath, content in sorted(files.items()):
            rel_path = filepath.relative_to(self.root_path) if filepath.is_relative_to(self.root_path) else filepath
            combined_lines.append(f"=== {rel_path} ===")
            combined_lines.append(content)
            combined_lines.append("")
        
        combined_text = "\n".join(combined_lines)
        
        return {
            "path": str(path),
            "files": {str(k): v for k, v in files.items()},
            "file_count": len(files),
            "total_chars": len(combined_text),
            "combined_text": combined_text,
        }

    def summarize(self, content: str, max_length: int = 5000) -> str:
        """Create a summary of content for use as seed.
        
        Args:
            content: Full content
            max_length: Maximum length of summary
            
        Returns:
            Summarized content
        """
        if len(content) <= max_length:
            return content
        
        # Take first portion + indicator
        return content[:max_length] + f"\n\n[...] ({len(content) - max_length} more characters)"


def create_local_ingestor(root_path: Optional[str] = None) -> LocalIngestor:
    """Factory function to create a local ingestor.
    
    Args:
        root_path: Root directory
        
    Returns:
        Configured LocalIngestor
    """
    return LocalIngestor(root_path=root_path)
