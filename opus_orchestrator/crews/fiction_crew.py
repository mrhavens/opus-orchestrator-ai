"""Fiction Writing Crew for Opus Orchestrator.

A CrewAI-powered crew for writing fiction with multiple specialized agents.
"""

from typing import Any, Optional

from crewai import Agent, Process
from dotenv import load_dotenv


from opus_orchestrator.crews.base_crew import OpusCrew
from opus_orchestrator.config import get_config


class FictionCrew(OpusCrew):
    """Fiction writing crew with Writer, Editor, and Proofreader agents."""

    def __init__(
        self,
        genre: str = "general fiction",
        tone: str = "literary",
        target_word_count: int = 1000,
        verbose: bool = True,
    ):
        """Initialize the fiction crew.
        
        Args:
            genre: Fiction genre (sci-fi, fantasy, romance, etc.)
            tone: Writing tone (literary, commercial, etc.)
            target_word_count: Target word count for the piece
            verbose: Enable verbose output
        """
        self.genre = genre
        self.tone = tone
        self.target_word_count = target_word_count
        
        super().__init__(verbose=verbose, process=Process.sequential)
        
        self._setup_agents()

    def _setup_agents(self) -> None:
        """Set up the fiction writing team."""
        
        # Writer Agent - creates the initial draft
        self.writer = self.create_agent(
            role="Fiction Writer",
            goal=f"Write compelling {self.genre} fiction that captivates readers "
                 f"with vivid prose, strong character development, and engaging narrative.",
            backstory=f"""You are an experienced {self.genre} writer known for your 
            ability to create immersive worlds and compelling characters. You understand 
            the nuances of {self.tone} writing and know how to keep readers engaged. 
            You have published multiple books and understand the craft of storytelling 
            at a deep level.""",
            verbose=self.verbose,
        )
        
        # Editor Agent - reviews and revises
        self.editor = self.create_agent(
            role="Fiction Editor",
            goal="Edit and improve the fiction draft to ensure narrative coherence, "
                 "character consistency, pacing, and emotional impact.",
            backstory="""You are a senior fiction editor with years of experience 
            working with major publishers. You have a keen eye for narrative flow, 
            character development, and pacing. You know how to turn good drafts into 
            great ones while preserving the author's voice.""",
            verbose=self.verbose,
        )
        
        # Proofreader Agent - final polish
        self.proofreader = self.create_agent(
            role="Proofreader",
            goal="Proofread the final draft for grammar, spelling, punctuation, "
                 "and consistency errors.",
            backstory="""You are a meticulous proofreader with an eagle eye for detail. 
            You specialize in fiction and know common errors to look for. You ensure 
            the final manuscript is polished and professional.""",
            verbose=self.verbose,
        )
        
        self.agents = [self.writer, self.editor, self.proofreader]

    def write_chapter(
        self,
        chapter_outline: str,
        style_guide: str,
        previous_chapters: str = "",
    ) -> str:
        """Write a chapter using the crew.
        
        Args:
            chapter_outline: Outline/summary of the chapter
            style_guide: Writing style guidelines
            previous_chapters: Content of previous chapters for continuity
            
        Returns:
            Final polished chapter text
        """
        # Task 1: Write initial draft
        write_task = self.create_task(
            description=f"""Write Chapter 1 based on this outline:

{chapter_outline}

STYLE GUIDE:
{style_guide}

PREVIOUS CHAPTERS (for continuity):
{previous_chapters}

Write a complete chapter of approximately {self.target_word_count} words. 
Make it engaging, well-paced, and true to the genre ({self.genre}) and tone ({self.tone}).""",
            agent=self.writer,
            expected_output=f"A complete chapter of {self.target_word_count}+ words in {self.genre} style.",
        )
        
        # Task 2: Edit and revise
        edit_task = self.create_task(
            description="""Review and improve the chapter draft. Ensure:
- Narrative coherence and logical flow
- Consistent character voices and motivations
- Appropriate pacing (not too fast, not too slow)
- Strong emotional beats where appropriate
- Genre conventions are met

If changes are needed, revise the chapter to address these concerns.""",
            agent=self.editor,
            expected_output="A revised and improved chapter that addresses all editorial concerns.",
        )
        
        # Task 3: Proofread
        proofread_task = self.create_task(
            description="""Proofread the final chapter. Check for:
- Grammar and spelling errors
- Punctuation mistakes
- Inconsistent capitalization
- Formatting issues
- Word choice problems

Fix any errors found. The chapter should be publication-ready.""",
            agent=self.proofreader,
            expected_output="A polished, error-free chapter ready for publication.",
        )
        
        self.tasks = [write_task, edit_task, proofread_task]
        
        result = self.run(inputs={
            "chapter_outline": chapter_outline,
            "style_guide": style_guide,
            "previous_chapters": previous_chapters,
        })
        
        return str(result)

    def write_full_story(
        self,
        story_outline: str,
        character_sheets: str,
        style_guide: str,
        num_chapters: int = 3,
    ) -> list[str]:
        """Write a full story with multiple chapters.
        
        Args:
            story_outline: Overall story outline
            character_sheets: Character descriptions
            style_guide: Writing style guidelines
            num_chapters: Number of chapters to write
            
        Returns:
            List of chapter texts
        """
        chapters = []
        previous = ""
        
        for i in range(1, num_chapters + 1):
            print(f"\\n📝 Writing Chapter {i}/{num_chapters}...")
            
            chapter_outline = f"""
{story_outline}

This is Chapter {i} of {num_chapters}.
"""
            chapter = self.write_chapter(
                chapter_outline=chapter_outline,
                style_guide=style_guide,
                previous_chapters=previous,
            )
            
            chapters.append(chapter)
            previous += f"\n\n--- Chapter {i} ---\n\n{chapter}\n\n"
        
        return chapters


def create_fiction_crew(
    genre: str = "general fiction",
    tone: str = "literary",
    target_word_count: int = 1000,
    verbose: bool = True,
) -> FictionCrew:
    """Factory function to create a fiction crew.
    
    Args:
        genre: Fiction genre
        tone: Writing tone
        target_word_count: Target word count
        verbose: Enable verbose output
        
    Returns:
        Configured FictionCrew instance
    """
    return FictionCrew(
        genre=genre,
        tone=tone,
        target_word_count=target_word_count,
        verbose=verbose,
    )
