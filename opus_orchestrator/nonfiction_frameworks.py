"""Nonfiction frameworks for Opus Orchestrator.

Rigorous nonfiction structures: Diátaxis, Technical Manual, Codebase Tour.
"""

from enum import Enum
from typing import Any


class NonfictionFramework(str, Enum):
    """Nonfiction book frameworks."""
    
    DIAXIS_TUTORIAL = "diataxis-tutorial"
    DIAXIS_HOWTO = "diataxis-howto"
    DIAXIS_EXPLANATION = "diataxis-explanation"
    DIAXIS_REFERENCE = "diataxis-reference"
    TECHNICAL_MANUAL = "technical-manual"
    CODEBASE_TOUR = "codebase-tour"
    API_DOCUMENTATION = "api-documentation"


# Diátaxis Framework Definitions
# Based on Daniele Procida's work - the gold standard for technical documentation

DIAXIS_TUTORIAL = {
    "name": "Diátaxis Tutorial",
    "description": "A tutorial is a lesson that leads the learner through a series of steps to complete a project. The learner learns by doing.",
    "stages": [
        "Introduction - What will we build and why?",
        "Prerequisites - What do you need before starting?",
        "Step 1: Setup - Getting the environment ready",
        "Step 2: First Steps - Your initial actions",
        "Step 3: Building - Creating something concrete",
        "Step 4: Enhancement - Adding features",
        "Step 5: Completion - Finishing the project",
        "Summary - What you learned",
        "Next Steps - Where to go from here",
    ],
    "structure": {
        "audience": "Learners who need guided, hands-on experience",
        "goal": "Complete a concrete project through step-by-step instruction",
        "approach": "Progressive disclosure - reveal complexity gradually",
        "tone": "Encouraging, clear, patient",
    },
}

DIAXIS_HOWTO = {
    "name": "Diátaxis How-To Guide",
    "description": "A how-to guide leads the reader through a series of steps to accomplish a goal. They already know what they want to do.",
    "stages": [
        "Goal Statement - What problem does this solve?",
        "Prerequisites - What's needed?",
        "Step 1 - First action",
        "Step 2 - Second action",
        "Step N - Final step",
        "Troubleshooting - Common issues",
        "Related Tasks - See also",
    ],
    "structure": {
        "audience": "Practitioners who know what they want to achieve",
        "goal": "Accomplish a specific, practical task",
        "approach": "Direct, efficient steps toward a goal",
        "tone": "Direct, authoritative, no fluff",
    },
}

DIAXIS_EXPLANATION = {
    "name": "Diátaxis Explanation",
    "description": "An explanation clarifies and deepens understanding of a topic. It provides context and connects concepts.",
    "stages": [
        "Overview - What are we exploring?",
        "Background - What do you need to know first?",
        "Core Concepts - The key ideas",
        "How It Works - Under the hood",
        "Different Approaches - Alternative perspectives",
        "Why It Matters - Significance",
        "Common Misconceptions - What people get wrong",
        "Further Reading - Deepen knowledge",
    ],
    "structure": {
        "audience": "Readers who want to understand, not just do",
        "goal": "Build mental models and deepen comprehension",
        "approach": "Multiple perspectives, rich context",
        "tone": "Thoughtful, explanatory, nuanced",
    },
}

DIAXIS_REFERENCE = {
    "name": "Diátaxis Reference",
    "description": "Reference documentation provides authoritative information about a system. Accurate, complete, findable.",
    "stages": [
        "Overview - What is this?",
        "Syntax - How to use it",
        "Parameters - What it accepts",
        "Returns - What it produces",
        "Examples - Usage patterns",
        "Errors - What can go wrong",
        "Notes - Important details",
        "See Also - Related topics",
    ],
    "structure": {
        "audience": "Users who need precise, detailed information",
        "goal": "Accurate, comprehensive information lookup",
        "approach": "Complete, organized, searchable",
        "tone": "Precise, technical, complete",
    },
}


# Technical Manual Framework
# Structured for learning technical subjects deeply

TECHNICAL_MANUAL = {
    "name": "Technical Manual",
    "description": "A comprehensive technical manual that takes readers from foundations to mastery with practical examples.",
    "stages": [
        "Part 1: Foundations",
        "  1. Introduction - Why this matters",
        "  2. Core Concepts - Essential background",
        "  3. Architecture - High-level design",
        "  4. Getting Started - First steps",
        "",
        "Part 2: Deep Dive",
        "  5. [Topic A] - In-depth exploration",
        "  6. [Topic B] - Implementation details",
        "  7. [Topic C] - Advanced features",
        "  8. [Topic D] - Edge cases",
        "",
        "Part 3: Practical Application",
        "  9. Hands-On Project - Build something",
        "  10. Best Practices - How experts do it",
        "  11. Debugging - When things go wrong",
        "  12. Performance - Optimization",
        "",
        "Part 4: Reference",
        "  13. API Reference - Complete API",
        "  14. Command Reference - All commands",
        "  15. Configuration - All options",
        "  16. Troubleshooting Guide - Common problems",
    ],
    "structure": {
        "audience": "Professionals needing comprehensive, practical knowledge",
        "goal": "Build expertise from ground up to mastery",
        "approach": "Theory → Practice → Reference spiral",
        "tone": "Professional, thorough, practical",
    },
}


