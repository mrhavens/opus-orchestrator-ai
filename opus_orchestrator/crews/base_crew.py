"""Base Crew for Opus Orchestrator.

Provides common functionality for all crews.
"""

import os
from typing import Any, Optional

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

load_dotenv()

from opus_orchestrator.config import get_config


def get_crewai_llm(provider: str = "openai", model: str = "gpt-4o") -> LLM:
    """Get a CrewAI LLM instance.
    
    Args:
        provider: LLM provider (openai, anthropic, etc.)
        model: Model name
        
    Returns:
        Configured CrewAI LLM
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if provider == "openai":
        return LLM(
            model="openai/" + model,
            api_key=api_key,
        )
    elif provider == "anthropic":
        return LLM(
            model="anthropic/" + model,
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )
    else:
        # Default to OpenAI
        return LLM(
            model="openai/gpt-4o",
            api_key=api_key,
        )


class OpusCrew:
    """Base class for Opus crews with common functionality."""

    def __init__(
        self,
        agents: Optional[list[Agent]] = None,
        tasks: Optional[list[Task]] = None,
        process: Process = Process.sequential,
        verbose: bool = True,
    ):
        """Initialize the crew.
        
        Args:
            agents: List of CrewAI agents
            tasks: List of tasks to complete
            process: Process type (sequential, hierarchical)
            verbose: Enable verbose output
        """
        self.config = get_config()
        self.llm = get_crewai_llm(
            provider=self.config.agent.provider,
            model=self.config.agent.model,
        )
        
        self.agents = agents or []
        self.tasks = tasks or []
        self.process = process
        self.verbose = verbose
        
        self._crew: Optional[Crew] = None

    def create_agent(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: Optional[list] = None,
        verbose: bool = True,
    ) -> Agent:
        """Create a CrewAI agent with the configured LLM.
        
        Args:
            role: Agent's role title
            goal: Agent's goal
            backstory: Agent's backstory
            tools: Optional tools for the agent
            verbose: Enable verbose
            
        Returns:
            Configured CrewAI Agent
        """
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=self.llm,
            tools=tools or [],
            verbose=verbose,
        )

    def create_task(
        self,
        description: str,
        agent: Agent,
        expected_output: Optional[str] = None,
    ) -> Task:
        """Create a CrewAI task.
        
        Args:
            description: Task description
            agent: Agent to perform the task
            expected_output: Expected output format
            
        Returns:
            Configured Task
        """
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output or "A well-written piece of content.",
        )

    def build(self) -> Crew:
        """Build the crew with configured agents and tasks.
        
        Returns:
            Configured CrewAI Crew
        """
        self._crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=self.process,
            verbose=self.verbose,
        )
        return self._crew

    def run(self, inputs: Optional[dict[str, Any]] = None) -> Any:
        """Run the crew.
        
        Args:
            inputs: Input variables for the crew
            
        Returns:
            Crew execution result
        """
        if not self._crew:
            self.build()
        
        return self._crew.kickoff(inputs=inputs or {})

    async def run_async(self, inputs: Optional[dict[str, Any]] = None) -> Any:
        """Run the crew asynchronously.
        
        Args:
            inputs: Input variables for the crew
            
        Returns:
            Crew execution result
        """
        if not self._crew:
            self.build()
        
        return await self._crew.kickoff_async(inputs=inputs or {})
