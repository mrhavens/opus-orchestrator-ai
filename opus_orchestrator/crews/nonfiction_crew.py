"""Nonfiction Writing Crew for Opus Orchestrator.

A CrewAI-powered crew for writing nonfiction with research and fact-checking.
"""

from typing import Any, Optional

from crewai import Agent, Process
from dotenv import load_dotenv

load_dotenv()

from opus_orchestrator.crews.base_crew import OpusCrew
from opus_orchestrator.config import get_config


class NonfictionCrew(OpusCrew):
    """Nonfiction writing crew with Researcher, Writer, Fact-Checker, and Editor."""

    def __init__(
        self,
        topic: str = "general",
        tone: str = "informative",
        target_word_count: int = 1000,
        verbose: bool = True,
    ):
        """Initialize the nonfiction crew.
        
        Args:
            topic: Main topic/subject area
            tone: Writing tone (academic, conversational, etc.)
            target_word_count: Target word count for the piece
            verbose: Enable verbose output
        """
        self.topic = topic
        self.tone = tone
        self.target_word_count = target_word_count
        
        super().__init__(verbose=verbose, process=Process.sequential)
        
        self._setup_agents()

    def _setup_agents(self) -> None:
        """Set up the nonfiction writing team."""
        
        # Researcher Agent - gathers information
        self.researcher = self.create_agent(
            role="Researcher",
            goal=f"Thoroughly research {self.topic} to provide accurate, comprehensive "
                 f"information for the writer.",
            backstory=f"""You are an expert researcher specializing in {self.topic}. 
            You know how to find reliable sources, verify information, and synthesize 
            complex topics into clear, accurate summaries. You have access to vast 
            knowledge and can explain nuanced subjects with clarity.""",
            verbose=self.verbose,
        )
        
        # Writer Agent - creates the initial draft
        self.writer = self.create_agent(
            role="Nonfiction Writer",
            goal=f"Write compelling {self.topic} content that informs, educates, "
                 f"and engages readers with {self.tone} tone.",
            backstory=f"""You are an experienced nonfiction writer known for your 
            ability to explain complex topics clearly. You write in a {self.tone} 
            style that resonates with general audiences while maintaining accuracy. 
            You know how to structure arguments and present evidence effectively.""",
            verbose=self.verbose,
        )
        
        # Fact-Checker Agent - verifies accuracy
        self.fact_checker = self.create_agent(
            role="Fact-Checker",
            goal="Verify all factual claims in the draft for accuracy and cite sources properly.",
            backstory="""You are a meticulous fact-checker with experience in journalism 
            and academic publishing. You know how to verify claims, check statistics, 
            and ensure all assertions are backed by reliable sources. You catch errors 
            that others miss.""",
            verbose=self.verbose,
        )
        
        # Editor Agent - reviews and refines
        self.editor = self.create_agent(
            role="Nonfiction Editor",
            goal="Edit and improve the nonfiction draft for clarity, structure, "
                 "and reader engagement while maintaining accuracy.",
            backstory="""You are a senior nonfiction editor with years of experience 
            working with authors on books, articles, and essays. You ensure content 
            is well-structured, arguments are logical, and the writing is clear and 
            engaging. You preserve the author's voice while improving the manuscript.""",
            verbose=self.verbose,
        )
        
        self.agents = [self.researcher, self.writer, self.fact_checker, self.editor]

    def write_section(
        self,
        section_outline: str,
        research_findings: str = "",
        style_guide: str = "",
    ) -> str:
        """Write a section using the crew.
        
        Args:
            section_outline: Outline/summary of the section
            research_findings: Existing research to incorporate
            style_guide: Writing style guidelines
            
        Returns:
            Final polished section text
        """
        # Task 1: Research (if not already done)
        if research_findings:
            research_task = self.create_task(
                description=f"""Research the following topic to provide accurate information:

{section_outline}

Provide key facts, statistics, and insights that will be needed for writing.""",
                agent=self.researcher,
                expected_output="Comprehensive research findings on the topic.",
            )
            self.tasks.append(research_task)
        
        # Task 2: Write initial draft
        write_task = self.create_task(
            description=f"""Write a nonfiction section based on this outline:

{section_outline}

RESEARCH FINDINGS:
{research_findings}

STYLE GUIDE:
{style_guide}

Write approximately {self.target_word_count} words. 
Make it informative, well-structured, and engaging in {self.tone} tone.""",
            agent=self.writer,
            expected_output=f"A complete section of {self.target_word_count}+ words.",
        )
        
        # Task 3: Fact-check
        factcheck_task = self.create_task(
            description="""Review and fact-check the section. Verify:
- All statistics and numbers are accurate
- Claims are supported by evidence
- Sources are reliable
- No misinformation or outdated claims

If issues found, note them for revision.""",
            agent=self.fact_checker,
            expected_output="Fact-checked section with verified claims.",
        )
        
        # Task 4: Edit and refine
        edit_task = self.create_task(
            description="""Edit and improve the section. Ensure:
- Clear structure with logical flow
- Strong introduction and conclusion
- Smooth transitions between points
- Appropriate tone ({self.tone})
- Reader engagement throughout

Address any fact-checking concerns. Make it publication-ready.""",
            agent=self.editor,
            expected_output="A polished, publication-ready nonfiction section.",
        )
        
        self.tasks = [t for t in self.tasks if t] + [write_task, factcheck_task, edit_task]
        
        result = self.run(inputs={
            "section_outline": section_outline,
            "research_findings": research_findings,
            "style_guide": style_guide,
        })
        
        return str(result)

    def write_chapter(
        self,
        chapter_outline: str,
        source_materials: str = "",
        style_guide: str = "",
    ) -> str:
        """Write a chapter using the crew.
        
        Args:
            chapter_outline: Outline/summary of the chapter
            source_materials: Source materials to draw from
            style_guide: Writing style guidelines
            
        Returns:
            Final polished chapter text
        """
        # Task 1: Research
        research_task = self.create_task(
            description=f"""Research thoroughly for this chapter:

{chapter_outline}

Use these source materials:
{source_materials}

Provide comprehensive research findings including key facts, expert opinions, 
and supporting evidence.""",
            agent=self.researcher,
            expected_output="Comprehensive research findings for the chapter.",
        )
        
        # Task 2: Write
        write_task = self.create_task(
            description=f"""Write a complete nonfiction chapter based on this outline:

{chapter_outline}

Use the research findings to support your arguments and provide valuable insights.

STYLE GUIDE:
{style_guide}

Write a chapter of approximately {self.target_word_count} words in {self.tone} tone.
Make it informative, engaging, and well-structured.""",
            agent=self.writer,
            expected_output=f"A complete chapter of {self.target_word_count}+ words.",
        )
        
        # Task 3: Fact-check
        factcheck_task = self.create_task(
            description="""Fact-check the entire chapter. Verify:
- All statistics, dates, and numbers
- Quoted statements and attributions
- Scientific claims and studies
- Historical facts and events
- Any potentially controversial claims

Provide a detailed report of any issues found.""",
            agent=self.fact_checker,
            expected_output="Fact-checked chapter with verified information.",
        )
        
        # Task 4: Edit
        edit_task = self.create_task(
            description=f"""Edit and finalize the chapter. Ensure:
- Clear chapter structure with logical flow
- Strong opening and closing
- Smooth transitions between sections
- Consistent {self.tone} tone throughout
- All fact-check issues addressed
- Publication-ready quality

This is the final polish pass.""",
            agent=self.editor,
            expected_output="A polished, publication-ready chapter.",
        )
        
        self.tasks = [research_task, write_task, factcheck_task, edit_task]
        
        result = self.run(inputs={
            "chapter_outline": chapter_outline,
            "source_materials": source_materials,
            "style_guide": style_guide,
        })
        
        return str(result)


def create_nonfiction_crew(
    topic: str = "general",
    tone: str = "informative",
    target_word_count: int = 1000,
    verbose: bool = True,
) -> NonfictionCrew:
    """Factory function to create a nonfiction crew.
    
    Args:
        topic: Main topic/subject
        tone: Writing tone
        target_word_count: Target word count
        verbose: Enable verbose output
        
    Returns:
        Configured NonfictionCrew instance
    """
    return NonfictionCrew(
        topic=topic,
        tone=tone,
        target_word_count=target_word_count,
        verbose=verbose,
    )
