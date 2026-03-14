"""LaTeX Compile for Opus Orchestrator.

Handles conversion to LaTeX and PDF compilation.
"""

import os
import re
import subprocess
import shutil
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

from opus_orchestrator.schemas import Manuscript, Chapter


@dataclass
class CompileOptions:
    """Options for LaTeX compilation."""
    template: str = "memoir"  # memoir, academic, base
    output_format: str = "pdf"  # pdf, tex
    theme: str = "light"  # light, dark, sepia
    font: str = "serif"  # serif, sans, mono
    include_toc: bool = True
    include_index: bool = False
    dedication: str = ""
    epigraph: str = ""
    acknowledgments: str = ""
    abstract: str = ""
    bibliography: str = ""
    author: str = "Opus Orchestrator"
    publisher: str = ""
    isbn: str = ""
    edition: str = ""
    series: str = ""
    date: str = ""
    
    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().strftime("%Y")


class LaTeXExporter:
    """Export manuscript to LaTeX and compile to PDF."""
    
    TEMPLATES = {
        # KDP Templates (print-ready)
        "kdp-pocket": "kdp-pocket.tex",     # 5x8 mass market
        "kdp-trade": "kdp-trade.tex",     # 5.5x8.5 standard
        "kdp-6x9": "kdp-6x9.tex",         # 6x9 popular
        "kdp-square": "kdp-square.tex",     # 8x8 art/photo
        "kdp-large": "kdp-large.tex",      # 8.5x11 workbook
        
        # Book Types
        "novel": "novel.tex",              # General fiction
        "memoir": "memoir.tex",           # Memoir/personal
        "hardcover": "hardcover.tex",      # Premium hardcover
        "poetry": "poetry.tex",           # Poetry collections
        "childrens": "childrens.tex",     # Picture books
        
        # Technical/Educational
        "academic": "academic.tex",        # Academic papers
        "textbook": "textbook.tex",       # With exercises
        "journal": "journal.tex",          # Workbooks/planners
        
        # Specialty
        "screenplay": "screenplay.tex",   # Film/TV scripts
        
        # Base
        "base": "base.tex",               # Minimal template
    }
    
    def __init__(self, template_dir: Optional[str] = None):
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            # Default to package templates
            self.template_dir = Path(__file__).parent / "templates" / "latex"
    
    def export(
        self,
        manuscript: Manuscript,
        book_title: str,
        options: Optional[CompileOptions] = None,
    ) -> dict:
        """Export manuscript to LaTeX.
        
        Args:
            manuscript: The Manuscript to export
            book_title: Title for the book
            options: CompileOptions
            
        Returns:
            Export metadata with file paths
        """
        opts = options or CompileOptions(template="memoir")
        
        # Get template
        template_file = self.TEMPLATES.get(opts.template, "memoir.tex")
        template_path = self.template_dir / template_file
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # Read template
        template_content = template_path.read_text()
        
        # Build body from chapters
        body = self._build_body(manuscript)
        
        # Fill template
        latex_content = self._fill_template(
            template_content,
            body,
            book_title,
            opts,
        )
        
        return {
            "latex": latex_content,
            "template": opts.template,
            "options": opts,
        }
    
    def export_to_file(
        self,
        manuscript: Manuscript,
        book_title: str,
        output_path: str,
        options: Optional[CompileOptions] = None,
    ) -> dict:
        """Export to .tex file."""
        result = self.export(manuscript, book_title, options)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result["latex"])
        
        result["output_file"] = str(output_file)
        return result
    
    def compile(
        self,
        manuscript: Manuscript,
        book_title: str,
        output_path: str,
        options: Optional[CompileOptions] = None,
    ) -> dict:
        """Export and compile to PDF.
        
        Args:
            manuscript: The Manuscript
            book_title: Book title
            output_path: Output .pdf path
            options: CompileOptions
            
        Returns:
            Compilation result with paths
        """
        # First export to tex
        tex_path = output_path.replace(".pdf", ".tex")
        result = self.export_to_file(manuscript, book_title, tex_path, options)
        
        # Try to compile
        compile_result = self._compile_latex(tex_path)
        
        result.update(compile_result)
        result["pdf_path"] = output_path if compile_result.get("success") else None
        
        return result
    
    def _build_body(self, manuscript: Manuscript) -> str:
        """Build LaTeX body from chapters."""
        parts = []
        
        for chapter in manuscript.chapters:
            # Chapter heading
            parts.append(f"\\chapter{{{chapter.title}}}")
            parts.append("")
            
            # Content (convert markdown to latex)
            content = self._markdown_to_latex(chapter.content or "")
            parts.append(content)
            parts.append("")
        
        return "\n".join(parts)
    
    def _markdown_to_latex(self, text: str) -> str:
        """Convert basic markdown to LaTeX."""
        # Headers
        text = re.sub(r'^### (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'\\chapter{\1}', text, flags=re.MULTILINE)
        
        # Bold/italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
        text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
        
        # Code blocks
        text = re.sub(r'```(\w+)?\n(.+?)```', r'\\begin{verbatim}\2\\end{verbatim}', text, flags=re.DOTALL)
        
        # Inline code
        text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)
        
        # Lists
        text = re.sub(r'^- (.+)$', r'\\item \1', text, flags=re.MULTILINE)
        text = re.sub(r'^\d+\. (.+)$', r'\\item \1', text, flags=re.MULTILINE)
        
        # Blockquotes
        text = re.sub(r'^> (.+)$', r'\\begin{quote}\1\\end{quote}', text, flags=re.MULTILINE)
        
        # Horizontal rule
        text = re.sub(r'^---$', r'\\hrulefill', text, flags=re.MULTILINE)
        
        return text
    
    def _fill_template(
        self,
        template: str,
        body: str,
        book_title: str,
        options: CompileOptions,
    ) -> str:
        """Fill template with content."""
        # Build replacements
        replacements = {
            "book_title": book_title,
            "author": options.author,
            "date": options.date,
            "publisher": options.publisher,
            "isbn": options.isbn,
            "edition": options.edition,
            "series": options.series,
            "dedication": options.dedication,
            "epigraph": options.epigraph,
            "acknowledgments": options.acknowledgments,
            "abstract": options.abstract,
            "bibliography": options.bibliography,
            "body": body,
        }
        
        # Fill template - handle both ${var} and $var
        content = template
        for key, value in replacements.items():
            # Replace ${var}
            content = content.replace(f"${{{key}}}", str(value))
            # Replace standalone $var 
            dollar_key = f"${key}"
            content = content.replace(dollar_key, str(value))
        
        return content
    
    def _compile_latex(self, tex_path: str) -> dict:
        """Compile LaTeX to PDF."""
        tex_file = Path(tex_path)
        if not tex_file.exists():
            return {"success": False, "error": "TeX file not found"}
        
        # Check for xelatex
        xelatex = shutil.which("xelatex")
        if not xelatex:
            return {
                "success": False,
                "error": "xelatex not found. Install with: brew install texlab or apt install texlive-xelatex",
                "tex_file": str(tex_file),
            }
        
        # Compile
        work_dir = tex_file.parent
        
        try:
            # Run xelatex
            result = subprocess.run(
                [xelatex, "-interaction=nonstopmode", tex_file.name],
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            success = result.returncode == 0
            
            return {
                "success": success,
                "returncode": result.returncode,
                "stdout": result.stdout[-2000:] if result.stdout else "",
                "stderr": result.stderr[-2000:] if result.stderr else "",
                "tex_file": str(tex_file),
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Compilation timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def export_to_latex(
    manuscript: Manuscript,
    book_title: str,
    output_path: str,
    template: str = "memoir",
    **options,
) -> dict:
    """Convenience function to export to LaTeX.
    
    Args:
        manuscript: The Manuscript
        book_title: Book title  
        output_path: Output .tex path
        template: Template name (memoir, academic, base)
        **options: Additional CompileOptions
        
    Returns:
        Export result
    """
    opts = CompileOptions(template=template, **options)
    exporter = LaTeXExporter()
    return exporter.export_to_file(manuscript, book_title, output_path, opts)


def compile_pdf(
    manuscript: Manuscript,
    book_title: str,
    output_path: str,
    template: str = "memoir",
    **options,
) -> dict:
    """Convenience function to compile to PDF.
    
    Args:
        manuscript: The Manuscript
        book_title: Book title
        output_path: Output .pdf path
        template: Template name
        **options: Additional CompileOptions
        
    Returns:
        Compilation result
    """
    opts = CompileOptions(template=template, **options)
    exporter = LaTeXExporter()
    return exporter.compile(manuscript, book_title, output_path, opts)
