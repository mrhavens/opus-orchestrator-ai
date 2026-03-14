"""Opus Orchestrator AI - Configuration."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


def _load_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Load from environment variable."""
    return os.environ.get(key, default)


class FortressConfig(BaseModel):
    """Configuration for Fortress integration."""

    fiction_repo: str = "mrhavens/fiction-fortress"
    nonfiction_repo: str = "mrhavens/nonfiction-fortress"
    crewai_repo: str = "mrhavens/crewai-fortress"
    autogen_repo: str = "mrhavens/autogen-fortress"
    langgraph_repo: str = "mrhavens/langgraph-fortress"


class AgentConfig(BaseModel):
    """Configuration for AI agents."""

    model: str = Field(default="MiniMax/MiniMax-M2.5", description="Default model for agents")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, description="Max tokens per response")
    max_iterations: int = Field(default=10, description="Max iterations per agent task")
    timeout: float = Field(default=120.0, description="HTTP timeout in seconds")
    
    # Provider configuration
    provider: str = Field(default="minimax", description="LLM provider: minimax, openai, anthropic")
    api_key: Optional[str] = Field(default=None, description="API key for LLM provider")


class IterationConfig(BaseModel):
    """Configuration for iteration loops."""

    min_critic_rounds: int = Field(default=2, description="Minimum critic review rounds")
    max_critic_rounds: int = Field(default=5, description="Maximum critic review rounds")
    approval_threshold: float = Field(default=0.8, description="Score threshold to proceed")
    auto_proceed_threshold: float = Field(default=0.9, description="Score to auto-approve")


class CostConfig(BaseModel):
    """Configuration for cost controls and rate limiting."""
    
    max_tokens_per_run: Optional[int] = Field(
        default=None, 
        description="Maximum tokens allowed per generation run"
    )
    max_cost_usd: Optional[float] = Field(
        default=None,
        description="Maximum cost allowed per generation run (USD)"
    )
    track_usage: bool = Field(
        default=True,
        description="Track cumulative token usage"
    )
    # Token prices (approximate, per 1M tokens)
    price_per_million_tokens: dict[str, float] = Field(
        default_factory=lambda: {
            "gpt-4o": 15.00,
            "gpt-4o-mini": 0.60,
            "claude-3-opus": 15.00,
            "claude-3-sonnet": 3.00,
            "minimax": 1.00,  # Approximate
        },
        description="Price per million tokens by model"
    )


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
    cost: CostConfig = Field(default_factory=CostConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)

    github_token: Optional[str] = Field(default=None, description="GitHub token for private repos")

    class Config:
        frozen = False


def load_config_from_env() -> OpusConfig:
    """Load configuration from environment variables.
    
    Reads:
    - MINIMAX_API_KEY for LLM
    - GITHUB_TOKEN for GitHub operations
    
    Uses MiniMax exclusively.
    """
    # Load MiniMax API key
    minimax_key = _load_env("MINIMAX_API_KEY")
    
    # Use MiniMax only
    if minimax_key:
        provider = "minimax"
        default_model = "MiniMax/MiniMax-M2.5"
        api_key = minimax_key
    else:
        provider = "minimax"
        default_model = "MiniMax/MiniMax-M2.5"
        api_key = None
    
    github_token = _load_env("GITHUB_TOKEN")
    
    agent_config = AgentConfig(
        model=default_model,
        provider=provider,
        api_key=api_key,
    )
    
    return OpusConfig(
        agent=agent_config,
        github_token=github_token,
    )


# Global config instance
_config: Optional[OpusConfig] = None


def get_config() -> OpusConfig:
    """Get the global configuration instance with validation."""
    global _config
    if _config is None:
        # Try to load from environment
        try:
            _config = load_config_from_env()
        except Exception:
            _config = OpusConfig()
    
    # Validate API keys are present
    _validate_config(_config)
    
    return _config


def _validate_config(config: OpusConfig) -> None:
    """Validate configuration at startup.
    
    Raises:
        ValueError: If required configuration is missing
    """
    errors = []
    
    # Check for API key
    if not config.agent.api_key:
        # Check environment
        if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("MINIMAX_API_KEY"):
            errors.append(
                "No LLM API key found. Set OPENAI_API_KEY or MINIMAX_API_KEY environment variable."
            )
    
    if errors:
        error_msg = "\n".join(errors)
        raise ValueError(f"Configuration validation failed:\n{error_msg}")


def set_config(config: OpusConfig) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config
