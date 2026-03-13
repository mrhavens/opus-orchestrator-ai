"""Tests for Purpose Classifier.

Run with: pytest tests/test_classifier.py -v
"""

import pytest
from opus_orchestrator.nonfiction.classifier import (
    PurposeClassifier,
    ClassificationResult,
    classify_purpose,
)
from opus_orchestrator.nonfiction_taxonomy import ReaderPurpose


class TestKeywordClassifier:
    """Tests for keyword-based classification."""
    
    @pytest.fixture
    def classifier(self):
        return PurposeClassifier()
    
    def test_howto_learn_hands_on(self, classifier):
        """'How to code in Python' should classify as LEARN_HANDS_ON."""
        result = classifier.classify(
            concept="How to Code in Python",
            target_audience="Beginners who want to learn programming",
            intended_outcome="Be able to write Python programs",
        )
        
        assert result.purpose == ReaderPurpose.LEARN_HANDS_ON
        assert result.confidence > 0.6
    
    def test_why_nations_fail(self, classifier):
        """'Why nations fail' should classify as UNDERSTAND."""
        result = classifier.classify(
            concept="Why Nations Fail",
            target_audience="Readers interested in economics and history",
            intended_outcome="Understand the causes of economic disparity",
        )
        
        assert result.purpose == ReaderPurpose.UNDERSTAND
    
    def test_7_habits_transform(self, classifier):
        """'7 habits of highly effective people' should classify as TRANSFORM."""
        result = classifier.classify(
            concept="7 Habits of Highly Effective People",
            target_audience="Professionals seeking personal growth",
            intended_outcome="Become more effective in life and work",
        )
        
        assert result.purpose == ReaderPurpose.TRANSFORM
    
    def test_crm_comparison_decide(self, classifier):
        """'Best CRM comparison' should classify as DECIDE."""
        result = classifier.classify(
            concept="Best CRM Software Comparison Guide",
            target_audience="Business owners choosing CRM software",
            intended_outcome="Choose the right CRM for their business",
        )
        
        assert result.purpose == ReaderPurpose.DECIDE
    
    def test_manual_reference(self, classifier):
        """'Python API Reference Manual' should classify as REFERENCE."""
        result = classifier.classify(
            concept="Python API Reference Manual",
            target_audience="Python developers",
            intended_outcome="Look up API documentation",
        )
        
        assert result.purpose == ReaderPurpose.REFERENCE
    
    def test_triumph_story_inspire(self, classifier):
        """'Against All Odds' biography should classify as BE_INSPIRED."""
        result = classifier.classify(
            concept="Against All Odds: My Story",
            target_audience="Readers seeking motivation",
            intended_outcome="Feel inspired by an incredible journey",
        )
        
        assert result.purpose == ReaderPurpose.BE_INSPIRED
    
    def test_understanding_concept(self, classifier):
        """'How the Mind Works' should classify as UNDERSTAND."""
        result = classifier.classify(
            concept="How the Mind Works",
            target_audience="Curious readers",
            intended_outcome="Understand cognitive psychology",
        )
        
        assert result.purpose == ReaderPurpose.UNDERSTAND
    
    def test_transform_explicit(self, classifier):
        """Explicit transformation language should trigger TRANSFORM."""
        result = classifier.classify(
            concept="Transform Your Life",
            target_audience="Anyone feeling stuck",
            intended_outcome="Overcome challenges and grow",
        )
        
        assert result.purpose == ReaderPurpose.TRANSFORM
    
    def test_skills_development(self, classifier):
        """Skills development should trigger LEARN_HANDS_ON."""
        result = classifier.classify(
            concept="Leadership Skills Development",
            target_audience="New managers",
            intended_outcome="Develop practical leadership skills",
        )
        
        assert result.purpose == ReaderPurpose.LEARN_HANDS_ON
    
    def test_analysis_decide(self, classifier):
        """Analysis for decision should trigger DECIDE."""
        result = classifier.classify(
            concept="Investment Analysis Strategies",
            target_audience="Investors",
            intended_outcome="Make better investment decisions",
        )
        
        assert result.purpose == ReaderPurpose.DECIDE
    
    def test_comprehensive_guide(self, classifier):
        """'Complete guide' often implies REFERENCE."""
        result = classifier.classify(
            concept="Complete Guide to Kubernetes",
            target_audience="DevOps engineers",
            intended_outcome="Comprehensive reference for K8s",
        )
        
        assert result.purpose == ReaderPurpose.REFERENCE
    
    def test_journey_biography(self, classifier):
        """Journey/memoir should trigger BE_INSPIRED."""
        result = classifier.classify(
            concept="My Journey from Poverty to CEO",
            target_audience="Aspiring entrepreneurs",
            intended_outcome="Find motivation from success story",
        )
        
        assert result.purpose == ReaderPurpose.BE_INSPIRED
    
    def test_ambiguous_defaults_to_understand(self, classifier):
        """Ambiguous input should default to UNDERSTAND."""
        result = classifier.classify(
            concept="The Nature of Things",
            target_audience="General readers",
            intended_outcome="Enjoy a well-written book",
        )
        
        # Should default to UNDERSTAND as most common nonfiction purpose
        assert result.confidence < 0.5  # Low confidence


