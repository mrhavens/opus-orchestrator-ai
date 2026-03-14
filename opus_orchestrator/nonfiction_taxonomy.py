"""Nonfiction Framework Taxonomy for Opus Orchestrator.

Purpose × Structure Matrix for intelligent framework selection.

This module provides the meta-structure for organizing nonfiction frameworks
by reader PURPOSE (why they're reading) and STRUCTURAL PATTERN (how it's organized).
"""

from enum import Enum
from typing import Optional


class ReaderPurpose(str, Enum):
    """Why is the reader reading this book?
    
    This determines the TYPE of experience and VALUE they expect.
    """
    LEARN_HANDS_ON = "learn_hands_on"      # "I want to DO something"
    UNDERSTAND = "understand"               # "I want to GRASP a concept"
    TRANSFORM = "transform"                  # "I want to CHANGE myself"
    DECIDE = "decide"                       # "I want to make a decision"
    REFERENCE = "reference"                 # "I want to LOOK something up"
    BE_INSPIRED = "be_inspired"             # "I want to feel something"
    BE_ENTERTAINED = "be_entertained"       # "I want to enjoy this"


class StructuralPattern(str, Enum):
    """How is the content ORGANIZED?
    
    This determines the scaffolding and flow.
    """
    SEQUENTIAL = "sequential"               # Step 1 → Step 2 → Step 3
    NARRATIVE = "narrative"                # Beginning → Middle → End
    PROBLEM_SOLUTION = "problem_solution"  # Pain → Solution → Evidence
    COMPARATIVE = "comparative"            # A vs B, then vs now
    SPIRAL = "spiral"                      # Simple → Complex → Simple
    MODULAR = "modular"                     # Standalone chapters, any order
    ARGUMENT = "argument"                   # Claim → Evidence → Rebuttal


class NonfictionCategory(str, Enum):
    """HIGH-LEVEL SUBJECT DOMAIN
    
    This determines vocabulary and expertise needed.
    """
    BUSINESS = "business"
    LEADERSHIP = "leadership"
    ENTREPRENEURSHIP = "entrepreneurship"
    SELF_HELP = "self_help"
    MEMOIR = "memoir"
    PHILOSOPHY = "philosophy"
    SCIENCE = "science"
    HISTORY = "history"
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTH = "health"
    RELATIONSHIPS = "relationships"
    CREATIVITY = "creativity"
    SPIRITUALITY = "spirituality"
    HOW_TO = "how_to"
    EDUCATION = "education"
    ACADEMIC = "academic"
    RPG = "rpg"


# ============================================================================
# PURPOSE × STRUCTURE MATRIX
# ============================================================================

# This is the intelligence: which frameworks work for which purposes

PURPOSE_STRUCTURE_MATRIX = {
    ReaderPurpose.LEARN_HANDS_ON: {
        "preferred_patterns": [StructuralPattern.SEQUENTIAL, StructuralPattern.SPIRAL],
        "framework_families": ["tutorial", "howto", "step_by_step"],
        "stage_emphasis": "exercises, practice, milestones",
    },
    ReaderPurpose.UNDERSTAND: {
        "preferred_patterns": [StructuralPattern.SPIRAL, StructuralPattern.COMPARATIVE],
        "framework_families": ["explanation", "concept", "analogy"],
        "stage_emphasis": "examples, mental models, analogies",
    },
    ReaderPurpose.TRANSFORM: {
        "preferred_patterns": [StructuralPattern.NARRATIVE, StructuralPattern.PROBLEM_SOLUTION],
        "framework_families": ["journey", "transformation", "memoir"],
        "stage_emphasis": "emotional arc, before/after, proof of change",
    },
    ReaderPurpose.DECIDE: {
        "preferred_patterns": [StructuralPattern.ARGUMENT, StructuralPattern.COMPARATIVE],
        "framework_families": ["big_idea", "case_study", "evidence_based"],
        "stage_emphasis": "data, proof, tradeoffs, recommendations",
    },
    ReaderPurpose.REFERENCE: {
        "preferred_patterns": [StructuralPattern.MODULAR, StructuralPattern.SEQUENTIAL],
        "framework_families": ["reference", "technical_manual", "api_docs"],
        "stage_emphasis": "completeness, findability, accuracy",
    },
    ReaderPurpose.BE_INSPIRED: {
        "preferred_patterns": [StructuralPattern.NARRATIVE, StructuralPattern.COMPARATIVE],
        "framework_families": ["biography", "visionary", "manifesto"],
        "stage_emphasis": "vision, emotion, memorable moments",
    },
}


