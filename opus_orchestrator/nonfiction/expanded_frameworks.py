"""Expanded Nonfiction Frameworks - The Best of the Best.

A comprehensive library of 35+ expert-level nonfiction frameworks
from the world's top practitioners, thinkers, and authors.

Each framework is designed for a specific purpose and structure,
with detailed prompts for generating world-class content.
"""

from opus_orchestrator.nonfiction_taxonomy import (
    ReaderPurpose,
    StructuralPattern,
    NonfictionCategory,
)


# =============================================================================
# EXPANDED FRAMEWORK LIBRARY
# =============================================================================

EXPANDED_FRAMEWORKS = {
    
    # ==========================================================================
    # BUSINESS & LEADERSHIP
    # ==========================================================================
    
    "big_idea": {
        "name": "Big Idea Framework",
        "description": "Jim Collins' methodology - one core insight, proven thoroughly. The book is built around a single revolutionary idea that challenges conventional wisdom.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "The Promise - What is the Big Idea?",
            "The Setting - Where does this idea fit?",
            "The Opposition - What does conventional wisdom say?",
            "The Evidence - Three proof points",
            "The Implications - What does this mean?",
            "The Counter-Arguments - Addressing skeptics",
            "The Adaptation - How to apply in different contexts",
            "The Conclusion - What to do starting today",
        ],
        "prompt_template": """Write a Big Idea book around {big_idea}. 

The Big Idea should:
- Challenge conventional wisdom
- Be defensible with evidence
- Have practical implications
- Be memorable and quotable

Structure: Promise → Opposition → Evidence → Implications → Application""",
        "tone_guidance": "Authoritative but humble. Confident without being arrogant. Data-driven but accessible. Like Jim Collins or Clayton Christensen.",
        "typical_length": "25,000-40,000 words",
        "audience": "Business leaders, entrepreneurs, strategists",
        "key_elements": ["Big Idea statement", "Evidence from multiple sources", "Practical applications", "Counter-argument handling"],
    },
    
    "one_thing": {
        "name": "The One Thing",
        "description": "Focus on the single most important thing. The premise: success is built by doing one thing exceptionally well.",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "The Myth - What most people get wrong",
            "The Truth - The one thing that matters",
            "The Proof - It's true because...",
            "The Obstacles - What gets in the way",
            "The Discipline - How to stay focused",
            "The Practice - Daily habits",
            "The Measurement - Tracking progress",
            "The Legacy - What you're building",
        ],
        "prompt_template": "Write a book about focusing on the one thing that matters most. Help readers cut through noise and prioritize.",
        "tone_guidance": "Direct, motivational, practical. No fluff. Like Gary Keller or James Clear.",
        "typical_length": "20,000-30,000 words",
        "audience": "Busy professionals, entrepreneurs",
    },
    
    "blue_ocean": {
        "name": "Blue Ocean Strategy",
        "description": "Create uncontested market space. Move from competing to creating.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "The Red Ocean - Competition as given",
            "The Blue Ocean - Creating new space",
            "The Six Paths - Where to look",
            "The Four Actions - Eliminate, Reduce, Raise, Create",
            "The Sequence - Build right",
            "Fair Process - Make it happen",
            "Overcoming Obstacles - Internal resistance",
            "Launch - Get to market",
        ],
        "prompt_template": "Write a Blue Ocean book about creating new market space. Help readers escape competition.",
        "tone_guidance": "Strategic, analytical, visionary. Like Chan Kim or Roger Martin.",
    },
    
    "four_disciplines": {
        "name": "Four Disciplines of Execution",
        "description": "4DX - Achieving wildly important goals. Focus, leverage, accountability, cadence.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "Discipline 1: Wildly Important Goal",
            "Discipline 2: Act on Lead Measures",
            "Discipline 3: Keep a Compelling Scoreboard",
            "Discipline 4: Create a Cadence of Accountability",
            "Putting It All Together",
            "Common Pitfalls",
            "Making It Stick",
        ],
        "prompt_template": "Write a practical book on the Four Disciplines of Execution for achieving goals.",
    },
    
    "good_to_great": {
        "name": "Good to Great",
        "description": "Level 5 Leadership and the Hedgehog Concept. Building enduring great companies.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.LEADERSHIP,
        "stages": [
            "Level 5 Leadership",
            "First Who, Then What",
            "Confront the Brutal Facts",
            "The Hedgehog Concept",
            "Culture of Discipline",
            "Technology Accelerators",
            "The Flywheel Effect",
            "From Good to Great to Built to Last",
        ],
        "prompt_template": "Write about transforming good organizations into great ones. Focus on Level 5 leadership.",
    },
    
    # ==========================================================================
    # MEMOIR & PERSONAL NARRATIVE
    # ==========================================================================
    
    "mountain_memoir": {
        "name": "Mountain Structure Memoir",
        "description": "The hero's journey adapted for memoir. Classic narrative arc with transformation at the core.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.MEMOIR,
        "stages": [
            "The Ordinary World - Life before",
            "The Call - Something changes",
            "Refusal - Why resist",
            "Crossing the Threshold - Commitment",
            "Tests, Allies, Enemies - Who helps, who hinders",
            "The Ordeal - The biggest challenge",
            "The Reward - What was gained",
            "The Road Back - Bringing it home",
            "Return with Elixir - Changed person",
        ],
        "prompt_template": "Write a memoir using the hero's journey structure. Show transformation through vivid narrative.",
        "tone_guidance": "Vivid, sensory, emotionally honest. Like a great novel but true.",
        "typical_length": "50,000-80,000 words",
    },
    
    "loss_and_gain": {
        "name": "Loss and Gain Framework",
        "description": "What was lost → The journey → What was gained. A powerful structure for any transformation story.",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.MEMOIR,
        "stages": [
            "What Was Lost - The before state",
            "The Moment of Loss - When it happened",
            "The Grieving - Processing the loss",
            "The Search - Looking for answers",
            "The Discovery - What was found",
            "The Struggle - Not easy",
            "The Gain - What was transformed",
            "The Gift - What was learned",
        ],
        "prompt_template": "Write a transformation memoir structured around loss and gain. Include the struggle.",
    },
    
    "scene_driven_memoir": {
        "name": "Scene-Driven Memoir",
        "description": "Vivid scenes connected by theme. Show, don't tell. Let moments reveal meaning.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.MEMOIR,
        "stages": [
            "Opening Scene - A moment that matters",
            "Scene 2 - Building the pattern",
            "Scene 3 - Deepening understanding",
            "Scene 4 - The turning point",
            "Scene 5 - Aftermath and meaning",
            "Scene 6 - The new normal",
            "Closing Scene - The echo of opening",
        ],
        "prompt_template": "Write a memoir built around vivid scenes. Let moments do the work. Show, don't tell.",
    },
    
    "single_moment_pivot": {
        "name": "Single-Moment Pivot",
        "description": "One moment changes everything. Build around the pivotal instant.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.MEMOIR,
        "stages": [
            "Before the Moment - Who you were",
            "The Moment - The pivot instant",
            "The Aftermath - Everything changed",
            "Making Sense - Understanding what happened",
            "Living It - The new reality",
            "The Ongoing Story - Still becoming",
        ],
        "prompt_template": "Write a memoir built around one pivotal moment that changed everything.",
    },
    
    "addiction_recovery": {
        "name": "Addiction & Recovery Memoir",
        "description": "The specific structure for addiction and recovery stories. Honesty about struggle and hope for transformation.",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.MEMOIR,
        "stages": [
            "The First Drink/Use - Before it took hold",
            "The Descent - It gets worse",
            "The Bottom - The breaking point",
            "The Decision - Getting help",
            "The Hard Work - Recovery isn't easy",
            "The Relapse - Sometimes it takes multiple tries",
            "The Long Road - Maintenance",
            "The Gift - What recovery gave back",
        ],
        "prompt_template": "Write an addiction and recovery memoir with unflinching honesty about the struggle.",
    },
    
    # ==========================================================================
    # PHILOSOPHY & IDEAS
    # ==========================================================================
    
    "socratic_method": {
        "name": "Socratic Method",
        "description": "Question → Answer → Follow-up → Deeper truth. The ancient method for exploring ideas.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.SPIRAL,
        "category": NonfictionCategory.PHILOSOPHY,
        "stages": [
            "The Question - What are we really asking?",
            "First Answer - Initial response",
            "Follow-Up 1 - Testing the answer",
            "Follow-Up 2 - The deeper question",
            "Paradox - The tension emerges",
            "Exploration - Living with the paradox",
            "Resolution - Not answers, but better questions",
            "The Final Question - What this opens up",
        ],
        "prompt_template": "Write a philosophical exploration using the Socratic method. Questions over answers.",
    },
    
    "argumentative_essay": {
        "name": "Argumentative Essay",
        "description": "Classic academic structure: Thesis → Evidence → Counterargument → Rebuttal → Conclusion.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.PHILOSOPHY,
        "stages": [
            "The Thesis - What you're arguing",
            "Context - Why it matters now",
            "Evidence Point 1 - First proof",
            "Evidence Point 2 - Second proof",
            "The Counter-Argument - The strongest objection",
            "The Rebuttal - Addressing objections",
            "Implications - What follows",
            "Conclusion - What to believe and do",
        ],
        "prompt_template": "Write an argumentative essay. State your position clearly, address objections fairly.",
    },
    
    "danish_philosopher": {
        "name": "Danish Philosopher Style",
        "description": "Kierkegaard-style: Paradox → Exploration → Resolution. Embrace the tension.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.SPIRAL,
        "category": NonfictionCategory.PHILOSOPHY,
        "stages": [
            "The Paradox - The apparent contradiction",
            "First Position - One side explored",
            "Second Position - The opposite explored",
            "The Leap - Moving beyond either/or",
            "The Resolution - Not compromise, transcendence",
            "Living It - Practical implications",
            "The Eternal - Connecting to larger meaning",
        ],
        "prompt_template": "Write a philosophical exploration that embraces paradox. Don't resolve too quickly.",
    },
    
    "thought_leader": {
        "name": "Thought Leader Framework",
        "description": "Contrarian idea → Evidence → Call to action. Establish authority through original thinking.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "The Contrarian View - What everyone believes",
            "The Problem - Why that view is wrong",
            "The New Perspective - Your alternative",
            "The Evidence - Proof from multiple angles",
            "The Implications - What this means",
            "The Call to Action - What to do differently",
            "The Future - Where this leads",
        ],
        "prompt_template": "Write a thought leadership book with a contrarian thesis. Challenge assumptions.",
    },
    
    # ==========================================================================
    # SCIENCE & EXPLANATION
    # ==========================================================================
    
    "discovery_narrative": {
        "name": "Discovery Narrative",
        "description": "Question → Journey → Answer → Implications. How we learned what we know.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.SCIENCE,
        "stages": [
            "The Question - What we didn't know",
            "The Search - Looking for answers",
            "The Discovery - The breakthrough moment",
            "The Evidence - How we verified",
            "The Debates - Controversies along the way",
            "The Current State - What we know now",
            "The Implications - What this opens",
            "The Mysteries - What we still don't know",
        ],
        "prompt_template": "Write about a scientific discovery as a narrative. The journey matters.",
    },
    
    "experiment_story": {
        "name": "Personal Experiment",
        "description": "I tried X to see what would happen. Personal research with universal lessons.",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.SCIENCE,
        "stages": [
            "The Hypothesis - What I wanted to test",
            "The Method - How I did it",
            "The Results - What happened",
            "The Analysis - What it means",
            "The Failures - What didn't work",
            "The Surprises - Unexpected findings",
            "The Conclusions - What I'd do differently",
            "The Application - What this means for you",
        ],
        "prompt_template": "Write about a personal experiment. Document the process honestly. Include failures.",
    },
    
    "explainer": {
        "name": "The Explainer",
        "description": "Steven Pinker style: Concept → Examples → Mechanism → Significance. Make complex ideas accessible.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.SPIRAL,
        "category": NonfictionCategory.SCIENCE,
        "stages": [
            "The Concept - What is it?",
            "Why It Matters - Why should we care?",
            "The Examples - Making it concrete",
            "The Mechanism - How it works",
            "The Evidence - What proves this?",
            "The Misconceptions - What's wrong",
            "The Significance - Why it matters more",
            "The Questions - What remains",
        ],
        "prompt_template": "Explain a complex concept accessibly. Examples first, then mechanism, then significance.",
    },
    
    "mental_models": {
        "name": "Mental Models Framework",
        "description": "Teach thinking tools. Each chapter = one model for better decisions.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "Why Mental Models Matter",
            "Model 1: First Principles",
            "Model 2: Inversion",
            "Model 3: Second-Order Thinking",
            "Model 4: The Map Is Not the Territory",
            "Model 5: Circle of Competence",
            "Model 6: Margin of Safety",
            "Putting Models Together",
        ],
        "prompt_template": "Write a book of mental models. Each chapter = one thinking tool with examples.",
    },
    
    # ==========================================================================
    # HISTORY
    # ==========================================================================
    
    "chronological_narrative": {
        "name": "Chronological History",
        "description": "Time-based storytelling. What happened, in order, and why it matters.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.HISTORY,
        "stages": [
            "The World Before - Setting the stage",
            "The Beginning - Where it starts",
            "The Key Events - What happened",
            "The Turning Points - When everything changed",
            "The Characters - Who made it happen",
            "The Consequences - What resulted",
            "The Legacy - Why it still matters",
            "The Lessons - What we learn",
        ],
        "prompt_template": "Write a historical narrative. Let events unfold chronologically with vivid detail.",
    },
    
    "thematic_history": {
        "name": "Thematic History",
        "description": "Organized by theme, not time. Each chapter explores an aspect across history.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.COMPARATIVE,
        "category": NonfictionCategory.HISTORY,
        "stages": [
            "The Theme - What we're exploring",
            "Ancient Examples",
            "Medieval Examples", 
            "Early Modern Examples",
            "Modern Examples",
            "The Pattern - What connects them",
            "The Meaning - What it tells us",
            "The Contemporary Lesson",
        ],
        "prompt_template": "Write history organized by theme, not time. Show patterns across eras.",
    },
    
    "comparative_history": {
        "name": "Comparative History",
        "description": "Then vs Now, East vs West, Culture vs Culture. Learn by comparison.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.COMPARATIVE,
        "category": NonfictionCategory.HISTORY,
        "stages": [
            "The Comparison - What are we comparing?",
            "Case A - First example in depth",
            "Case B - Second example in depth",
            "Side by Side - Direct comparison",
            "The Differences - What contrasts",
            "The Similarities - What connects",
            "The Explanations - Why the patterns",
            "The Implications - What this means for now",
        ],
        "prompt_template": "Write a comparative history. Let the comparison reveal insights.",
    },
    
    "cause_effect_chain": {
        "name": "Cause and Effect Chain",
        "description": "Events leading to now. The chain of causation that brought us here.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.HISTORY,
        "stages": [
            "The Starting Point - Where it began",
            "First Cause → First Effect",
            "Second Cause → Second Effect",
            "The Chain Deepens - How it built",
            "Critical Junctures - Could have gone differently",
            "The Cumulative Effect - Where it led",
            "The Current State - Where we are now",
            "Future Projections - Where it might go",
        ],
        "prompt_template": "Write history as a cause-and-effect chain. Show how we got to now.",
    },
    
    # ==========================================================================
    # HOW-TO NON-TECHNICAL
    # ==========================================================================
    
    "pas_method": {
        "name": "Problem-Agitation-Solution",
        "description": "Classic copywriting structure: Pain → Agitation → Solution. Make them feel before solving.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.PROBLEM_SOLUTION,
        "category": NonfictionCategory.HOW_TO,
        "stages": [
            "The Problem - Paint the pain vividly",
            "The Agitation - Make it worse",
            "The Solution - Your answer",
            "How It Works - The mechanism",
            "Proof It Works - Testimonials, evidence",
            "Why Better - Why your way vs others",
            "The Call to Action - Buy now",
            "Risk Reversal - Guarantee",
        ],
        "prompt_template": "Write using PAS: Problem, Agitation, Solution. Make them feel the pain before offering the cure.",
    },
    
    "reverse_engineering": {
        "name": "Reverse Engineering",
        "description": "Start with the end goal. Work backward to show how to get there.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.HOW_TO,
        "stages": [
            "The Goal - What you're achieving",
            "Step Backward - What's the last step?",
            "Step Backward - What's before that?",
            "Continue Backward - Keep going",
            "The First Step - Where to actually start",
            "The Path Forward - The real sequence",
            "Common Mistakes - What goes wrong",
            "Success Patterns - What works",
        ],
        "prompt_template": "Work backward from the goal. Show how to achieve the end result by working backward.",
    },
    
    "minimalist_howto": {
        "name": "Minimalist How-To",
        "description": "The fewest steps to the result. No fluff, just what works.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.HOW_TO,
        "stages": [
            "The One Thing - The core action",
            "Why It Works - Brief explanation",
            "The Steps - As few as possible",
            "Common Mistakes - What to avoid",
            "What to Do Instead - The right way",
            "Variations - When to adapt",
            "Next Level - After mastering",
        ],
        "prompt_template": "Write a minimalist how-to. Cut everything that isn't essential. Focus on results.",
    },
    
    "challenge_response": {
        "name": "Challenge-Response",
        "description": "Address specific challenges one by one. Q&A style for clarity.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.HOW_TO,
        "stages": [
            "The Big Challenge - Overview",
            "Challenge 1 - The first objection",
            "Response 1 - How to overcome",
            "Challenge 2 - The next obstacle",
            "Response 2 - How to overcome",
            "Challenge 3 - The difficult part",
            "Response 3 - The solution",
            "Putting It Together - How it works",
        ],
        "prompt_template": "Write as challenges and responses. Address every objection the reader has.",
    },
    
    # ==========================================================================
    # THOUGHT LEADERSHIP
    # ==========================================================================
    
    "contrarian_proof": {
        "name": "Contrarian + Proof",
        "description": "Counter-intuitive claim → Evidence → Implications. Challenge what people think.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "What Everyone Thinks - The conventional view",
            "Why They're Wrong - The flaw in thinking",
            "The Alternative - What you propose",
            "Evidence 1 - First proof point",
            "Evidence 2 - Second proof point",
            "Evidence 3 - Third proof point",
            "What It Means - The implications",
            "What to Do - The call to action",
        ],
        "prompt_template": "Argue a contrarian position with overwhelming evidence. Challenge conventional wisdom.",
    },
    
    "future_now": {
        "name": "Future + Now",
        "description": "Where we're going → What to do about it. Visionary but practical.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.BUSINESS,
        "stages": [
            "The Vision - Where things are going",
            "Why It Matters - The stakes",
            "The Transformation - How it changes everything",
            "The Leaders - Who's driving change",
            "The Followers - Who's being left behind",
            "What to Do - How to prepare",
            "The Timeline - When it happens",
            "The Invitation - Join the future",
        ],
        "prompt_template": "Paint a vision of the future and show how to get there. Be visionary but practical.",
    },
    
    "mistake_learning": {
        "name": "Mistake → Learning",
        "description": "Common mistakes reveal the path. Learn from what goes wrong.",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.COMPARATIVE,
        "category": NonfictionCategory.SELF_HELP,
        "stages": [
            "The Mistake - What people get wrong",
            "The Cost - Why it matters",
            "The Lesson - What it teaches",
            "The Correct Approach - What to do instead",
            "How to Know - Signs you're making it",
            "How to Fix - Getting back on track",
            "The Deeper Lesson - What this opens",
            "Moving Forward - Without the mistake",
        ],
        "prompt_template": "Write about common mistakes and what they teach. Learn from errors.",
    },
    
    # ==========================================================================
    # SPIRITUALITY & WELLNESS
    # ==========================================================================
    
    "spiritual_journey": {
        "name": "Spiritual Journey",
        "description": "The path from doubt to faith, from broken to whole. Deeply personal but universal themes.",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.SPIRITUALITY,
        "stages": [
            "The Longing - What was missing",
            "The Search - Looking for answers",
            "The First Path - What didn't work",
            "The Crisis - Questioning everything",
            "The Opening - When it started to shift",
            "The Practice - What made the difference",
            "The Integration - Bringing it into life",
            "The Gift - What was received",
        ],
        "prompt_template": "Write a spiritual journey. Be personal, be vulnerable, point to the transcendent.",
    },
    
    "healing_narrative": {
        "name": "Healing Narrative",
        "description": "From wounded to whole. The journey of physical, emotional, or psychological healing.",
        "purpose": ReaderPurpose.TRANSFORM,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.HEALTH,
        "stages": [
            "Before the Wound - Whole and healthy",
            "The Wound - What broke",
            "The Impact - How it changed everything",
            "The Denial - Pretending it's not happening",
            "The Acknowledgment - Finally facing it",
            "The Journey - Healing isn't linear",
            "The Breakthrough - The turning point",
            "The New Normal - Integration",
        ],
        "prompt_template": "Write a healing narrative. Include the struggle. Healing is not linear.",
    },
    
    # ==========================================================================
    # RELATIONSHIPS & COMMUNICATION
    # ==========================================================================
    
    "relationship_blueprint": {
        "name": "Relationship Blueprint",
        "description": "How great relationships work. The principles behind lasting connection.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.SPIRAL,
        "category": NonfictionCategory.RELATIONSHIPS,
        "stages": [
            "The Ideal - What great looks like",
            "The Foundation - What it's built on",
            "The Communication Pattern",
            "The Conflict Pattern",
            "The Intimacy Pattern",
            "The Growth Pattern",
            "The Crisis Response",
            "The Lifetime View",
        ],
        "prompt_template": "Write about what makes relationships work. Show the patterns.",
    },
    
    "communication_mastery": {
        "name": "Communication Mastery",
        "description": "From awkward to fluent. The complete communication framework.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RELATIONSHIPS,
        "stages": [
            "The Foundation - Listening",
            "The Expression - Speaking clearly",
            "The Reading - Understanding others",
            "The Writing - Clear communication",
            "The Difficult Conversation",
            "The Conflict Resolution",
            "The Influence",
            "The Mastery Integration",
        ],
        "prompt_template": "Write a complete communication guide. From foundation to mastery.",
    },
    
}


