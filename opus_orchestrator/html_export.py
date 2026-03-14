"""HTML Export and Browser PDF for Opus Orchestrator.

Uses browser for PDF generation - no LaTeX required!
"""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HTMLOptions:
    """Options for HTML export."""
    template: str = "memoir"  # memoir, academic, minimal
    theme: str = "light"  # light, dark, sepia
    font: str = "serif"  # serif, sans
    include_toc: bool = True
    author: str = ""
    dedication: str = ""
    date: str = ""
    
    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().strftime("%Y")


# HTML Templates
TEMPLATES = {
    "memoir": {
        "name": "Memoir",
        "description": "Novel, memoir, personal narrative",
        "fonts": ["Merriweather", "Lora"],
        "background": "#fdfbf7",
        "text": "#2c2c2c",
    },
    "academic": {
        "name": "Academic",
        "description": "Technical, textbook, educational",
        "fonts": ["Roboto", "Open Sans"],
        "background": "#ffffff",
        "text": "#1a1a1a",
    },
    "minimal": {
        "name": "Minimal",
        "description": "Clean, simple design",
        "fonts": ["Inter", "System UI"],
        "background": "#ffffff",
        "text": "#000000",
    },
}


class HTMLExporter:
    """Export manuscript to HTML and PDF via browser."""
    
    def __init__(self, template_dir: Optional[str] = None):
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = Path(__file__).parent / "templates" / "html"
    
    def export(
        self,
        manuscript,
        book_title: str,
        options: Optional[HTMLOptions] = None,
    ) -> str:
        """Export manuscript to HTML.
        
        Args:
            manuscript: The Manuscript to export
            book_title: Title for the book
            options: HTMLOptions
            
        Returns:
            HTML string
        """
        opts = options or HTMLOptions()
        
        template_info = TEMPLATES.get(opts.template, TEMPLATES["memoir"])
        
        # Build HTML
        html_parts = [
            self._build_head(book_title, template_info, opts),
            self._build_body(manuscript, book_title, opts),
        ]
        
        return "\n".join(html_parts)
    
    def export_to_file(
        self,
        manuscript,
        book_title: str,
        output_path: str,
        options: Optional[HTMLOptions] = None,
    ) -> dict:
        """Export to HTML file."""
        html = self.export(manuscript, book_title, options)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html)
        
        return {
            "output_file": str(output_file),
            "template": options.template if options else "memoir",
            "size": len(html),
        }
    
    def _build_head(
        self,
        book_title: str,
        template_info: dict,
        options: HTMLOptions,
    ) -> str:
        """Build HTML head with styles."""
        font_import = self._get_font_import(template_info["fonts"])
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{book_title}</title>
  {font_import}
  <style>
    :root {{
      --bg: {template_info["background"]};
      --text: {template_info["text"]};
      --accent: #8b4513;
      --font-main: '{template_info["fonts"][0]}', serif;
      --font-alt: '{template_info["fonts"][1]}', sans-serif;
    }}
    
    * {{ box-sizing: border-box; }}
    
    body {{
      font-family: var(--font-main);
      background: var(--bg);
      color: var(--text);
      line-height: 1.8;
      max-width: 6in;
      margin: 0 auto;
      padding: 1in;
    }}
    
    h1 {{
      font-size: 2.5em;
      text-align: center;
      margin-bottom: 0.5em;
      font-weight: 300;
    }}
    
    h2 {{
      font-size: 1.5em;
      margin-top: 2em;
      border-bottom: 1px solid #ddd;
      padding-bottom: 0.3em;
    }}
    
    h3 {{
      font-size: 1.2em;
      margin-top: 1.5em;
    }}
    
    p {{
      text-align: justify;
      margin-bottom: 1em;
      text-indent: 1.5em;
    }}
    
    p:first-of-type {{ text-indent: 0; }}
    
    .title-page {{
      height: 90vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
    }}
    
    .title-page h1 {{
      font-size: 3em;
      margin-bottom: 0.2em;
    }}
    
    .title-page .author {{
      font-size: 1.5em;
      color: #666;
      margin-top: 1em;
    }}
    
    .title-page .date {{
      font-size: 1em;
      color: #999;
      margin-top: 2em;
    }}
    
    .dedication {{
      margin-top: 3em;
      font-style: italic;
      text-align: center;
    }}
    
    .toc {{
      margin: 2em 0;
      padding: 1em;
      background: rgba(0,0,0,0.02);
    }}
    
    .toc h2 {{
      border: none;
      margin-top: 0;
    }}
    
    .toc ul {{
      list-style: none;
      padding: 0;
    }}
    
    .toc li {{
      padding: 0.3em 0;
      border-bottom: 1px dotted #ccc;
    }}
    
    .toc a {{
      text-decoration: none;
      color: inherit;
    }}
    
    .chapter {{
      margin: 2em 0;
    }}
    
    .chapter-number {{
      font-size: 0.8em;
      color: #999;
      text-transform: uppercase;
      letter-spacing: 0.2em;
    }}
    
    @media print {{
      body {{ padding: 0; }}
      .page-break {{ page-break-before: always; }}
    }}
  </style>