# ============================================================================
# FRAMEWORK DEFINITIONS
# ============================================================================

# Each framework has: purpose, structure, stages, prompts

NONFICTION_FRAMEWORKS = {
    # ---------------------------------------------------------------------
    # LEARN_HANDS_ON (Tutorials, How-To)
    # ---------------------------------------------------------------------
    "tutorial": {
        "name": "Tutorial",
        "description": "Guided learning by doing - complete a project",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "stages": [
            "Welcome - What will you build and why?",
            "Prerequisites - What do you need first?",
            "Setup - Get your environment ready",
            "Step 1 - Your first action",
            "Step 2 - Build on Step 1",
            "Step 3 - Add complexity",
            "Step 4 - Debug/fix issues",
            "Completion - You did it!",
            "Next Steps - Where to go next",
        ],
        "prompt_template": "Write a tutorial that leads learners through {project} to achieve {outcome}. Include specific steps, code examples, and checkpoints.",
    },
    
    "howto": {
        "name": "How-To Guide",
        "description": "Accomplish a specific goal - reader knows what they want",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "stages": [
            "Before You Start - Prerequisites",
            "The Method - Core approach",
            "Step 1 - First action",
            "Step 2 - Build on Step 1", 
            "Step N - Final step",
            "Troubleshooting - Common issues",
            "Related Tasks - See also",
        ],
        "prompt_template": "Write a how-to guide for {goal}. Reader already knows what they want - give them direct steps.",
    },

    # ---------------------------------------------------------------------
    # UNDERSTAND (Explanations, Concepts)
    # ---------------------------------------------------------------------
    "concept_explainer": {
        "name": "Concept Explainer",
        "description": "Build deep understanding through analogies and examples",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.SPIRAL,
        "stages": [
            "The Hook - Why this matters",
            "What It Is - Simple definition",
            "The Mental Model - Analogy for understanding",
            "How It Works - Mechanism",
            "Why It Works - Deep dive",
            "Common Misconceptions - What people get wrong",
            "Real Examples - Case studies",
            "Connected Ideas - Related concepts",
        ],
        "prompt_template": "Explain {concept} to a reader who wants to truly understand it. Use vivid analogies, counterexamples, and build a mental model.",
    },

    "compare_contrast": {
        "name": "Compare & Contrast",
        "description": "Understand by comparing alternatives",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.COMPARATIVE,
        "stages": [
            "The Question - Why compare these?",
            "Option A - Deep dive",
            "Option B - Deep dive", 
            "Side-by-Side - Direct comparison table",
            "Trade-offs - What you gain/lose with each",
            "Recommendation - When to choose what",
        ],
        "prompt_template": "Compare {option_a} vs {option_b}. Help reader understand differences deeply and choose wisely.",
    },

    # ---------------------------------------------------------------------
    # TRANSFORM (Self-Help, Memoir)
    # ---------------------------------------------------------------------
    "transformation_journey": {
        "name": "Transformation Journey",
        "description": "Take reader from stuck to transformed",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.NARRATIVE,
        "stages": [
            "The Wake-Up - Recognize the problem",
            "Denial - Why we resist change",
            "The Dark Night - Lowest point",
            "The Realization - Key insight",
            "The Path - How to change",
            "Struggles & Setbacks - Realistic journey",
            "Breakthrough - The shift",
            "New Normal - How life is different",
            "Call to Action - Start now",
        ],
        "prompt_template": "Write a transformation narrative that helps readers go from {stuck_state} to {transformed_state}. Include emotional honesty and practical steps.",
    },

    "mountain_structure": {
        "name": "Mountain Structure",
        "description": "Classic narrative arc - normal → crisis → resolution",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.NARRATIVE,
        "stages": [
            "Ordinary World - Life before",
            "The Call - Something changes",
            "Refusal - Why resist",
            "Crossing the Threshold - Commitment",
            "Tests and Allies - Who helps",
            "The Ordeal - Biggest challenge",
            "The Reward - What was gained",
            "The Road Back - Bringing it home",
            "Return with Elixir - Changed person",
        ],
        "prompt_template": "Write using the hero's journey structure applied to {topic}. Make it emotionally resonant and transformation-focused.",
    },

    "atomic_habits_style": {
        "name": "Atomic Habits Framework",
        "description": "Identity-based habit change",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.SEQUENTIAL,
        "stages": [
            "The Surprising Power of Atomic Habits",
            "The First Law - Make it Obvious",
            "The Second Law - Make it Attractive",
            "The Third Law - Make it Easy",
            "The Fourth Law - Make it Satisfying",
            "Advanced Tactics - Habit stacking, temptation bundling",
            "The Inside Story - How it really works",
            "The Outer World - How to make it stick",
        ],
        "prompt_template": "Write a habit-change book using identity-based framework. Focus on small changes that compound into big transformation.",
    },

    # ---------------------------------------------------------------------
    # DECIDE (Business, Leadership)
    # ---------------------------------------------------------------------
    "big_idea": {
        "name": "Big Idea Framework",
        "description": "One core insight, proven thoroughly",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "stages": [
            "The Captivating Promise - What's the big idea?",
            "The Opposition - What does conventional wisdom say?",
            "The Evidence - Proof from multiple sources",
            "The Implications - What does this mean?",
            "The Counter-Arguments - Address skeptics",
            "The Conclusion - What to do now",
        ],
        "prompt_template": "Present the big idea: {idea}. Challenge conventional wisdom, provide compelling evidence, lead to action.",
    },

    "problem_solution": {
        "name": "Problem-Solution Framework",
        "description": "Pain → Solution → Proof → Action",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.PROBLEM_SOLUTION,
        "stages": [
            "The Problem - Paint the pain vividly",
            "The Root Cause - Why it's happening",
            "The Solution - Your methodology",
            "The Evidence - Case studies and data",
            "The Transformation - Before and after",
            "The Call to Action - What to do now",
        ],
        "prompt_template": "Write a problem-solution book. Make the pain real, present your solution with proof, drive to action.",
    },

    "case_study": {
        "name": "Case Study Collection",
        "description": "Real examples prove the point",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.COMPARATIVE,
        "stages": [
            "The Question - What are we exploring?",
            "Case 1 - Deep dive",
            "Case 2 - Deep dive",
            "Case 3 - Deep dive",
            "Patterns - What worked and why",
            "Framework - Generalizable principles",
            "Application - How to apply",
        ],
        "prompt_template": "Build your argument through {n} detailed case studies. Let real examples prove your point.",
    },

    # ---------------------------------------------------------------------
    # REFERENCE (Technical)
    # ---------------------------------------------------------------------
    "diataxis_tutorial": {
        "name": "Diátaxis Tutorial",
        "description": "Learn by doing a project",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "stages": [
            "Introduction - What will we build?",
            "Prerequisites - What you need",
            "Step 1: Setup",
            "Step 2: First steps",
            "Step 3: Building",
            "Step 4: Enhancing",
            "Step 5: Completion",
            "Summary",
            "Next Steps",
        ],
    },

    "diataxis_howto": {
        "name": "Diátaxis How-To",
        "description": "Accomplish a specific task",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "stages": [
            "Goal Statement",
            "Prerequisites",
            "Step 1", "Step 2", "Step N",
            "Troubleshooting",
            "Related Tasks",
        ],
    },

    "diataxis_explanation": {
        "name": "Diátaxis Explanation",
        "description": "Deep understanding of a topic",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.SPIRAL,
        "stages": [
            "Overview",
            "Background",
            "Core Concepts",
            "How It Works",
            "Different Approaches",
            "Why It Matters",
            "Common Misconceptions",
            "Further Reading",
        ],
    },

    "diataxis_reference": {
        "name": "Diátaxis Reference",
        "description": "Complete, accurate reference",
        "purpose": ReaderPurpose.REFERENCE,
        "structure": StructuralPattern.MODULAR,
        "stages": [
            "Overview",
            "Syntax",
            "Parameters",
            "Returns",
            "Examples",
            "Errors",
            "Notes",
            "See Also",
        ],
    },
}


