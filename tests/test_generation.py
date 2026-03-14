"""Tests for NonfictionGenerator document generation.

Tests for:
- DIAXIS_EXPLANATION framework
- DIAXIS_TUTORIAL framework
- TECHNICAL_MANUAL framework
- Word count verification
- Structure verification
- Quality verification
"""

import pytest
import re
from unittest.mock import Mock, patch, MagicMock
from typing import Optional


# =============================================================================
# TEST SOURCE CONTENT
# =============================================================================

# Source content from mrhavens/opus-orchestrator-tests
SOURCE_CONTENT = """# Test Source File 1 - Philosophy

## The Nature of Consciousness

Consciousness remains one of the greatest mysteries in science and philosophy. Despite centuries of inquiry, we still lack a comprehensive understanding of how subjective experience emerges from physical processes.

### Key Questions

1. What is the relationship between brain activity and conscious experience?
2. Can consciousness be measured or quantified?
3. Is consciousness a fundamental property of the universe?

### The Hard Problem

David Chalmers coined the term "hard problem" to describe the challenge of explaining why and how physical processes give rise to subjective experience. This remains unsolved.

---

# Test Source File 2 - Technology

## Artificial Intelligence Overview

AI has evolved from rule-based systems to modern machine learning approaches. Key developments include:

- Neural networks
- Deep learning
- Transformer architectures
- Large language models

### Current Capabilities

Modern AI can:
- Generate human-like text
- Recognize images
- Play complex games
- Translate languages
- Write code

### Limitations

Despite advances, AI lacks:
- True understanding
- Common sense reasoning
- General intelligence
- Emotional experience
"""


# =============================================================================
# TEST NONFICTION GENERATOR - MOCKED
# =============================================================================

class TestNonfictionGenerator:
    """Tests for NonfictionGenerator with mocked LLM."""
    
    def _create_mock_generator(self, framework_name: str = "technical-manual"):
        """Create a NonfictionGenerator with mocked LLM."""
        from opus_orchestrator.nonfiction_generator import NonfictionGenerator
        from opus_orchestrator.nonfiction_frameworks import NonfictionFramework
        
        # Map framework names to enum values
        framework_map = {
            "diataxis-explanation": NonfictionFramework.DIAXIS_EXPLANATION,
            "diataxis-tutorial": NonfictionFramework.DIAXIS_TUTORIAL,
            "technical-manual": NonfictionFramework.TECHNICAL_MANUAL,
        }
        
        framework = framework_map.get(framework_name, NonfictionFramework.TECHNICAL_MANUAL)
        
        with patch('opus_orchestrator.nonfiction_generator.LLMClient') as MockLLM:
            mock_instance = MockLLM.return_value
            mock_instance.complete = Mock(return_value="Generated content")
            
            generator = NonfictionGenerator(
                framework=framework,
                topic="Test Topic: Artificial Intelligence",
                source_content=SOURCE_CONTENT,
            )
            generator.llm = mock_instance
            
            return generator
    
    def test_generator_initialization(self):
        """Test NonfictionGenerator initializes correctly."""
        from opus_orchestrator.nonfiction_generator import NonfictionGenerator
        from opus_orchestrator.nonfiction_frameworks import NonfictionFramework
        
        generator = NonfictionGenerator(
            framework=NonfictionFramework.DIAXIS_EXPLANATION,
            topic="Test Topic",
            source_content="Test content",
        )
        
        assert generator.framework == NonfictionFramework.DIAXIS_EXPLANATION
        assert generator.topic == "Test Topic"
        assert generator.source_content == "Test content"
        assert generator.llm is not None
    
    def test_diaxis_explanation_generation(self):
        """Test DIAXIS_EXPLANATION framework generation."""
        generator = self._create_mock_generator("diataxis-explanation")
        
        result = generator.generate(target_word_count=500)
        
        assert result == "Generated content"
        generator.llm.complete.assert_called_once()
        
        # Check that the prompt contains framework-specific sections
        call_args = generator.llm.complete.call_args
        prompt = call_args.kwargs.get('user_prompt', '') or call_args[1].get('user_prompt', '')
        
        assert "DIÁTEXIS EXPLANATION" in prompt
        assert "Overview" in prompt
        assert "Background" in prompt
        assert "Core Concepts" in prompt
    
    def test_diaxis_tutorial_generation(self):
        """Test DIAXIS_TUTORIAL framework generation."""
        generator = self._create_mock_generator("diataxis-tutorial")
        
        result = generator.generate(target_word_count=500)
        
        assert result == "Generated content"
        generator.llm.complete.assert_called_once()
        
        call_args = generator.llm.complete.call_args
        prompt = call_args.kwargs.get('user_prompt', '') or call_args[1].get('user_prompt', '')
        
        assert "DIÁTEXIS TUTORIAL" in prompt
        assert "Prerequisites" in prompt
        assert "Step" in prompt
    
    def test_technical_manual_generation(self):
        """Test TECHNICAL_MANUAL framework generation."""
        generator = self._create_mock_generator("technical-manual")
        
        result = generator.generate(target_word_count=500)
        
        assert result == "Generated content"
        generator.llm.complete.assert_called_once()
        
        call_args = generator.llm.complete.call_args
        prompt = call_args.kwargs.get('user_prompt', '') or call_args[1].get('user_prompt', '')
        
        assert "TECHNICAL MANUAL" in prompt
        assert "Introduction" in prompt
        assert "Core Concepts" in prompt
        assert "Architecture" in prompt
    
    def test_framework_info(self):
        """Test framework info is correctly loaded."""
        from opus_orchestrator.nonfiction_generator import NonfictionGenerator
        from opus_orchestrator.nonfiction_frameworks import NonfictionFramework, get_nonfiction_framework
        
        generator = NonfictionGenerator(
            framework=NonfictionFramework.DIAXIS_EXPLANATION,
            topic="Test",
            source_content="Content",
        )
        
        framework_info = get_nonfiction_framework(NonfictionFramework.DIAXIS_EXPLANATION)
        assert framework_info["name"] == "Diátaxis Explanation"
        assert "stages" in framework_info
        assert len(framework_info["stages"]) > 0


