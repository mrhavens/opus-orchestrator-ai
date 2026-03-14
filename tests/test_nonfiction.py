"""Comprehensive Tests for Opus Orchestrator.

Tests for:
- Orchestrator
- Nonfiction framework
- Classifier
- Ingestion
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import json


# =============================================================================
# TEST CLASSIFIER
# =============================================================================

class TestPurposeClassifier:
    """Tests for PurposeClassifier."""
    
    def test_keyword_howto(self):
        """Test 'how to' triggers LEARN_HANDS_ON."""
        from opus_orchestrator.nonfiction.classifier import PurposeClassifier
        
        classifier = PurposeClassifier()
        result = classifier._keyword_classify(
            concept="How to Code in Python",
            target_audience="Beginners",
            intended_outcome="Learn programming",
        )
        
        assert result.purpose.value == "learn_hands_on"
        assert result.confidence > 0.5
    
    def test_keyword_transform(self):
        """Test transform keywords."""
        from opus_orchestrator.nonfiction.classifier import PurposeClassifier
        
        classifier = PurposeClassifier()
        result = classifier._keyword_classify(
            concept="Transform Your Life",
            target_audience="Anyone feeling stuck",
            intended_outcome="Overcome challenges",
        )
        
        assert result.purpose.value == "transform"
    
    def test_keyword_decide(self):
        """Test decide keywords."""
        from opus_orchestrator.nonfiction.classifier import PurposeClassifier
        
        classifier = PurposeClassifier()
        result = classifier._keyword_classify(
            concept="Best CRM Comparison",
            target_audience="Business owners",
            intended_outcome="Choose right CRM",
        )
        
        assert result.purpose.value == "decide"


# =============================================================================
# TEST TAXONOMY
# =============================================================================

class TestTaxonomy:
    """Tests for taxonomy and framework selection."""
    
    def test_purpose_structure_matrix(self):
        """Test PURPOSE_STRUCTURE_MATRIX exists."""
        from opus_orchestrator.nonfiction_taxonomy import PURPOSE_STRUCTURE_MATRIX
        
        assert len(PURPOSE_STRUCTURE_MATRIX) > 0
    
    def test_select_framework_learn(self):
        """Test framework selection for learn purpose."""
        from opus_orchestrator.nonfiction_taxonomy import select_framework, ReaderPurpose
        
        framework = select_framework(purpose=ReaderPurpose.LEARN_HANDS_ON)
        
        assert framework is not None
        assert "stages" in framework
    
    def test_select_framework_transform(self):
        """Test framework selection for transform purpose."""
        from opus_orchestrator.nonfiction_taxonomy import select_framework, ReaderPurpose
        
        framework = select_framework(purpose=ReaderPurpose.TRANSFORM)
        
        assert framework is not None
        assert framework.get("purpose") == ReaderPurpose.TRANSFORM


# =============================================================================
# TEST CRITERIA
# =============================================================================

class TestCritiqueCriteria:
    """Tests for purpose-specific critique criteria."""
    
    def test_get_criteria_learn(self):
        """Test criteria for learn purpose."""
        from opus_orchestrator.nonfiction.critique_criteria import get_critique_criteria, ReaderPurpose
        
        criteria = get_critique_criteria(ReaderPurpose.LEARN_HANDS_ON)
        
        assert criteria is not None
        assert len(criteria.criteria) > 0
    
    def test_get_criteria_transform(self):
        """Test criteria for transform purpose."""
        from opus_orchestrator.nonfiction.critique_criteria import get_critique_criteria, ReaderPurpose
        
        criteria = get_critique_criteria(ReaderPurpose.TRANSFORM)
        
        assert criteria is not None
        # Should have emotional honesty as top criterion
        criterion_names = [c.name for c in criteria.criteria]
        assert "Emotional Honesty" in criterion_names


# =============================================================================
# TEST EXPANDED FRAMEWORKS
# =============================================================================

class TestExpandedFrameworks:
    """Tests for expanded framework library."""
    
    def test_framework_count(self):
        """Test we have 35+ frameworks."""
        from opus_orchestrator.nonfiction.expanded_frameworks import get_total_framework_count
        
        count = get_total_framework_count()
        assert count >= 35
    
    def test_business_frameworks(self):
        """Test business frameworks exist."""
        from opus_orchestrator.nonfiction.expanded_frameworks import EXPANDED_FRAMEWORKS
        
        assert "big_idea" in EXPANDED_FRAMEWORKS
        assert "one_thing" in EXPANDED_FRAMEWORKS
    
    def test_creative_frameworks(self):
        """Test creative frameworks exist."""
        from opus_orchestrator.nonfiction.creative_frameworks import CREATIVE_FRAMEWORKS
        
        assert "choose_your_own_adventure" in CREATIVE_FRAMEWORKS
        assert "epistolary_novel" in CREATIVE_FRAMEWORKS


# =============================================================================
# TEST RPG FRAMEWORKS
# =============================================================================

class TestRPGFrameworks:
    """Tests for RPG framework library."""
    
    def test_rpg_frameworks_exist(self):
        """Test RPG frameworks."""
        from opus_orchestrator.nonfiction.rpg_frameworks import RPG_FRAMEWORKS
        
        assert "core_rulebook" in RPG_FRAMEWORKS
        assert "adventure_module" in RPG_FRAMEWORKS
        assert "monster_manual" in RPG_FRAMEWORKS


# =============================================================================
# TEST TEXTBOOK FRAMEWORKS
# =============================================================================

class TestTextbookFrameworks:
    """Tests for textbook framework library."""
    
    def test_textbook_frameworks(self):
        """Test textbook frameworks."""
        from opus_orchestrator.nonfiction.textbook_frameworks import TEXTBOOK_FRAMEWORKS
        
        assert "comprehensive_textbook" in TEXTBOOK_FRAMEWORKS
        assert "online_course" in TEXTBOOK_FRAMEWORKS


# =============================================================================
# TEST ACADEMIC PAPERS
# =============================================================================

class TestAcademicPapers:
    """Tests for academic paper frameworks."""
    
    def test_academic_papers(self):
        """Test academic paper types."""
        from opus_orchestrator.nonfiction.academic_papers import ACADEMIC_PAPER_TYPES
        
        assert "empirical_paper" in ACADEMIC_PAPER_TYPES
        assert "position_paper" in ACADEMIC_PAPER_TYPES


# =============================================================================
# TEST INTAKE
# =============================================================================

class TestIntake:
    """Tests for intake agent."""
    
    def test_intake_input(self):
        """Test IntakeInput dataclass."""
        from opus_orchestrator.nonfiction.intake import IntakeInput
        
        intake = IntakeInput(
            concept="My book idea",
            explicit_purpose="transform",
        )
        
        assert intake.concept == "My book idea"
        assert intake.explicit_purpose == "transform"
    
    def test_intake_result(self):
        """Test IntakeResult."""
        from opus_orchestrator.nonfiction.intake import IntakeResult, ReaderPurpose
        
        result = IntakeResult(
            purpose=ReaderPurpose.TRANSFORM,
            confidence=0.9,
            category=None,
            framework={},
            reasoning="Test",
            source="explicit",
        )
        
        assert result.purpose == ReaderPurpose.TRANSFORM
        assert result.confidence == 0.9


# =============================================================================
# TEST MULTI SOURCE INGEST
# =============================================================================

class TestMultiSourceIngest:
    """Tests for multi-source ingestion."""
    
    @pytest.mark.asyncio
    async def test_ingest_single_source(self):
        """Test ingesting from single source."""
        from opus_orchestrator.utils.multi_source_ingest import ContentSource, SourceType
        
        source = ContentSource(
            source_type=SourceType.LOCAL,
            local_path="/tmp/test",
        )
        
        assert source.source_type == SourceType.LOCAL
    
    def test_content_source(self):
        """Test ContentSource creation."""
        from opus_orchestrator.utils.multi_source_ingest import ContentSource, SourceType
        
        source = ContentSource(
            source_type=SourceType.GITHUB,
            repo="test/repo",
        )
        
        assert source.repo == "test/repo"


# =============================================================================
# TEST UTILS
# =============================================================================

class TestUtils:
    """Tests for utility functions."""
    
    def test_safe_imports(self):
        """Test all main modules import."""
        from opus_orchestrator.nonfiction import (
            PurposeClassifier,
            ReaderPurpose,
            IntakeAgent,
            select_framework,
            get_critique_criteria,
        )
        
        assert PurposeClassifier is not None
        assert ReaderPurpose is not None


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
