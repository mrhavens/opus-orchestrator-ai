#!/usr/bin/env python3
"""
CrewAI Agent Teams for Opus Orchestrator
========================================
Creates 5 specialized CrewAI agents to fix issues in parallel.
"""

import asyncio
import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# Get API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY not found in environment")
    sys.exit(1)

def create_agent(name: str, role: str, goal: str, backstory: str):
    """Create a specialized CrewAI agent."""
    return Agent(
        name=name,
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
    )


# ============================================================================
# TEAM 1: Critical Bug Fix Squad
# ============================================================================

TEAM_1_AGENT = create_agent(
    name="CriticalBugSquad",
    role="Senior Python Developer - Bug Fixer",
    goal="Fix critical bugs that prevent Opus from running",
    backstory="""You are a senior Python developer with 15+ years of experience.
You specialize in debugging complex async code, FastAPI applications, and LangGraph workflows.
You have a reputation for finding and fixing bugs that others miss.
Your code is always tested and follows best practices.
You are methodical: you read the code, understand the bug, fix it, and verify."""
)

TEAM_1_TASK = Task(
    description="""Fix these critical bugs in Opus Orchestrator:

1. opus_orchestrator/utils/llm.py - The async methods use `self.client` which is undefined.
   Should use `self._async_client` instead.
   
2. opus_orchestrator/server.py - The /upload endpoint uses UploadFile and File 
   without importing them from FastAPI.
   
3. opus_orchestrator/langgraph_workflow.py - The fallback mechanism just returns
   initial_state instead of real recovery. Implement proper error handling.

Read each file, identify the exact bug, fix it, and ensure the fix is correct.""",
    agent=TEAM_1_AGENT,
    expected_output="Fixed Python files with bug corrections applied"
)


# ============================================================================
# TEAM 2: Agent & Workflow Repair
# ============================================================================

TEAM_2_AGENT = create_agent(
    name="AgentWorkflowRepair",
    role="Multi-Agent Systems Specialist",
    goal="Fix agent behavior and workflow logic issues",
    backstory="""You are a specialist in multi-agent AI systems.
You have deep experience with AutoGen, CrewAI, and LangGraph.
You understand how agents should collaborate, critique, and revise work.
You fixed many bugs in agent orchestration systems.
Your specialty is making agents actually do what they're supposed to do."""
)

TEAM_2_TASK = Task(
    description="""Fix these agent/workflow bugs in Opus Orchestrator:

1. opus_orchestrator/autogen_critique.py - The iterate_chapter() method runs
   a critique loop but never actually revises the chapter. The comment says
   "In production: pass feedback to writer agent for revision" but it's commented out.
   Implement actual revision logic.
   
2. opus_orchestrator/crews/base_crew.py - The get_crewai_llm() function accepts
   provider and model parameters but ignores them, always using OpenAI.
   Make it actually use the passed parameters.

Read each file, understand the bug, fix it, verify the logic is correct.""",
    agent=TEAM_2_AGENT,
    expected_output="Fixed agent and workflow code with proper logic"
)


# ============================================================================
# TEAM 3: Infrastructure & Config
# ============================================================================

TEAM_3_AGENT = create_agent(
    name="InfrastructureTeam",
    role="DevOps & Infrastructure Engineer",
    goal="Improve configuration, error handling, and infrastructure",
    backstory="""You are a DevOps and infrastructure engineer with expertise in
Python application configuration, error handling, and best practices.
You believe in fail-fast with clear messages, not silent failures.
You understand API rate limiting and cost controls.
You make systems robust and production-ready."""
)

TEAM_3_TASK = Task(
    description="""Fix these infrastructure issues in Opus Orchestrator:

1. opus_orchestrator/utils/github_ingest.py - GitHubIngestor requires a token
   for all repos, but public repos don't need one. Make token optional for
   public repos, required only for private.
   
2. opus_orchestrator/config.py + orchestrator.py - When API keys are missing,
   the system proceeds anyway and fails later with obscure errors.
   Add validation at startup with clear error messages.
   
3. opus_orchestrator/config.py - Add rate limiting and cost controls:
   - Add max_tokens_per_run to config
   - Track cumulative token usage
   - Add cost estimation
   - Implement early termination when budget exceeded

Read each file, implement the fixes, ensure proper error handling.""",
    agent=TEAM_3_AGENT,
    expected_output="Infrastructure improvements with proper error handling"
)