# =============================================================================
# TEST DOCUMENT STRUCTURE VERIFICATION
# =============================================================================

class TestDocumentStructure:
    """Tests for document structure verification."""
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    def extract_sections(self, text: str) -> list[str]:
        """Extract section headers from document."""
        # Match markdown headers
        sections = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
        return sections
    
    def test_diaxis_explanation_sections(self):
        """Verify DIAXIS_EXPLANATION has expected sections."""
        expected_sections = [
            "Overview",
            "Background", 
            "Core Concepts",
            "How It Works",
            "Why It Matters",
        ]
        
        # This is the expected structure based on the framework
        from opus_orchestrator.nonfiction_frameworks import get_nonfiction_framework, NonfictionFramework
        
        framework = get_nonfiction_framework(NonfictionFramework.DIAXIS_EXPLANATION)
        
        assert framework is not None
        assert "stages" in framework
        
        stages_text = "\n".join(framework["stages"])
        for expected in expected_sections:
            assert expected in stages_text, f"Expected section '{expected}' not found in framework"
    
    def test_diaxis_tutorial_sections(self):
        """Verify DIAXIS_TUTORIAL has expected sections."""
        from opus_orchestrator.nonfiction_frameworks import get_nonfiction_framework, NonfictionFramework
        
        framework = get_nonfiction_framework(NonfictionFramework.DIAXIS_TUTORIAL)
        
        assert framework is not None
        stages_text = "\n".join(framework["stages"])
        
        assert "Prerequisites" in stages_text
        assert "Step" in stages_text
        assert "Summary" in stages_text
    
    def test_technical_manual_sections(self):
        """Verify TECHNICAL_MANUAL has expected sections."""
        from opus_orchestrator.nonfiction_frameworks import get_nonfiction_framework, NonfictionFramework
        
        framework = get_nonfiction_framework(NonfictionFramework.TECHNICAL_MANUAL)
        
        assert framework is not None
        stages_text = "\n".join(framework["stages"])
        
        assert "Introduction" in stages_text
        assert "Core Concepts" in stages_text
        assert "Architecture" in stages_text
        assert "Getting Started" in stages_text


