#!/usr/bin/env python3
"""
Opus Orchestrator AI - CrewAI Development Teams
================================================
Divides 17 issues into 5 specialized teams, creates branches,
and assigns work.
"""

TEAMS = {
    "team-1-critical-bugs": {
        "name": "Critical Bug Fix Squad",
        "description": "Fixes blocking bugs that prevent the system from running",
        "issues": [
            "#1 - LLM Client self.client undefined (async methods)",
            "#3 - Server Upload missing UploadFile/File imports",
            "#17 - LangGraph workflow error recovery (fake fallback)",
        ],
        "priority": "CRITICAL",
        "files_to_fix": [
            "opus_orchestrator/utils/llm.py",
            "opus_orchestrator/server.py",
            "opus_orchestrator/langgraph_workflow.py",
        ]
    },
    "team-2-agent-workflow": {
        "name": "Agent & Workflow Repair Crew",
        "description": "Fixes agent behavior and workflow logic issues",
        "issues": [
            "#2 - AutoGen critique loop never revises chapters",
            "#5 - CrewAI LLM factory ignores config parameters",
        ],
        "priority": "HIGH",
        "files_to_fix": [
            "opus_orchestrator/autogen_critique.py",
            "opus_orchestrator/crews/base_crew.py",
        ]
    },
    "team-3-infrastructure": {
        "name": "Infrastructure & Config Team",
        "description": "Improves configuration, error handling, and infrastructure",
        "issues": [
            "#4 - GitHub Ingestor requires token for public repos",
            "#14 - Silent failures when API keys missing",
            "#10 - Add rate limiting and cost controls",
        ],
        "priority": "MEDIUM",
        "files_to_fix": [
            "opus_orchestrator/utils/github_ingest.py",
            "opus_orchestrator/config.py",
            "opus_orchestrator/orchestrator.py",
        ]
    },
    "team-4-architecture": {
        "name": "Architecture & Design Squad",
        "description": "Refactors design issues and consolidates duplicate code",
        "issues": [
            "#6 - Duplicate state management (OpusState vs OpusGraphState)",
            "#11 - No structured output validation from agents",
            "#12 - Duplicate framework prompt systems",
        ],
        "priority": "MEDIUM",
        "files_to_fix": [
            "opus_orchestrator/state.py",
            "opus_orchestrator/langgraph_state.py",
            "opus_orchestrator/agents/base.py",
            "opus_orchestrator/frameworks.py",
            "opus_orchestrator/orchestrator.py",
        ]
    },
    "team-5-features": {
        "name": "Features & Polish Team",
        "description": "Implements missing features and polish items",
        "issues": [
            "#7 - Add test suite for core functionality",
            "#8 - Implement streaming for long-running generations",
            "#9 - Enable LangGraph state persistence (checkpointing)",
            "#13 - Giant monolith files need refactoring",
            "#15 - Research agent disconnected from main flow",
            "#16 - Nonfiction support underdeveloped",
        ],
        "priority": "LOW",
        "files_to_fix": [
            "tests/",
            "opus_orchestrator/server.py",
            "opus_orchestrator/langgraph_workflow.py",
            "tests/test_orchestrator.py",
            "opus_orchestrator/cli.py",
            "opus_orchestrator/orchestrator.py",
        ]
    }
}

for team_id, team in TEAMS.items():
    print(f"\n{'='*70}")
    print(f"🚂 TEAM: {team['name']}")
    print(f"   Priority: {team['priority']}")
    print(f"   Description: {team['description']}")
    print(f"\n   Issues:")
    for issue in team['issues']:
        print(f"      • {issue}")
    print(f"\n   Files to fix:")
    for f in team['files_to_fix']:
        print(f"      • {f}")
