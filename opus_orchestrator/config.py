"""Opus Orchestrator AI - Configuration."""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class FortressConfig(BaseModel):
    """Configuration for Fortress integration."""

    fiction_repo: str = "mrhavens/fiction-fortress"
    nonfiction_repo: str = "mrhavens/nonfiction-fortress"
    crewai_repo: str = "mrhavens/crewai-fortress"
    autogen_repo: str = "mrhavens/autogen-fortress"
    langgraph_repo: str = "mrhavens/langgraph-fortress"


class AgentConfig(BaseModel):
    """Configuration for AI agents."""

    model: str = Field(default="gpt-4o", description="Default model for agents")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, description="Max tokens per response")
    max_iterations: int = Field(default=10, description="Max iterations per agent task")


class IterationConfig(BaseModel):
    """Configuration for iteration loops."""

    min_critic_rounds: int = Field(default=2, description="Minimum critic review rounds")
    max_critic_rounds: int = Field(default=5, description="Maximum critic review rounds")
    approval_threshold: float = Field(default=0.8, description="Score threshold to proceed")
    auto_proceed_threshold: float = Field(default=0.9, description="Score to auto-approve")


class OutputConfig(BaseModel):
    """Configuration for output generation."""

    format: str = Field(default="markdown", description="Output format: markdown, epub, pdf")
    include_frontmatter: bool = True
    include_toc: bool = True
    chapter_separator: str = "\n\n---\n\n"
    output_dir: Path = Field(default=Path("./output"))


class OpusConfig(BaseModel):
    """Main configuration for Opus Orchestrator."""

    fortress: FortressConfig = Field(default_factory=FortressConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    iteration: IterationConfig = Field(default_factory=IterationConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)

    github_token: Optional[str] = Field(default=None, description="GitHub token for private repos")

    class Config:
        frozen = False


# Global config instance
_config: Optional[OpusConfig] = None


def get_config() -> OpusConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = OpusConfig()
    return _config


def set_config(config: OpusConfig) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config