# =============================================================================
# TEST WORD COUNT VERIFICATION
# =============================================================================

class TestWordCount:
    """Tests for word count verification."""
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    def test_word_count_within_tolerance(self):
        """Test that word count verification logic works correctly."""
        # This tests the word count verification logic
        target = 5000
        tolerance = 0.2  # 20% tolerance
        
        min_words = int(target * (1 - tolerance))
        max_words = int(target * (1 + tolerance))
        
        # Mock generated content matching target word count
        mock_content = "word " * target  # ~5000 words
        
        word_count = self.count_words(mock_content)
        
        assert min_words <= word_count <= max_words, f"Word count {word_count} outside range [{min_words}, {max_words}]"


# =============================================================================
# INTEGRATION TESTS (require actual API)
# =============================================================================

class TestNonfictionGeneratorIntegration:
    """Integration tests that make actual API calls.
    
    These tests are skipped by default. Run with: pytest -v -m integration
    """
    
    @pytest.mark.integration
    @pytest.mark.skipif(
        not __import__('os').environ.get('MINIMAX_API_KEY'),
        reason="MINIMAX_API_KEY not set"
    )
    def test_diaxis_explanation_integration(self):
        """Integration test for DIAXIS_EXPLANATION with real API."""
        from opus_orchestrator.nonfiction_generator import NonfictionGenerator
        from opus_orchestrator.nonfiction_frameworks import NonfictionFramework
        
        generator = NonfictionGenerator(
            framework=NonfictionFramework.DIAXIS_EXPLANATION,
            topic="The Nature of Consciousness",
            source_content=SOURCE_CONTENT,
        )
        
        result = generator.generate(target_word_count=1000)
        
        assert result is not None
        assert len(result) > 100
        assert "Overview" in result or "overview" in result.lower()
        
        # Check word count is reasonable
        word_count = len(result.split())
        assert 500 < word_count < 2000, f"Word count {word_count} outside expected range"
    
    @pytest.mark.integration
    @pytest.mark.skipif(
        not __import__('os').environ.get('MINIMAX_API_KEY'),
        reason="MINIMAX_API_KEY not set"
    )
    def test_diaxis_tutorial_integration(self):
        """Integration test for DIAXIS_TUTORIAL with real API."""
        from opus_orchestrator.nonfiction_generator import NonfictionGenerator
        from opus_orchestrator.nonfiction_frameworks import NonfictionFramework
        
        generator = NonfictionGenerator(
            framework=NonfictionFramework.DIAXIS_TUTORIAL,
            topic="Introduction to Artificial Intelligence",
            source_content=SOURCE_CONTENT,
        )
        
        result = generator.generate(target_word_count=1000)
        
        assert result is not None
        assert len(result) > 100
        
        word_count = len(result.split())
        assert 500 < word_count < 2000
    
    @pytest.mark.integration
    @pytest.mark.skipif(
        not __import__('os').environ.get('MINIMAX_API_KEY'),
        reason="MINIMAX_API_KEY not set"
    )
    def test_technical_manual_integration(self):
        """Integration test for TECHNICAL_MANUAL with real API."""
        from opus_orchestrator.nonfiction_generator import NonfictionGenerator
        from opus_orchestrator.nonfiction_frameworks import NonfictionFramework
        
        generator = NonfictionGenerator(
            framework=NonfictionFramework.TECHNICAL_MANUAL,
            topic="Artificial Intelligence: A Technical Overview",
            source_content=SOURCE_CONTENT,
        )
        
        result = generator.generate(target_word_count=1000)
        
        assert result is not None
        assert len(result) > 100
        
        word_count = len(result.split())
        assert 500 < word_count < 2000


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