# ============================================================================
# THE INTELLIGENT SELECTOR
# ============================================================================

def select_framework(
    purpose: ReaderPurpose,
    category: Optional[NonfictionCategory] = None,
    user_preferred_framework: Optional[str] = None,
) -> dict:
    """Intelligently select the best framework based on purpose and category.
    
    Args:
        purpose: Why is the reader reading?
        category: What domain? (optional - for vocabulary)
        user_preferred_framework: User explicitly chose one
        
    Returns:
        Framework definition with prompts and stages
    """
    # If user specified, try to use it
    if user_preferred_framework and user_preferred_framework in NONFICTION_FRAMEWORKS:
        return NONFICTION_FRAMEWORKS[user_preferred_framework]
    
    # Otherwise, use the matrix to select
    if purpose not in PURPOSE_STRUCTURE_MATRIX:
        # Default fallback
        return NONFICTION_FRAMEWORKS["concept_explainer"]
    
    matrix_entry = PURPOSE_STRUCTURE_MATRIX[purpose]
    framework_families = matrix_entry["framework_families"]
    
    # Find best match
    for family in framework_families:
        for key, fw in NONFICTION_FRAMEWORKS.items():
            if family.lower() in fw.get("name", "").lower():
                return fw
    
    # Ultimate fallback
    return NONFICTION_FRAMEWORKS["concept_explainer"]


