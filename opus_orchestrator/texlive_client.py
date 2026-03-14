"""TeX Live API Client for Opus Orchestrator.

Compiles LaTeX via remote TeX Live API service.
"""

import json
import base64
from typing import Optional, Dict, Any
from pathlib import Path


class TeXLiveClient:
    """Client for TeX Live API service."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        """Initialize TeX Live client.
        
        Args:
            base_url: Base URL of TeX Live API service
        """
        self.base_url = base_url.rstrip("/")
    
    def compile(
        self,
        tex_content: str,
        engine: str = "xelatex",
        timeout: int = 120,
    ) -> Dict[str, Any]:
        """Compile LaTeX via API.
        
        Args:
            tex_content: LaTeX source code
            engine: LaTeX engine (xelatex, pdflatex, lualatex)
            timeout: Compilation timeout in seconds
            
        Returns:
            Compilation result with PDF data
        """
        import requests
        
        response = requests.post(
            f"{self.base_url}/compile",
            json={
                "tex": tex_content,
                "engine": engine,
                "timeout": timeout,
            },
            timeout=timeout + 10,
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"TeX Live API error: {response.text}")
        
        result = response.json()
        
        if result.get("error"):
            raise RuntimeError(f"LaTeX compilation failed: {result['error']}")
        
        return result
    
    def compile_file(
        self,
        tex_path: str,
        engine: str = "xelatex",
    ) -> bytes:
        """Compile LaTeX file via API.
        
        Args:
            tex_path: Path to .tex file
            engine: LaTeX engine
            
        Returns:
            Compiled PDF as bytes
        """
        tex_content = Path(tex_path).read_text()
        result = self.compile(tex_content, engine)
        
        # Decode PDF from base64
        pdf_data = base64.b64decode(result["pdf"])
        return pdf_data


def compile_via_texlive(
    tex_content: str,
    base_url: str = "http://localhost:8080",
    engine: str = "xelatex",
) -> bytes:
    """Convenience function to compile LaTeX via TeX Live API.
    
    Args:
        tex_content: LaTeX source
        base_url: TeX Live API URL
        engine: LaTeX engine
        
    Returns:
        Compiled PDF bytes
    """
    client = TeXLiveClient(base_url)
    result = client.compile(tex_content, engine)
    return base64.b64decode(result["pdf"])