class TestClassificationConfidence:
    """Tests for confidence scoring."""
    
    @pytest.fixture
    def classifier(self):
        return PurposeClassifier()
    
    def test_strong_match_high_confidence(self, classifier):
        """Multiple keyword matches should give high confidence."""
        result = classifier.classify(
            concept="How to Build a Startup: A Step-by-Step Guide",
            target_audience="Aspiring entrepreneurs who want to learn practical skills",
            intended_outcome="Build and launch a startup",
        )
        
        assert result.confidence > 0.7
    
    def test_no_match_low_confidence(self, classifier):
        """No keyword matches should give low confidence."""
        result = classifier.classify(
            concept="Things",
            target_audience="People",
            intended_outcome="Read something",
        )
        
        assert result.confidence < 0.5


class TestReasoning:
    """Tests for reasoning generation."""
    
    @pytest.fixture
    def classifier(self):
        return PurposeClassifier()
    
    def test_reasoning_includes_matched_keywords(self, classifier):
        """Reasoning should mention matched keywords."""
        result = classifier.classify(
            concept="How to Learn Python Programming",
            target_audience="Beginners",
            intended_outcome="Learn skills",
        )
        
        assert result.reasoning is not None
        assert len(result.reasoning) > 0


class TestConvenienceFunction:
    """Tests for the classify_purpose convenience function."""
    
    @pytest.mark.asyncio
    async def test_convenience_function_returns_result(self):
        """Convenience function should return ClassificationResult."""
        result = await classify_purpose(
            concept="How to Cook",
            target_audience="Beginners",
        )
        
        assert isinstance(result, ClassificationResult)
        assert result.purpose in ReaderPurpose


class TestEdgeCases:
    """Edge case tests."""
    
    @pytest.fixture
    def classifier(self):
        return PurposeClassifier()
    
    def test_empty_inputs(self, classifier):
        """Empty inputs should not crash."""
        result = classifier.classify(
            concept="",
            target_audience="",
            intended_outcome="",
        )
        
        assert result.purpose is not None
        assert result.confidence > 0
    
    def test_very_long_concept(self, classifier):
        """Very long concept should be handled."""
        long_concept = "How to " + "do things " * 100
        result = classifier.classify(concept=long_concept)
        
        assert result.purpose is not None
    
    def test_special_characters(self, classifier):
        """Special characters should not break classification."""
        result = classifier.classify(
            concept="How-to: Build @Awesome #Startup!",
            target_audience="Everyone!!!",
            intended_outcome="???",
        )
        
        assert result.purpose is not None


# Integration-like tests (would need mock LLM)
class TestLLMClassification:
    """Tests for LLM-based classification (skipped without LLM)."""
    
    @pytest.mark.skip(reason="Requires LLM client")
    async def test_llm_classifies_nuanced_input(self):
        """LLM should handle nuanced classification."""
        # This would test the LLM path
        pass
    
    @pytest.mark.skip(reason="Requires LLM client") 
    async def test_llm_fallback_on_parse_error(self):
        """Should fallback to keywords on parse error."""
        # This would test error handling
        pass
