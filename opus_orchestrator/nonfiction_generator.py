"""Nonfiction generator using rigorous frameworks.

Generate technical documentation using Diátaxis, Technical Manual, and Codebase Tour frameworks.
"""

import os
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()

from opus_orchestrator.nonfiction_frameworks import (
    NonfictionFramework,
    get_nonfiction_framework,
)
from opus_orchestrator.utils.llm import LLMClient
from opus_orchestrator.config import get_config


class NonfictionGenerator:
    """Generate nonfiction using rigorous frameworks."""
    
    def __init__(
        self,
        framework: NonfictionFramework = NonfictionFramework.TECHNICAL_MANUAL,
        topic: str = "",
        source_content: str = "",
        model: Optional[str] = None,
    ):
        """Initialize nonfiction generator.
        
        Args:
            framework: Nonfiction framework to use
            topic: Topic to document
            source_content: Source code/content to document
            model: Override model name
        """
        self.framework = framework
        self.topic = topic
        self.source_content = source_content
        
        config = get_config()
        self.llm = LLMClient(
            provider=config.agent.provider,
            model=model or config.agent.model,
        )
        
        self.framework_info = get_nonfiction_framework(framework)
    
    def generate(self, target_word_count: int = 5000) -> str:
        """Generate nonfiction document.
        
        Args:
            target_word_count: Target word count
            
        Returns:
            Generated document
        """
        if self.framework == NonfictionFramework.CODEBASE_TOUR:
            return self._generate_codebase_tour(target_word_count)
        elif self.framework == NonfictionFramework.TECHNICAL_MANUAL:
            return self._generate_technical_manual(target_word_count)
        elif self.framework == NonfictionFramework.DIAXIS_TUTORIAL:
            return self._generate_diataxis_tutorial(target_word_count)
        elif self.framework == NonfictionFramework.DIAXIS_HOWTO:
            return self._generate_diataxis_howto(target_word_count)
        elif self.framework == NonfictionFramework.DIAXIS_EXPLANATION:
            return self._generate_diataxis_explanation(target_word_count)
        elif self.framework == NonfictionFramework.DIAXIS_REFERENCE:
            return self._generate_diataxis_reference(target_word_count)
        else:
            return self._generate_technical_manual(target_word_count)
    
    def _generate_codebase_tour(self, target_word_count: int) -> str:
        """Generate codebase tour documentation."""
        source_summary = self.source_content[:10000] if self.source_content else "No source content provided"
        
        prompt = f"""Generate comprehensive CODEBASE TOUR documentation.

FRAMEWORK: Codebase Tour - Document a codebase systematically

TOPIC: {self.topic}

SOURCE CODE/CONTENT:
{source_summary}

Generate the following sections:
1. Repository Overview - What is this project, what problem does it solve?
2. High-Level Architecture - System components and data flow
3. Core Components - Purpose and API of main components
4. Data Structures - Key structs and relationships
5. Core Functions - Main entry points and algorithms
6. Interfaces - How components communicate
7. Configuration - Config files and options
8. Testing - Test strategies and key files
9. Contributing - Development setup and PR process

Write in a technical, precise tone. Be specific and use code examples.
Target approximately {target_word_count} words.
"""
        return self.llm.complete(
            system_prompt="You are an expert technical writer specializing in codebase documentation.",
            user_prompt=prompt,
            temperature=0.7,
        )
    
    def _generate_technical_manual(self, target_word_count: int) -> str:
        """Generate technical manual."""
        source_summary = self.source_content[:10000] if self.source_content else "No source content provided"
        
        prompt = f"""Generate a comprehensive TECHNICAL MANUAL.

FRAMEWORK: Technical Manual - From foundations to mastery

TOPIC: {self.topic}

SOURCE CONTENT:
{source_summary}

Generate a technical manual with:
1. Introduction - Why this topic matters
2. Core Concepts - Essential background knowledge
3. Architecture - High-level system design
4. Getting Started - First steps for beginners
5. Deep Dive Sections - Detailed exploration of key topics
6. Practical Examples - Hands-on code examples
7. Best Practices - How experts do it
8. Troubleshooting - Common problems and solutions
9. Reference - API/command reference

Write in a professional, thorough, practical tone.
Target approximately {target_word_count} words.
"""
        return self.llm.complete(
            system_prompt="You are an expert technical writer specializing in technical manuals and educational content.",
            user_prompt=prompt,
            temperature=0.7,
        )
    
    def _generate_diataxis_tutorial(self, target_word_count: int) -> str:
        """Generate Diátaxis tutorial."""
        prompt = f"""Generate a DIÁTEXIS TUTORIAL.

FRAMEWORK: Tutorial - Learn by doing a concrete project

TOPIC: {self.topic}

Generate a tutorial that leads the learner through a complete project:
1. Introduction - What will we build and why?
2. Prerequisites - What do you need before starting?
3. Step 1: Setup - Getting the environment ready
4. Step 2: First Steps - Your initial actions  
5. Step 3: Building - Creating something concrete
6. Step 4: Enhancement - Adding features
7. Step 5: Completion - Finishing the project
8. Summary - What you learned
9. Next Steps - Where to go from here

Write in an encouraging, clear, patient tone.
Use numbered steps. Make it achievable for beginners.
Target approximately {target_word_count} words.
"""
        return self.llm.complete(
            system_prompt="You are an expert technical educator specializing in tutorials.",
            user_prompt=prompt,
            temperature=0.7,
        )
    
    def _generate_diataxis_howto(self, target_word_count: int) -> str:
        """Generate Diátaxis how-to guide."""
        prompt = f"""Generate a DIÁTEXIS HOW-TO GUIDE.

FRAMEWORK: How-To Guide - Accomplish a specific task

TOPIC: {self.topic}

Generate a practical how-to guide:
1. Goal Statement - What problem does this solve?
2. Prerequisites - What's needed?
3. Step 1 - First action
4. Step 2 - Second action
5. Step N - Final step
6. Troubleshooting - Common issues
7. Related Tasks - See also

Write in a direct, authoritative tone. No fluff.
Target approximately {target_word_count} words.
"""
        return self.llm.complete(
            system_prompt="You are an expert technical writer specializing in how-to guides.",
            user_prompt=prompt,
            temperature=0.7,
        )
    
    def _generate_diataxis_explanation(self, target_word_count: int) -> str:
        """Generate Diátaxis explanation."""
        prompt = f"""Generate a DIÁTEXIS EXPLANATION.

FRAMEWORK: Explanation - Clarify and deepen understanding

TOPIC: {self.topic}

Generate an explanatory document:
1. Overview - What are we exploring?
2. Background - What do you need to know first?
3. Core Concepts - The key ideas
4. How It Works - Under the hood
5. Different Approaches - Alternative perspectives
6. Why It Matters - Significance
7. Common Misconceptions - What people get wrong
8. Further Reading - Deepen knowledge

Write in a thoughtful, explanatory tone. Build mental models.
Target approximately {target_word_count} words.
"""
        return self.llm.complete(
            system_prompt="You are an expert educator specializing in explanatory writing.",
            user_prompt=prompt,
            temperature=0.7,
        )
    
    def _generate_diataxis_reference(self, target_word_count: int) -> str:
        """Generate Diátaxis reference."""
        prompt = f"""Generate DIÁTEXIS REFERENCE documentation.

FRAMEWORK: Reference - Accurate, complete information lookup

TOPIC: {self.topic}

Generate reference documentation:
1. Overview - What is this?
2. Syntax - How to use it
3. Parameters - What it accepts
4. Returns - What it produces
5. Examples - Usage patterns
6. Errors - What can go wrong
7. Notes - Important details
8. See Also - Related topics

Write in a precise, technical, complete tone.
Target approximately {target_word_count} words.
"""
        return self.llm.complete(
            system_prompt="You are an expert technical writer specializing in reference documentation.",
            user_prompt=prompt,
            temperature=0.7,
        )


def create_nonfiction_generator(
    framework: NonfictionFramework = NonfictionFramework.TECHNICAL_MANUAL,
    topic: str = "",
    source_content: str = "",
) -> NonfictionGenerator:
    """Factory function to create a nonfiction generator."""
    return NonfictionGenerator(
        framework=framework,
        topic=topic,
        source_content=source_content,
    )