# =============================================================================
# FRAMEWORK BY CATEGORY
# =============================================================================

FRAMEWORKS_BY_CATEGORY = {
    NonfictionCategory.BUSINESS: [
        "big_idea", "one_thing", "blue_ocean", "four_disciplines", 
        "thought_leader", "contrarian_proof", "future_now", "mental_models",
    ],
    NonfictionCategory.LEADERSHIP: [
        "good_to_great", "relationship_blueprint", "communication_mastery",
    ],
    NonfictionCategory.SELF_HELP: [
        "transformation_journey", "mountain_structure", "atomic_habits_style",
        "mistake_learning", "minimalist_howto", "challenge_response",
    ],
    NonfictionCategory.MEMOIR: [
        "mountain_memoir", "loss_and_gain", "scene_driven_memoir",
        "single_moment_pivot", "addiction_recovery",
    ],
    NonfictionCategory.PHILOSOPHY: [
        "socratic_method", "argumentative_essay", "danish_philosopher",
    ],
    NonfictionCategory.SCIENCE: [
        "discovery_narrative", "experiment_story", "explainer", "mental_models",
    ],
    NonfictionCategory.HISTORY: [
        "chronological_narrative", "thematic_history", "comparative_history",
        "cause_effect_chain",
    ],
    NonfictionCategory.SPIRITUALITY: [
        "spiritual_journey", "transformation_journey",
    ],
    NonfictionCategory.HEALTH: [
        "healing_narrative", "challenge_response",
    ],
    NonfictionCategory.RELATIONSHIPS: [
        "relationship_blueprint", "communication_mastery",
    ],
}


