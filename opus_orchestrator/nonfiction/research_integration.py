"""Research Integration for Nonfiction Generation.

Integrates the research agent into the main nonfiction pipeline.
"""

from typing import Optional
from dataclasses import dataclass

from opus_orchestrator.nonfiction import ReaderPurpose


@dataclass
class ResearchRequest:
    """A research request for the research agent."""
    topic: str
    subtopics: list[str]
    depth: str = "standard"  # shallow, standard, deep
    include_academic: bool = False


@dataclass
class ResearchResult:
    """Result from research agent."""
    summary: str
    key_findings: list[str]
    sources: list[str]
    gaps_identified: list[str]
    raw_data: dict


class ResearchIntegrator:
    """Integrates research into the nonfiction pipeline.
    
    Can be used at different stages:
    - Pre-writing: Gather research for the book
    - Per-chapter: Research specific topics
    - Verification: Check facts post-writing
    """
    
    def __init__(self, research_agent=None):
        self.research_agent = research_agent
    
    async def research_for_book(
        self,
        concept: str,
        purpose: ReaderPurpose,
        depth: str = "standard",
    ) -> ResearchResult:
        """Conduct research for an entire book.
        
        Args:
            concept: The book concept/topic
            purpose: The reader purpose (determines research focus)
            depth: How deep to research
            
        Returns:
            ResearchResult with findings and sources
        """
        # Determine research focus based on purpose
        research_focus = self._get_research_focus(purpose)
        
        # Build research queries
        queries = self._build_research_queries(concept, purpose)
        
        # This would call the actual research agent
        # For now, return a structured result
        return ResearchResult(
            summary=f"Research for {concept} focused on {research_focus}",
            key_findings=[
                "Finding 1 would go here",
                "Finding 2 would go here",
            ],
            sources=["Source 1", "Source 2"],
            gaps_identified=["Gap 1", "Gap 2"],
            raw_data={},
        )
    
    def _get_research_focus(self, purpose: ReaderPurpose) -> str:
        """Determine research focus based on purpose."""
        focus_map = {
            ReaderPurpose.LEARN_HANDS_ON: "best practices, tutorials, methods",
            ReaderPurpose.UNDERSTAND: "theories, concepts, explanations",
            ReaderPurpose.TRANSFORM: "case studies, success stories, methods",
            ReaderPurpose.DECIDE: "data, studies, comparisons, evidence",
            ReaderPurpose.REFERENCE: "comprehensive documentation, specifications",
            ReaderPurpose.BE_INSPIRED: "stories, journeys, examples",
        }
        return focus_map.get(purpose, "general information")
    
    def _build_research_queries(self, concept: str, purpose: ReaderPurpose) -> list[str]:
        """Build research queries based on concept and purpose."""
        base_query = concept
        
        queries = [
            f"{base_query} overview",
            f"{base_query} {self._get_research_focus(purpose)}",
        ]
        
        if purpose == ReaderPurpose.DECIDE:
            queries.extend([
                f"{base_query} pros and cons",
                f"{base_query} comparison",
                f"{base_query} research studies",
            ])
        
        elif purpose == ReaderPurpose.TRANSFORM:
            queries.extend([
                f"{base_query} success stories",
                f"{base_query} case studies",
                f"{base_query} methods",
            ])
        
        elif purpose == ReaderPurpose.UNDERSTAND:
            queries.extend([
                f"{base_query} theory",
                f"{base_query} concept explained",
                f"{base_query} how it works",
            ])
        
        return queries
    
    async def research_chapter(
        self,
        chapter_topic: str,
        context: dict,
    ) -> ResearchResult:
        """Research a specific chapter.
        
        Args:
            chapter_topic: What this chapter is about
            context: Book context (concept, purpose, etc.)
            
        Returns:
            ResearchResult for this chapter
        """
        # Research this specific topic
        queries = [
            f"{chapter_topic} overview",
            f"{chapter_topic} best practices",
            f"{chapter_topic} recent developments",
        ]
        
        return ResearchResult(
            summary=f"Research for chapter: {chapter_topic}",
            key_findings=[],
            sources=[],
            gaps_identified=[],
            raw_data={},
        )
    
    def should_use_research(self, purpose: ReaderPurpose) -> bool:
        """Determine if research should be used for this purpose.
        
        Args:
            purpose: The reader purpose
            
        Returns:
            Whether to use research
        """
        # Research is valuable for these purposes
        research_worthwhile = [
            ReaderPurpose.UNDERSTAND,
            ReaderPurpose.DECIDE,
            ReaderPurpose.TRANSFORM,
            ReaderPurpose.LEARN_HANDS_ON,
        ]
        
        return purpose in research_worthwhile
    
    def get_research_stages(self) -> list[str]:
        """Get the stages where research can be integrated.
        
        Returns:
            List of stage names where research applies
        """
        return [
            "pre_writing",      # Research before writing begins
            "per_chapter",       # Research each chapter
            "verification",      # Verify facts after writing
            "enhancement",        # Add research to strengthen content
        ]


def get_research_config_for_purpose(purpose: ReaderPurpose) -> dict:
    """Get research configuration optimized for purpose.
    
    Args:
        purpose: The reader purpose
        
    Returns:
        Dict with research settings
    """
    configs = {
        ReaderPurpose.LEARN_HANDS_ON: {
            "depth": "standard",
            "include_tutorials": True,
            "include_best_practices": True,
            "include_academic": False,
        },
        ReaderPurpose.UNDERSTAND: {
            "depth": "deep",
            "include_theories": True,
            "include_explanations": True,
            "include_academic": True,
        },
        ReaderPurpose.TRANSFORM: {
            "depth": "standard",
            "include_case_studies": True,
            "include_success_stories": True,
            "include_methods": True,
        },
        ReaderPurpose.DECIDE: {
            "depth": "deep",
            "include_studies": True,
            "include_data": True,
            "include_comparisons": True,
            "include_academic": True,
        },
        ReaderPurpose.REFERENCE: {
            "depth": "deep",
            "include_specifications": True,
            "include_documentation": True,
            "include_comprehensive": True,
        },
        ReaderPurpose.BE_INSPIRED: {
            "depth": "shallow",
            "include_stories": True,
            "include_journeys": True,
            "include_examples": True,
        },
    }
    
    return configs.get(purpose, {"depth": "standard"})
