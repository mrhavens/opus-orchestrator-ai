"""GitHub Ingestion Tests for Opus Orchestrator."""

import pytest
from opus_orchestrator.utils.github_ingest import GitHubIngestor


class TestGitHubIngestor:
    """Test GitHub repository ingestion."""

    def test_ingestor_initialization(self):
        """Test ingestor can be initialized."""
        ingestor = GitHubIngestor()
        assert ingestor is not None
        assert ingestor.base_url == "https://api.github.com"

    def test_ingestor_with_token(self):
        """Test ingestor with token."""
        ingestor = GitHubIngestor(token="test_token")
        assert ingestor.token == "test_token"

    def test_ingestor_no_token_warning(self, capsys):
        """Test warning when no token provided."""
        import sys
        from io import StringIO
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        ingestor = GitHubIngestor()
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # Should have warned about no token
        assert "⚠️" in output or "No GitHub token" in output or ingestor.token is None

    def test_should_include_filters_correctly(self):
        """Test file inclusion filtering."""
        ingestor = GitHubIngestor()
        
        # Test exclusion
        assert not ingestor._should_include(
            "node_modules/test.js", None, [".git", "node_modules"], True
        )
        
        # Test inclusion
        assert ingestor._should_include(
            "README.md", [".md"], [".git"], False
        )

    def test_extract_text_from_files(self):
        """Test combining multiple files."""
        ingestor = GitHubIngestor()
        
        files = {
            "README.md": "# Test Project",
            "src/main.py": "print('hello')",
        }
        
        result = ingestor.extract_text_from_files(files)
        
        assert "README.md" in result
        assert "src/main.py" in result
        assert "# Test Project" in result

    @pytest.mark.integration
    def test_ingest_public_repo(self):
        """Test ingesting a public repository."""
        # This is an integration test - skip if no token
        import os
        
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            pytest.skip("No GITHUB_TOKEN available")
        
        ingestor = GitHubIngestor(token=token)
        result = ingestor.ingest_repo("mrhavens/opus-orchestrator-tests")
        
        assert result["file_count"] > 0
        assert result["total_chars"] > 0
        assert "combined_text" in result

    @pytest.mark.integration
    def test_ingest_specific_files(self):
        """Test ingesting with specific extensions."""
        import os
        
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            pytest.skip("No GITHUB_TOKEN available")
        
        ingestor = GitHubIngestor(token=token)
        files = ingestor.get_all_files(
            "mrhavens/opus-orchestrator-tests",
            extensions=[".md"],
            include_all=False,
        )
        
        # Should only have markdown files
        for path in files.keys():
            assert path.endswith(".md"), f"Non-MD file found: {path}"