def get_frameworks_for_purpose(purpose: ReaderPurpose) -> list[dict]:
    """Get all frameworks that work for a purpose."""
    if purpose not in PURPOSE_STRUCTURE_MATRIX:
        return []
    
    matrix_entry = PURPOSE_STRUCTURE_MATRIX[purpose]
    families = matrix_entry["framework_families"]
    
    results = []
    for key, fw in NONFICTION_FRAMEWORKS.items():
        if any(f in fw.get("name", "").lower() for f in families):
            results.append({"id": key, **fw})
    
    return results


def describe_purpose(purpose: ReaderPurpose) -> dict:
    """Get description of what a purpose means for the reader."""
    descriptions = {
        ReaderPurpose.LEARN_HANDS_ON: {
            "reader_thinks": "I want to DO something specific",
            "value_received": "Skills I can use immediately",
            "emotion": "Accomplished, capable",
            "length_typical": "Short to medium (5-30k words)",
        },
        ReaderPurpose.UNDERSTAND: {
            "reader_thinks": "I want to GRASP how something works",
            "value_received": "Mental models and deep understanding",
            "emotion": "Enlightened, informed",
            "length_typical": "Medium (20-60k words)",
        },
        ReaderPurpose.TRANSFORM: {
            "reader_thinks": "I want to CHANGE myself or my life",
            "value_received": "A path to becoming different",
            "emotion": "Hopeful, motivated, understood",
            "length_typical": "Medium to long (30-80k words)",
        },
        ReaderPurpose.DECIDE: {
            "reader_thinks": "I need to make a decision or choice",
            "value_received": "Clarity and confidence in choice",
            "emotion": "Empowered, informed",
            "length_typical": "Short to medium (10-40k words)",
        },
        ReaderPurpose.REFERENCE: {
            "reader_thinks": "I need to LOOK something up",
            "value_received": "Accurate information, fast",
            "emotion": "Efficient, relieved",
            "length_typical": "Variable (manual size)",
        },
    }
    return descriptions.get(purpose, {})