# Codebase Tour Framework
# For documenting code directly

CODEBASE_TOUR = {
    "name": "Codebase Tour",
    "description": "Document a codebase systematically: structure → components → relationships → implementation → usage.",
    "stages": [
        "1. Repository Overview",
        "  - What is this project?",
        "  - What problem does it solve?",
        "  - Key technologies",
        "  - Directory structure",
        "",
        "2. High-Level Architecture",
        "  - System components",
        "  - Data flow",
        "  - Key abstractions",
        "",
        "3. Core Components",
        "  - Component A: Purpose, public API, key structs",
        "  - Component B: Purpose, public API, key structs",
        "  - Component C: Purpose, public API, key structs",
        "",
        "4. Data Structures",
        "  - Key structs and their fields",
        "  - Relationships between data types",
        "  - Memory layout if relevant",
        "",
        "5. Core Functions",
        "  - Main entry points",
        "  - Critical paths",
        "  - Algorithm implementations",
        "",
        "6. Interfaces",
        "  - How components communicate",
        "  - Public APIs",
        "  - Event/message systems",
        "",
        "7. Configuration",
        "  - Config files",
        "  - Environment variables",
        "  - Runtime parameters",
        "",
        "8. Testing",
        "  - Test strategies",
        "  - Key test files",
        "  - How to run tests",
        "",
        "9. Contributing",
        "  - Development setup",
        "  - Code style",
        "  - Pull request process",
    ],
    "structure": {
        "audience": "Developers who need to understand, use, or contribute to the codebase",
        "goal": "Map code to mental model accurately",
        "approach": "Top-down from architecture to implementation",
        "tone": "Technical, precise, code-focused",
    },
}


# API Documentation Framework
# For generating API docs from code

API_DOCUMENTATION = {
    "name": "API Documentation",
    "description": "Complete API reference documentation: endpoints, parameters, responses, examples, errors.",
    "stages": [
        "API Overview",
        "  - Introduction",
        "  - Authentication",
        "  - Rate Limiting",
        "  - Base URL",
        "",
        "Resources",
        "  - Each endpoint documented:",
        "    - Endpoint URL and method",
        "    - Description",
        "    - Path parameters",
        "    - Query parameters",
        "    - Request body schema",
        "    - Response schema",
        "    - Success codes",
        "    - Error codes",
        "    - Example request",
        "    - Example response",
        "",
        "Models",
        "  - Data models used",
        "  - Field definitions",
        "  - Type specifications",
        "",
        "Errors",
        "  - Error code reference",
        "  - Error message meanings",
        "  - Troubleshooting",
        "",
        "SDKs/Libraries",
        "  - Official libraries",
        "  - Community libraries",
        "",
        "Changelog",
        "  - Version history",
        "  - Breaking changes",
    ],
    "structure": {
        "audience": "Developers integrating with the API",
        "goal": "Complete, accurate reference for implementation",
        "approach": "Complete enumeration of all capabilities",
        "tone": "Technical, complete, unambiguous",
    },
}


# Registry of all nonfiction frameworks
NONFICTION_FRAMEWORKS = {
    NonfictionFramework.DIAXIS_TUTORIAL: DIAXIS_TUTORIAL,
    NonfictionFramework.DIAXIS_HOWTO: DIAXIS_HOWTO,
    NonfictionFramework.DIAXIS_EXPLANATION: DIAXIS_EXPLANATION,
    NonfictionFramework.DIAXIS_REFERENCE: DIAXIS_REFERENCE,
    NonfictionFramework.TECHNICAL_MANUAL: TECHNICAL_MANUAL,
    NonfictionFramework.CODEBASE_TOUR: CODEBASE_TOUR,
    NonfictionFramework.API_DOCUMENTATION: API_DOCUMENTATION,
}


def get_nonfiction_framework(framework: NonfictionFramework) -> dict[str, Any]:
    """Get a nonfiction framework by type."""
    return NONFICTION_FRAMEWORKS.get(framework, {})


def list_nonfiction_frameworks() -> dict[str, dict]:
    """List all available nonfiction frameworks."""
    return {
        k.value: {
            "name": v.get("name", k.value),
            "description": v.get("description", ""),
        }
        for k, v in NONFICTION_FRAMEWORKS.items()
    }
