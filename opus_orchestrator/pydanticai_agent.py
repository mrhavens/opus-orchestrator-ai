"""PydanticAI Agent for Opus Orchestrator.

Provides structured output validation and agent expertise using PydanticAI.
"""

import os
from typing import Any, Optional, Type

from pydantic import BaseModel
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv("/home/solaria/.openclaw/workspace/opus-orchestrator-ai/.env")

from opus_orchestrator.config import get_config


def get_pydanticai_model() -> str:
    """Get the model name for PydanticAI.
    
    Returns:
        Model string for PydanticAI
    """
    config = get_config()
    
    # Map our config to PydanticAI model names
    if config.agent.provider == "openai":
        return "openai:gpt-4o"
    elif config.agent.provider == "anthropic":
        return "anthropic:claude-3-5-sonnet-20241022"
    else:
        return "openai:gpt-4o"


class OpusPydanticAgent:
    """PydanticAI-powered agent with structured output validation.
    
    This agent ensures all outputs conform to defined schemas,
    providing type-safe, validated responses.
    """

    def __init__(
        self,
        result_type: Optional[Type[BaseModel]] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ):
        """Initialize the PydanticAI agent.
        
        Args:
            result_type: Pydantic model for structured output
            model: Override model name
            system_prompt: System prompt for the agent
        """
        self.config = get_config()
        self.model = model or get_pydanticai_model()
        self.result_type = result_type
        self.system_prompt = system_prompt
        
        # Create the PydanticAI agent
        self._agent: Optional[Agent] = None
        self._setup_agent()

    def _setup_agent(self) -> None:
        """Set up the PydanticAI agent."""
        model = self.model
        
        # Build system prompt
        system_prompt = self.system_prompt or """You are an expert writer and editor for Opus Orchestrator.
You produce high-quality, structured output that conforms to the given schema.
Always follow best practices for the content type you're creating."""
        
        if self.result_type:
            self._agent = Agent(
                model=model,
                output_type=self.result_type,
                system_prompt=system_prompt,
            )
        else:
            self._agent = Agent(
                model=model,
                system_prompt=system_prompt,
            )

    async def run(self, prompt: str) -> BaseModel | str:
        """Run the agent with a prompt.
        
        Args:
            prompt: User prompt
            
        Returns:
            Structured result or string
        """
        if not self._agent:
            self._setup_agent()
        
        if self.result_type:
            result = await self._agent.run(prompt)
            return result.output
        else:
            result = await self._agent.run(prompt)
            return result.output

    def run_sync(self, prompt: str) -> BaseModel | str:
        """Run the agent synchronously.
        
        Args:
            prompt: User prompt
            
        Returns:
            Structured result or string
        """
        import asyncio
        
        if not self._agent:
            self._setup_agent()
        
        if self.result_type:
            result = asyncio.run(self._agent.run(prompt))
            return result.output
        else:
            result = asyncio.run(self._agent.run(prompt))
            return result.output


# =============================================================================
# SCHEMAS FOR STRUCTURED OUTPUT
# =============================================================================

class StorySeed(BaseModel):
    """Structured story seed output."""
    one_sentence: str
    one_paragraph: str
    genre: str
    target_audience: str
    tone: str
    themes: list[str]


class CharacterProfile(BaseModel):
    """Character profile schema."""
    name: str
    role: str  # protagonist, antagonist, supporting
    description: str
    motivations: list[str]
    flaws: list[str]
    backstory: str
    arc: str  # character transformation


class ChapterOutline(BaseModel):
    """Chapter outline schema."""
    chapter_number: int
    title: str
    summary: str
    pov_character: str
    key_events: list[str]
    setting: str
    chapter_goal: str
    chapter_resolution: str


class ChapterDraft(BaseModel):
    """Chapter draft schema."""
    chapter_number: int
    title: str
    content: str
    word_count: int
    pov: str
    tone: str
    key_moments: list[str]
    dialogue_snippets: list[str]


class CritiqueResult(BaseModel):
    """Critique result schema."""
    score: float  # 0.0 - 1.0
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
    verdict: str  # APPROVED, MINOR_REVISIONS, MAJOR_REVISIONS


class StyleGuide(BaseModel):
    """Style guide schema."""
    tone: str
    voice: str
    vocabulary_level: str
    sentence_structure: str
    pacing: str
    dialogue_style: str
    description_style: str
    prohibited_elements: list[str]


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

def create_story_seed_agent() -> OpusPydanticAgent:
    """Create agent for generating story seeds."""
    return OpusPydanticAgent(
        result_type=StorySeed,
        system_prompt="""You are a story architect expert. Create detailed story seeds
that capture the essence of a story concept. Include genre, audience, tone, and themes.""",
    )


def create_character_agent() -> OpusPydanticAgent:
    """Create agent for generating character profiles."""
    return OpusPydanticAgent(
        result_type=CharacterProfile,
        system_prompt="""You are a character development expert. Create rich, detailed
character profiles with clear motivations, flaws, and arcs. Make characters feel real.""",
    )


def create_chapter_outline_agent() -> OpusPydanticAgent:
    """Create agent for generating chapter outlines."""
    return OpusPydanticAgent(
        result_type=ChapterOutline,
        system_prompt="""You are a plot structure expert. Create detailed chapter outlines
with clear goals, events, and resolutions. Ensure pacing works for the genre.""",
    )


def create_chapter_draft_agent() -> OpusPydanticAgent:
    """Create agent for writing chapter drafts."""
    return OpusPydanticAgent(
        result_type=ChapterDraft,
        system_prompt="""You are an expert fiction writer. Write compelling, well-paced
chapters that follow the outline while adding rich detail, dialogue, and description.""",
    )


def create_critique_agent() -> OpusPydanticAgent:
    """Create agent for critiquing content."""
    return OpusPydanticAgent(
        result_type=CritiqueResult,
        system_prompt="""You are an expert literary critic. Evaluate content objectively,
providing constructive feedback. Score honestly - don't inflate scores. Be specific.""",
    )


def create_style_guide_agent() -> OpusPydanticAgent:
    """Create agent for generating style guides."""
    return OpusPydanticAgent(
        result_type=StyleGuide,
        system_prompt="""You are an expert editor. Create comprehensive style guides
that capture the voice and tone of the intended work. Be specific and actionable.""",
    )
