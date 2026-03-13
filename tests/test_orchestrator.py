"""Test suite for Opus Orchestrator.

Tests for core functionality - these can run without API keys.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from opus_orchestrator.config import (
    OpusConfig,
    AgentConfig,
    CostConfig,
    IterationConfig,
    load_config_from_env,
)


class TestConfig:
    """Tests for configuration."""
    
    def test_default_config(self):
        """Test default configuration is valid."""
        config = OpusConfig()
        assert config.agent.model is not None
        assert config.agent.temperature == 0.7
        assert config.iteration.max_critic_rounds == 5
    
    def test_cost_config_defaults(self):
        """Test cost config has defaults."""
        cost = CostConfig()
        assert cost.track_usage is True
        assert "gpt-4o" in cost.price_per_million_tokens
    
    def test_iteration_config(self):
        """Test iteration config."""
        iteration = IterationConfig()
        assert iteration.approval_threshold == 0.8
        assert iteration.auto_proceed_threshold == 0.9
        assert iteration.max_critic_rounds >= iteration.min_critic_rounds


class TestSchemas:
    """Tests for Pydantic schemas."""
    
    def test_book_intent_validation(self):
        """Test BookIntent validation."""
        from opus_orchestrator.schemas import BookIntent, BookType
        
        intent = BookIntent(
            book_type=BookType.FICTION,
            genre="fantasy",
            target_audience="young adult",
            intended_outcome="complete novel",
            target_word_count=80000,
        )
        
        assert intent.book_type == BookType.FICTION
        assert intent.target_word_count == 80000
    
    def test_chapter_blueprint(self):
        """Test ChapterBlueprint validation."""
        from opus_orchestrator.schemas import ChapterBlueprint
        
        chapter = ChapterBlueprint(
            chapter_number=1,
            title="The Beginning",
            summary="Our hero starts their journey",
            word_count_target=3000,
        )
        
        assert chapter.chapter_number == 1
        assert chapter.word_count_target == 3000


class TestFrameworks:
    """Tests for story frameworks."""
    
    def test_get_framework_prompt(self):
        """Test framework prompt generation."""
        from opus_orchestrator.frameworks import get_framework_prompt, StoryFramework
        
        # Test all frameworks have prompts
        for framework in StoryFramework:
            prompt = get_framework_prompt(framework)
            assert prompt is not None
            assert len(prompt) > 0
    
    def test_framework_for_genre(self):
        """Test framework suggestions by genre."""
        from opus_orchestrator.frameworks import get_framework_for_genre
        
        # Fantasy should suggest Hero's Journey
        suggestions = get_framework_for_genre("fantasy")
        assert len(suggestions) > 0
        
        # Unknown genre should fallback
        suggestions = get_framework_for_genre("unknown")
        assert len(suggestions) > 0


class TestGitHubIngestor:
    """Tests for GitHub ingestion."""
    
    def test_ingestor_without_token(self):
        """Test GitHubIngestor works without token."""
        from opus_orchestrator.utils.github_ignest import GitHubIngestor
        
        # Should not raise without token
        ingestor = GitHubIngestor(token=None)
        assert ingestor.headers is not None
        assert "Accept" in ingestor.headers
    
    def test_ingestor_with_token(self):
        """Test GitHubIngestor with token."""
        from opus_orchestrator.utils.github_ignest import GitHubIngestor
        
        ingestor = GitHubIngestor(token="test_token")
        assert "Authorization" in ingestor.headers


class TestAgentResponse:
    """Tests for agent responses."""
    
    def test_agent_response_success(self):
        """Test successful agent response."""
        from opus_orchestrator.agents.base import AgentResponse
        
        response = AgentResponse(
            success=True,
            output="Test output",
            metadata={"key": "value"},
        )
        
        assert response.success is True
        assert response.output == "Test output"
        assert response.error is None
    
    def test_agent_response_error(self):
        """Test error agent response."""
        from opus_orchestrator.agents.base import AgentResponse
        
        response = AgentResponse(
            success=False,
            output=None,
            error="Something went wrong",
        )
        
        assert response.success is False
        assert response.error == "Something went wrong"


# Mock tests that require API keys
class TestLLMClient:
    """Tests for LLM client (mocked)."""
    
    @patch('opus_orchestrator.utils.llm.requests.post')
    def test_sync_client_openai(self, mock_post):
        """Test synchronous OpenAI client."""
        from opus_orchestrator.utils.llm import LLMClient
        
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_post.return_value = mock_response
        
        client = LLMClient(
            api_key="test_key",
            provider="openai",
            model="gpt-4o",
        )
        
        result = client.complete(
            system_prompt="System",
            user_prompt="User",
        )
        
        assert result == "Test response"
        mock_post.assert_called_once()


# Integration-like tests (need environment)
class TestIntegration:
    """Integration tests - skip if no API key."""
    
    @pytest.mark.skipif(
        not __import__('os')..environ.get('OPENAI_API_KEY'),
        reason="No API key"
    )
    def test_real_api_call(self):
        """Test actual API call if key exists."""
        from opus_orchestrator.utils.llm import LLMClient
        
        client = LLMClient(provider="openai", model="gpt-4o")
        
        result = client.complete(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'test' if you receive this.",
        )
        
        assert "test" in result.lower()
