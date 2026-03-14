"""Scrivener-style output for Opus Orchestrator.

Generates chapter-by-chapter output with binder.json metadata.
Supports auto-branching and push to GitHub.
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from opus_orchestrator.schemas import Manuscript, Chapter


@dataclass
class ExportOptions:
    """Options for Scrivener export."""
    output_dir: str = "./output"
    split_chapters: bool = True
    branch: str = "draft/generated"
    push_to_remote: bool = False
    commit_message: str = ""
    author_name: str = "Opus Orchestrator"
    author_email: str = "opus@clowder.net"
    
    def __post_init__(self):
        if not self.commit_message:
            self.commit_message = f"Auto-export: {datetime.now().strftime('%Y-%m-%d %H:%M')}"


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
        options: Optional[ExportOptions] = None,
    ) -> dict:
        """Export manuscript to Scrivener-style structure.
        
        Args:
            manuscript: The Manuscript to export
            book_title: Title for the book folder
            options: ExportOptions (optional)
            
        Returns:
            Export metadata with file paths and word counts
        """
        opts = options or ExportOptions(
            output_dir=opts.output_dir if options else "./output",
            split_chapters=options.split_chapters if options else True,
        )
        
        # Create book folder
        book_folder = self.output_dir / self._slugify(book_title)
        book_folder.mkdir(parents=True, exist_ok=True)
        
        if opts.split_chapters:
            result = self._export_split(manuscript, book_folder, book_title)
        else:
            result = self._export_single(manuscript, book_folder, book_title)
        
        # Optionally push to GitHub
        if opts.push_to_remote:
            push_result = self._push_to_git(
                book_folder,
                opts.branch,
                opts.commit_message,
                opts.author_name,
                opts.author_email,
            )
            result.update(push_result)
        
        return result
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


    def _push_to_git(
        self,
        folder: Path,
        branch: str,
        commit_message: str,
        author_name: str,
        author_email: str,
    ) -> dict:
        """Push exported folder to GitHub.
        
        Args:
            folder: Folder to push
            branch: Branch name (will be created if doesn't exist)
            commit_message: Commit message
            author_name: Git author name
            author_email: Git author email
            
        Returns:
            Push result metadata
        """
        import subprocess
        
        # Check if git repo exists
        git_dir = folder / ".git"
        if not git_dir.exists():
            # Initialize new repo
            subprocess.run(["git", "init"], cwd=folder, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", author_email], cwd=folder, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", author_name], cwd=folder, check=True, capture_output=True)
        
        # Add all files
        subprocess.run(["git", "add", "."], cwd=folder, check=True, capture_output=True)
        
        # Check if there are changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=folder,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            return {"pushed": False, "reason": "No changes to commit"}
        
        # Commit
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=folder,
            check=True,
            capture_output=True
        )
        
        # Get or add remote
        remotes = subprocess.run(
            ["git", "remote", "-v"],
            cwd=folder,
            capture_output=True,
            text=True
        )
        
        if not remotes.stdout.strip():
            # No remote set - can't push
            return {
                "pushed": False, 
                "reason": "No remote configured. Add one with: git remote add origin <url>"
            }
        
        # Push to branch
        try:
            subprocess.run(
                ["git", "push", "-u", "origin", branch, "--no-verify"],
                cwd=folder,
                check=True,
                capture_output=True
            )
            return {
                "pushed": True,
                "branch": branch,
                "commit_message": commit_message,
            }
        except subprocess.CalledProcessError as e:
            return {
                "pushed": False,
                "reason": f"Push failed: {e.stderr.decode() if e.stderr else str(e)}"
            }


def export_to_scrivener(
    manuscript: Manuscript,
    book_title: str,
    output_dir: str = "./output",
    split_chapters: bool = True,
    branch: str = "draft/generated",
    push_to_remote: bool = False,
    commit_message: str = "",
) -> dict:
    """Convenience function to export in Scrivener style.
    
    Args:
        manuscript: The Manuscript to export
        book_title: Title for the book
        output_dir: Output directory
        split_chapters: Split into individual chapter files
        branch: Branch to push to (default: draft/generated)
        push_to_remote: Whether to push to GitHub remote
        commit_message: Custom commit message
        
    Returns:
        Export metadata
    """
    options = ExportOptions(
        output_dir=output_dir,
        split_chapters=split_chapters,
        branch=branch,
        push_to_remote=push_to_remote,
        commit_message=commit_message,
    )
    
    exporter = ScrivenerExporter(output_dir)
    return exporter.export(manuscript, book_title, options)