# ============================================================================
# TEAM 4: Architecture & Design
# ============================================================================

TEAM_4_AGENT = create_agent(
    name="ArchitectureSquad",
    role="Software Architect",
    goal="Refactor design issues and consolidate duplicate code",
    backstory="""You are a software architect with expertise in clean code,
refactoring, and system design. You specialize in reducing complexity
and eliminating duplication. You believe in DRY (Don't Repeat Yourself)
and single sources of truth. You make systems maintainable."""
)

TEAM_4_TASK = Task(
    description="""Fix these architecture/design issues in Opus Orchestrator:

1. opus_orchestrator/state.py and langgraph_state.py - There are two parallel
   state models (OpusState and OpusGraphState) that duplicate fields.
   Create a unified state model that both can use, or create clear adapters.

2. opus_orchestrator/agents/base.py - Agents return raw text strings,
   not validated Pydantic models. Add output validation using the existing
   schemas in schemas/book.py. Make agents return validated output.

3. opus_orchestrator/frameworks.py and orchestrator.py - There are two
   different systems for framework prompts. Consolidate into a single
   source of truth in frameworks.py and import it in orchestrator.py.

This is refactoring work - preserve existing functionality while improving design.""",
    agent=TEAM_4_AGENT,
    expected_output="Refactored code with improved architecture"
)


# ============================================================================
# TEAM 5: Features & Polish
# ============================================================================

TEAM_5_AGENT = create_agent(
    name="FeaturesTeam",
    role="Full-Stack Developer - Features",
    goal="Implement missing features and polish the application",
    backstory="""You are a full-stack developer who loves implementing features
and making things complete. You have experience with testing, streaming,
state persistence, and integrating disconnected components.
You make software feature-complete and production-ready."""
)

TEAM_5_TASK = Task(
    description="""Implement these features in Opus Orchestrator:

1. tests/test_orchestrator.py - Add basic test coverage:
   - Test framework prompts
   - Test CLI commands (mocked)
   - Test schema validation
   
2. opus_orchestrator/langgraph_workflow.py - Enable checkpointing:
   - Change checkpointer = None to use MemorySaver
   - Add config option to enable/disable
   - Store thread_id for resume capability

3. opus_orchestrator/server.py - Implement streaming:
   - Add /generate/stream endpoint using Server-Sent Events
   - Stream progress updates (stage, percentage)
   
4. Split large files (if time permits):
   - Extract CLI commands into separate modules
   - Target: no file > 400 lines

Note: For issues #15 (Research Agent) and #16 (Nonfiction), add TODO
comments describing what needs to be done for future work.""",
    agent=TEAM_5_AGENT,
    expected_output="Implemented features and tests"
)


# ============================================================================
# RUN ALL TEAMS
# ============================================================================

def run_team(crew: Crew, team_name: str):
    """Run a team and return results."""
    print(f"\n{'='*70}")
    print(f"🚀 Starting {team_name}...")
    print(f"{'='*70}")
    
    result = crew.kickoff()
    
    print(f"\n✅ {team_name} Complete!")
    return result


if __name__ == "__main__":
    print("🎯 Opus Orchestrator AI - CrewAI Development Teams")
    print("=" * 70)
    
    # Create crews
    crews = [
        (Crew(agents=[TEAM_1_AGENT], tasks=[TEAM_1_TASK], verbose=True), "Team 1: Critical Bugs"),
        (Crew(agents=[TEAM_2_AGENT], tasks=[TEAM_2_TASK], verbose=True), "Team 2: Agent/Workflow"),
        (Crew(agents=[TEAM_3_AGENT], tasks=[TEAM_3_TASK], verbose=True), "Team 3: Infrastructure"),
        (Crew(agents=[TEAM_4_AGENT], tasks=[TEAM_4_TASK], verbose=True), "Team 4: Architecture"),
        (Crew(agents=[TEAM_5_AGENT], tasks=[TEAM_5_TASK], verbose=True), "Team 5: Features"),
    ]
    
    # Run sequentially (can be parallelized if needed)
    results = []
    for crew, name in crews:
        try:
            result = run_team(crew, name)
            results.append((name, "SUCCESS", result))
        except Exception as e:
            results.append((name, "FAILED", str(e)))
            print(f"❌ {name} failed: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEAM SUMMARY")
    print("=" * 70)
    for name, status, _ in results:
        emoji = "✅" if status == "SUCCESS" else "❌"
        print(f"{emoji} {name}: {status}")