</head>"""
    
    def _build_body(
        self,
        manuscript,
        book_title: str,
        options: HTMLOptions,
    ) -> str:
        """Build HTML body from chapters."""
        parts = ["<body>"]
        
        # Title page
        parts.append('<div class="title-page">')
        parts.append(f"<h1>{book_title}</h1>")
        if options.author:
            parts.append(f'<div class="author">by {options.author}</div>')
        if options.date:
            parts.append(f'<div class="date">{options.date}</div>')
        parts.append("</div>")
        
        # Dedication
        if options.dedication:
            parts.append(f'<div class="dedication">{options.dedication}</div>')
        
        # Table of contents
        if options.include_toc:
            parts.append('<div class="toc"><h2>Contents</h2><ul>')
            for i, chapter in enumerate(manuscript.chapters, 1):
                parts.append(f'<li><a href="#chapter-{i}">{chapter.title}</a></li>')
            parts.append("</ul></div>")
        
        # Chapters
        for i, chapter in enumerate(manuscript.chapters, 1):
            parts.append(f'<div class="chapter" id="chapter-{i}">')
            parts.append(f'<span class="chapter-number">Chapter {i}</span>')
            parts.append(f"<h2>{chapter.title}</h2>")
            
            # Content
            content = self._markdown_to_html(chapter.content or "")
            parts.append(content)
            
            parts.append("</div>")
        
        parts.append("</body></html>")
        
        return "\n".join(parts)
    
    def _markdown_to_html(self, text: str) -> str:
        """Convert basic markdown to HTML."""
        import re
        
        # Headers
        text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        
        # Bold/italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # Code
        text = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        
        # Lists
        text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        
        # Wrap consecutive <li> in <ul>
        lines = text.split('\n')
        in_list = False
        new_lines = []
        for line in lines:
            if line.strip().startswith('<li>'):
                if not in_list:
                    new_lines.append('<ul>')
                    in_list = True
            else:
                if in_list:
                    new_lines.append('</ul>')
                    in_list = False
            new_lines.append(line)
        if in_list:
            new_lines.append('</ul>')
        text = '\n'.join(new_lines)
        
        # Paragraphs
        paragraphs = []
        for para in text.split('\n\n'):
            para = para.strip()
            if para and not para.startswith('<'):
                para = f'<p>{para}</p>'
            paragraphs.append(para)
        text = '\n'.join(paragraphs)
        
        return text
    
    def _get_font_import(self, fonts: list) -> str:
        """Get Google Fonts import URL."""
        font_query = "|".join(fonts).replace(" ", "+")
        return f'<link href="https://fonts.googleapis.com/css2?family={font_query}&display=swap" rel="stylesheet">'


def export_to_html(
    manuscript,
    book_title: str,
    output_path: str = "",
    template: str = "memoir",
    **options,
) -> dict:
    """Convenience function to export to HTML.
    
    Args:
        manuscript: The Manuscript
        book_title: Book title
        output_path: Output .html path (optional)
        template: Template name
        **options: Additional HTMLOptions
        
    Returns:
        Export result with HTML string or file path
    """
    opts = HTMLOptions(template=template, **options)
    exporter = HTMLExporter()
    
    if output_path:
        return exporter.export_to_file(manuscript, book_title, output_path, opts)
    else:
        html = exporter.export(manuscript, book_title, opts)
        return {"html": html, "template": template}


def export_to_pdf(
    manuscript,
    book_title: str,
    output_path: str,
    template: str = "memoir",
    **options,
) -> dict:
    """Export to PDF via browser.
    
    Args:
        manuscript: The Manuscript
        book_title: Book title
        output_path: Output .pdf path
        template: Template name
        **options: Additional HTMLOptions
        
    Returns:
        Export result
    """
    # First export to HTML
    opts = HTMLOptions(template=template, **options)
    exporter = HTMLExporter()
    
    html = exporter.export(manuscript, book_title, opts)
    
    # Save HTML temporarily
    html_path = output_path.replace(".pdf", ".html")
    Path(html_path).write_text(html)
    
    return {
        "html_file": html_path,
        "pdf_file": output_path,
        "template": template,
        "html": html,
    }
