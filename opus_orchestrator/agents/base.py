"""Base agent class for Opus Orchestrator."""

from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

from opus_orchestrator.config import AgentConfig, get_config
from opus_orchestrator.utils.llm import LLMClient, get_llm_client


T = TypeVar("T", bound=BaseModel)


class AgentResponse(BaseModel):
    """Standard response from an agent."""

    success: bool
    output: Any
    error: Optional[str] = None
    metadata: dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True


class BaseAgent(ABC, Generic[T]):
    """Base class for all Opus agents.

    Each agent has:
    - A specific role (from Fortress documentation)
    - System prompts derived from Fortress methodologies
    - Input/output schemas
    - Execution logic
    """

    def __init__(
        self,
        role: str,
        description: str,
        system_prompt: str,
        output_schema: type[T] | None = None,
        config: Optional[AgentConfig] = None,
    ):
        self.role = role
        self.description = description
        self.system_prompt = system_prompt
        self.output_schema = output_schema
        self.config = config or get_config().agent
        self._llm_client: Optional[LLMClient] = None

    @property
    def llm_client(self) -> LLMClient:
        """Get or create LLM client."""
        if self._llm_client is None:
            self._llm_client = get_llm_client()
        return self._llm_client

    @abstractmethod
    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute the agent's task.

        Args:
            input_data: The input data for this agent
            context: Additional context from the orchestrator

        Returns:
            AgentResponse with output and metadata
        """
        pass

    async def call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
    ) -> str:
        """Call the LLM with prompts.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            temperature: Optional temperature override
            
        Returns:
            Generated text
        """
        temp = temperature if temperature is not None else self.config.temperature
        
        # Use async version for async context
        return await self.llm_client.complete_async(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temp,
            max_tokens=self.config.max_tokens,
        )
    def validate_output(self, output: Any, schema: type[T]) -> tuple[bool, Optional[T], Optional[str]]:
        """Validate agent output against a Pydantic schema.
        
        Args:
            output: Raw output from the agent (usually str)
            schema: Pydantic model to validate against
            
        Returns:
            Tuple of (is_valid, validated_output, error_message)
        """
        if schema is None:
            # No schema to validate against
            return True, None, None
        
        # Try to parse the output as the schema
        try:
            # If output is a string, try to parse as JSON first
            if isinstance(output, str):
                import json
                # Try to extract JSON from the output
                try:
                    # Look for JSON block
                    if "```json" in output:
                        json_str = output.split("```json")[1].split("```")[0]
                    elif "```" in output:
                        json_str = output.split("```")[1].split("```")[0]
                    else:
                        json_str = output
                    data = json.loads(json_str)
                except (json.JSONDecodeError, IndexError):
                    # Not JSON, return as-is
                    return True, None, None
            else:
                data = output
            
            # Validate against schema
            validated = schema(**data)
            return True, validated, None
            
        except Exception as e:
            return False, None, f"Validation failed: {str(e)}"



    def build_system_prompt(self, context: dict[str, Any]) -> str:
        """Build the full system prompt with context.

        Args:
            context: Additional context to inject

        Returns:
            Complete system prompt
        """
        base = self.system_prompt

        if context:
            context_str = "\n\n## Context\n"
            for key, value in context.items():
                context_str += f"- **{key}**: {value}\n"
            return base + context_str

        return base

    def build_user_prompt(self, task: str, input_data: Any) -> str:
        """Build the user prompt for a specific task.

        Args:
            task: Description of the task
            input_data: Input data formatted for the task

        Returns:
            Complete user prompt
        """
        return f"""## Task

{task}

## Input

{input_data}

## Instructions

Please complete this task following the methodology specified in your system prompt.
"""

    async def cleanup(self):
        """Clean up resources."""
        if self._llm_client:
            await self._llm_client.close()
            self._llm_client = None
