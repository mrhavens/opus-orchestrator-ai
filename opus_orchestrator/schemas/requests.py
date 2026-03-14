"""Input validation for Opus API requests.

Uses Pydantic for robust request validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal


class GenerateRequest(BaseModel):
    """Request to generate a book."""
    
    concept: str = Field(..., min_length=3, max_length=500)
    repo: Optional[str] = None
    
    # Framework options
    framework: str = Field(default="snowflake")
    genre: str = Field(default="fiction")
    book_type: Literal["fiction", "nonfiction"] = Field(default="fiction")
    
    # Nonfiction options
    purpose: Optional[Literal["learn", "understand", "transform", "decide", "reference", "inspire"]] = None
    category: Optional[str] = None
    
    # Generation options
    words: int = Field(default=5000, ge=100, le=200000)
    chapters: int = Field(default=3, ge=1, le=100)
    tone: str = Field(default="literary")
    
    # Orchestration options
    use_crewai: bool = False
    use_autogen: bool = True
    
    # Checkpointing
    thread_id: Optional[str] = None
    resume: bool = False
    
    @validator("concept")
    def concept_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Concept cannot be empty")
        return v.strip()
    
    @validator("repo")
    def validate_repo(cls, v):
        if v and not cls._is_valid_repo(v):
            raise ValueError("Invalid repository format. Use 'owner/repo'")
        return v
    
    @staticmethod
    def _is_valid_repo(repo: str) -> bool:
        return "/" in repo and len(repo.split("/")) == 2
    
    class Config:
        schema_extra = {
            "example": {
                "concept": "A robot who dreams of being human",
                "genre": "sci-fi",
                "book_type": "fiction",
                "words": 5000
            }
        }


class IngestRequest(BaseModel):
    """Request to ingest content."""
    
    source_type: Literal["github", "s3", "local", "url"] = Field(...)
    repo: Optional[str] = None
    bucket: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    
    @validator("source_type")
    def validate_source(cls, v, values):
        required = {
            "github": "repo",
            "s3": "bucket", 
            "local": "path",
            "url": "url",
        }
        if required.get(v) and not values.get(required[v]):
            raise ValueError(f"{required[v]} required for {v} source")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "source_type": "github",
                "repo": "owner/repo"
            }
        }


class ConfigRequest(BaseModel):
    """Request to update config."""
    
    provider: Optional[Literal["openai", "anthropic", "minimax"]] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=4000, ge=100, le=100000)
    
    @validator("temperature")
    def validate_temperature(cls, v):
        if v < 0 or v > 2:
            raise ValueError("Temperature must be between 0 and 2")
        return v