def get_frameworks_by_category(category: NonfictionCategory) -> list[dict]:
    """Get all frameworks for a category.
    
    Args:
        category: The nonfiction category
        
    Returns:
        List of framework definitions
    """
    framework_ids = FRAMEWORKS_BY_CATEGORY.get(category, [])
    return [EXPANDED_FRAMEWORKS[fid] for fid in framework_ids if fid in EXPANDED_FRAMEWORKS]


def suggest_framework_for_book(
    topic: str,
    target_audience: str,
    intended_outcome: str,
) -> list[tuple[str, float]]:
    """Suggest the best frameworks for a book idea.
    
    Args:
        topic: The book topic
        target_audience: Who it's for
        intended_outcome: What readers will get
        
    Returns:
        List of (framework_id, confidence) sorted by confidence
    """
    topic_lower = topic.lower()
    audience_lower = target_audience.lower()
    outcome_lower = intended_outcome.lower()
    
    scores = []
    
    for fid, fw in EXPANDED_FRAMEWORKS.items():
        score = 0.0
        
        # Check category keywords
        if "business" in topic_lower or "business" in audience_lower:
            if fw.get("category") in [NonfictionCategory.BUSINESS, NonfictionCategory.LEADERSHIP]:
                score += 0.3
        
        if "lead" in topic_lower or "leader" in topic_lower:
            if fw.get("category") == NonfictionCategory.LEADERSHIP:
                score += 0.4
        
        if "memoir" in topic_lower or "story" in topic_lower:
            if fw.get("category") == NonfictionCategory.MEMOIR:
                score += 0.4
        
        # Check purpose alignment
        if any(word in outcome_lower for word in ["learn", "do", "step", "how to"]):
            if fw.get("purpose") == ReaderPurpose.LEARN_HANDS_ON:
                score += 0.3
        
        if any(word in outcome_lower for word in ["understand", "why", "how it works"]):
            if fw.get("purpose") == ReaderPurpose.UNDERSTAND:
                score += 0.3
        
        if any(word in outcome_lower for word in ["change", "transform", "become", "improve"]):
            if fw.get("purpose") == ReaderPurpose.TRANSFORM:
                score += 0.3
        
        if any(word in outcome_lower for word in ["decide", "choose", "compare"]):
            if fw.get("purpose") == ReaderPurpose.DECIDE:
                score += 0.3
        
        if scores:
            scores.append((fid, score))
    
    # Sort by score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:5]


# Total count
def get_total_framework_count() -> int:
    """Get total number of frameworks."""
    return len(EXPANDED_FRAMEWORKS)
