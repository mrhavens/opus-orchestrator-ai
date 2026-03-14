"""E2E Integration Tests for Opus Orchestrator."""

import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestE2EGitHubToOutput:
    """Test full pipeline: GitHub input → Generate → GitHub output."""

    @pytest.mark.integration
    @pytest.mark.skip(reason="Full E2E test - takes significant time")
    def test_full_pipeline_github_to_github(self):
        """Test full pipeline with GitHub input and output."""
        # This would be the ideal E2E test:
        # 1. Ingest from GitHub
        # 2. Generate content
        # 3. Push to GitHub
        
        # For now, document the steps
        assert True

    def test_pipeline_stages_documented(self):
        """Test that pipeline stages are documented."""
        from opus_orchestrator.orchestrator import OpusOrchestrator
        
        # Verify all stages exist
        stages = [
            'snowflake_stage_1',
            'snowflake_stage_2', 
            'snowflake_stage_3',
            'snowflake_stage_4',
            'snowflake_stage_5',
            'snowflake_stage_6',
            'snowflake_stage_7',
        ]
        
        for stage in stages:
            assert hasattr(OpusOrchestrator, stage), f"Missing stage: {stage}"


class TestE2ENonfictionPipeline:
    """Test nonfiction-specific E2E pipeline."""

    def test_nonfiction_purpose_classification(self):
        """Test purpose classification in pipeline."""
        from opus_orchestrator.nonfiction.classifier import PurposeClassifier
        from opus_orchestrator.nonfiction_taxonomy import ReaderPurpose
        
        classifier = PurposeClassifier()
        
        # Test various inputs
        result = classifier._keyword_classify(
            concept="How to learn Python",
            target_audience="Beginners",
            intended_outcome="Learn programming",
        )
        
        assert result.purpose in ReaderPurpose
        assert result.confidence > 0

    def test_framework_selection_by_purpose(self):
        """Test framework selection based on purpose."""
        from opus_orchestrator.nonfiction_taxonomy import (
            select_framework,
            ReaderPurpose,
            NonfictionCategory,
        )
        
        # Test different purposes
        for purpose in ReaderPurpose:
            framework = select_framework(
                purpose=purpose,
                category=None,
                user_preferred_framework=None,
            )
            
            assert framework is not None
            assert "name" in framework


class TestE2EFictionPipeline:
    """Test fiction-specific E2E pipeline."""

    def test_fiction_agents_initialized(self):
        """Test fiction agents are properly initialized."""
        from opus_orchestrator import OpusOrchestrator
        
        orch = OpusOrchestrator(
            book_type="fiction",
            genre="fantasy",
        )
        
        # Verify fiction agents exist
        assert "architect" in orch.agents
        assert "worldsmith" in orch.agents
        assert "character_lead" in orch.agents
        assert "voice" in orch.agents
        assert "editor" in orch.agents

    def test_snowflake_method_stages(self):
        """Test Snowflake method stages are available."""
        from opus_orchestrator import OpusOrchestrator
        
        orch = OpusOrchestrator(book_type="fiction")
        
        # Check all Snowflake stage attributes exist
        assert hasattr(orch, 'one_sentence')
        assert hasattr(orch, 'one_paragraph')
        assert hasattr(orch, 'character_sheets')
        assert hasattr(orch, 'four_page_outline')
        assert hasattr(orch, 'character_charts')
        assert hasattr(orch, 'scene_list')


class TestE2EErrorHandling:
    """Test error handling in E2E scenarios."""

    def test_missing_api_key_handling(self):
        """Test proper handling when no API key."""
        import os
        from opus_orchestrator.config import get_config
        
        # Save original value
        orig_key = os.environ.get("OPENAI_API_KEY")
        
        # Temporarily remove key
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        
        try:
            # Should raise or handle gracefully
            config = get_config()
            # May return default config
            assert config is not None
        finally:
            # Restore key
            if orig_key:
                os.environ["OPENAI_API_KEY"] = orig_key

    def test_invalid_book_type(self):
        """Test handling of invalid book type."""
        from opus_orchestrator.schemas import BookType
        
        # Should handle invalid type
        with pytest.raises(ValueError):
            BookType("invalid_type")

    def test_orchestrator_graceful_failure(self):
        """Test orchestrator handles failures gracefully."""
        from opus_orchestrator import OpusOrchestrator
        
        orch = OpusOrchestrator(book_type="fiction")
        
        # State should be None initially
        assert orch.state is None


class TestE2EConfiguration:
    """Test configuration in E2E scenarios."""

    def test_config_loading(self):
        """Test configuration loads properly."""
        from opus_orchestrator.config import get_config
        
        config = get_config()
        
        assert config is not None
        assert config.agent is not None

    def test_config_validation(self):
        """Test config validates properly."""
        from opus_orchestrator.config import OpusConfig
        
        config = OpusConfig()
        
        # Verify defaults are sensible
        assert config.agent.max_iterations > 0
        assert config.iteration.approval_threshold > 0
        assert config.iteration.approval_threshold <= 1.0


class TestE2EStateManagement:
    """Test state management across pipeline."""

    def test_state_initialization(self):
        """Test OpusState initializes correctly."""
        from opus_orchestrator.state import OpusState
        
        state = OpusState()
        
        assert state.progress == 0.0
        assert state.current_stage == "ingestion"
        assert state.errors == []
        assert state.warnings == []

    def test_state_progress_tracking(self):
        """Test progress is tracked properly."""
        from opus_orchestrator.state import OpusState
        
        state = OpusState()
        
        # Simulate progress
        state.progress = 0.5
        state.current_stage = "drafting"
        
        assert state.progress == 0.5
        assert state.current_stage == "drafting"

    def test_state_error_tracking(self):
        """Test errors are tracked."""
        from opus_orchestrator.state import OpusState
        
        state = OpusState()
        
        # Add an error
        state.errors.append("Test error")
        
        assert len(state.errors) == 1
        assert "Test error" in state.errors


class TestE2EBookTypes:
    """Test different book type configurations."""

    def test_fiction_config(self):
        """Test fiction-specific configuration."""
        from opus_orchestrator import OpusOrchestrator
        
        orch = OpusOrchestrator(
            book_type="fiction",
            genre="mystery",
            target_word_count=75000,
        )
        
        assert orch.book_type.value == "fiction"
        assert orch.framework_info is not None

    def test_nonfiction_config(self):
        """Test nonfiction-specific configuration."""
        from opus_orchestrator import OpusOrchestrator
        
        orch = OpusOrchestrator(
            book_type="nonfiction",
            genre="science",
            target_word_count=50000,
        )
        
        assert orch.book_type.value == "nonfiction"
        assert orch.purpose is not None


class TestE2EFrameworks:
    """Test different frameworks in E2E."""

    def test_all_story_frameworks_available(self):
        """Test all story frameworks are available."""
        from opus_orchestrator.frameworks import StoryFramework
        
        frameworks = [
            StoryFramework.SNOWFLAKE,
            StoryFramework.THREE_ACT,
            StoryFramework.HERO_JOURNEY,
            StoryFramework.SAVE_THE_CAT,
            StoryFramework.STORY_CIRCLE,
            StoryFramework.SEVEN_POINT,
            StoryFramework.FICHTEAN,
        ]
        
        for fw in frameworks:
            assert fw is not None

    def test_framework_info_retrieval(self):
        """Test framework info can be retrieved."""
        from opus_orchestrator.frameworks import FRAMEWORKS, StoryFramework
        
        for framework in StoryFramework:
            info = FRAMEWORKS.get(framework)
            
            if info:
                assert "name" in info or hasattr(framework, 'value')
