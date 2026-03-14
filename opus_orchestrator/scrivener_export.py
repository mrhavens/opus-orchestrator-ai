"""Scrivener-style output for Opus Orchestrator.

Generates chapter-by-chapter output with binder.json metadata.
"""

import json
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

from opus_orchestrator.schemas import Manuscript, Chapter


@dataclass
class ChapterFile:
    """A single chapter file."""
    filename: str
    title: str
    content: str
    word_count: int
    order: int


@dataclass
class BinderItem:
    """A binder item (chapter or folder)."""
    id: str
    type: str  # "chapter" or "folder"
    title: str
    filename: str
    order: int
    word_count: int
    children: list = None
    
    def to_dict(self):
        d = asdict(self)
        if self.children:
            d['children'] = [c.to_dict() if hasattr(c, 'to_dict') else c for c in self.children]
        return d


class ScrivenerExporter:
    """Export manuscript in Scrivener-style folder structure."""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
    
    def export(
        self,
        manuscript: Manuscript,
        book_title: str,
        split_chapters: bool = True,
    ) -> dict:
        """Export manuscript to Scrivener-style structure.
        
        Args:
            manuscript: The Manuscript to export
            book_title: Title for the book folder
            split_chapters: If True, split into individual files
            
        Returns:
            Export metadata with file paths and word counts
        """
        # Create book folder
        book_folder = self.output_dir / self._slugify(book_title)
        book_folder.mkdir(parents=True, exist_ok=True)
        
        if split_chapters:
            return self._export_split(manuscript, book_folder, book_title)
        else:
            return self._export_single(manuscript, book_folder, book_title)
    
    def _export_split(
        self,
        manuscript: Manuscript,
        book_folder: Path,
        book_title: str,
    ) -> dict:
        """Export as individual chapter files."""
        binder = []
        total_words = 0
        
        for idx, chapter in enumerate(manuscript.chapters):
            order = idx + 1
            filename = f"{order:02d}_{self._slugify(chapter.title)}.md"
            filepath = book_folder / filename
            
            # Write chapter file
            content = self._format_chapter(chapter, order)
            filepath.write_text(content, encoding='utf-8')
            
            word_count = len(content.split())
            total_words += word_count
            
            binder.append(BinderItem(
                id=f"chapter-{order}",
                type="chapter",
                title=chapter.title,
                filename=filename,
                order=order,
                word_count=word_count,
            ))
        
        # Write binder.json
        binder_data = {
            "version": "1.0",
            "title": book_title,
            "total_chapters": len(manuscript.chapters),
            "total_words": total_words,
            "items": [item.to_dict() for item in binder],
        }
        
        binder_path = book_folder / "binder.json"
        binder_path.write_text(
            json.dumps(binder_data, indent=2),
            encoding='utf-8'
        )
        
        # Write metadata.json
        metadata = {
            "title": book_title,
            "book_type": manuscript.book_type.value if hasattr(manuscript.book_type, 'value') else str(manuscript.book_type),
            "genre": manuscript.genre,
            "total_chapters": len(manuscript.chapters),
            "total_words": total_words,
            "chapters": [
                {
                    "order": item.order,
                    "title": item.title,
                    "filename": item.filename,
                    "word_count": item.word_count,
                }
                for item in binder
            ],
        }
        
        metadata_path = book_folder / "metadata.json"
        metadata_path.write_text(
            json.dumps(metadata, indent=2),
            encoding='utf-8'
        )
        
        return {
            "book_folder": str(book_folder),
            "chapters": len(manuscript.chapters),
            "total_words": total_words,
            "binder": str(binder_path),
        }
    
    def _export_single(
        self,
        manuscript: Manuscript,
        book_folder: Path,
        book_title: str,
    ) -> dict:
        """Export as single file."""
        filename = f"{self._slugify(book_title)}.md"
        filepath = book_folder / filename
        
        content = self._format_manuscript(manuscript)
        filepath.write_text(content, encoding='utf-8')
        
        word_count = len(content.split())
        
        # Simple binder with just the main file
        binder_data = {
            "version": "1.0",
            "title": book_title,
            "total_chapters": 1,
            "total_words": word_count,
            "items": [
                {
                    "id": "manuscript",
                    "type": "chapter",
                    "title": book_title,
                    "filename": filename,
                    "order": 1,
                    "word_count": word_count,
                }
            ],
        }
        
        binder_path = book_folder / "binder.json"
        binder_path.write_text(
            json.dumps(binder_data, indent=2),
            encoding='utf-8'
        )
        
        return {
            "book_folder": str(book_folder),
            "chapters": 1,
            "total_words": word_count,
            "binder": str(binder_path),
        }
    
    def _format_chapter(self, chapter: Chapter, order: int) -> str:
        """Format a single chapter with frontmatter."""
        word_count = len(chapter.content.split()) if chapter.content else 0
        
        frontmatter = f"""---
chapter: {order}
title: "{chapter.title}"
word_count: {word_count}
---

"""
        
        # Add chapter heading if not in content
        content = chapter.content or ""
        if not content.strip().startswith("#"):
            content = f"# {chapter.title}\n\n{content}"
        
        return frontmatter + content
    
    def _format_manuscript(self, manuscript: Manuscript) -> str:
        """Format entire manuscript."""
        parts = [f"# {manuscript.title}\n"]
        
        for chapter in manuscript.chapters:
            parts.append(f"\n---\n\n")
            parts.append(f"## {chapter.title}\n\n")
            parts.append(chapter.content or "")
        
        return "".join(parts)
    
    def _slugify(self, text: str) -> str:
        """Convert title to filename-safe slug."""
        # Remove special chars, replace spaces with underscores
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')


def export_to_scrivener(
    manuscript: Manuscript,
    book_title: str,
    output_dir: str = "./output",
    split_chapters: bool = True,
) -> dict:
    """Convenience function to export in Scrivener style.
    
    Args:
        manuscript: The Manuscript to export
        book_title: Title for the book
        output_dir: Output directory
        split_chapters: Split into individual chapter files
        
    Returns:
        Export metadata
    """
    exporter = ScrivenerExporter(output_dir)
    return exporter.export(manuscript, book_title, split_chapters)
