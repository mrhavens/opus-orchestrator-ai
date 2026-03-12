"""Story frameworks for Opus Orchestrator.

Implements multiple narrative structure frameworks:
- Snowflake Method
- Three-Act Structure
- Save the Cat (Blake Snyder)
- Hero's Journey (Joseph Campbell)
- Story Circle (Dan Harmon)
- The 7-Point Plot (The Pantone)
- Fichtean Curve
"""

from enum import Enum
from typing import Any


class StoryFramework(str, Enum):
    """Available story frameworks."""
    
    SNOWFLAKE = "snowflake"
    THREE_ACT = "three-act"
    SAVE_THE_CAT = "save-the-cat"
    HERO_JOURNEY = "hero-journey"
    STORY_CIRCLE = "story-circle"
    SEVEN_POINT = "seven-point"
    FICHTEAN = "fichtean"


# Framework descriptions and prompts

FRAMEWORKS = {
    StoryFramework.SNOWFLAKE: {
        "name": "Snowflake Method",
        "description": "Fractal expansion from sentence to paragraph to full novel",
        "stages": [
            "One sentence summary",
            "One paragraph outline", 
            "Character sheets",
            "Four-page outline",
            "Detailed character charts",
            "Scene list",
            "Scene descriptions",
        ],
    },
    
    StoryFramework.THREE_ACT: {
        "name": "Three-Act Structure",
        "description": "Classic setup, confrontation, resolution structure",
        "stages": [
            "Act I: Setup - Introduce protagonist, status quo, inciting incident",
            "Act I: Break into Two - Commit to journey",
            "Act II, Part 1: Fun and Games - Promise of premise",
            "Act II, Part 1: Midpoint - Stakes raise",
            "Act II, Part 2: Bad Guys Close In - External pressure",
            "Act II, Part 2: All Is Lost - Lowest point",
            "Act III: Finale - Climax and resolution",
        ],
    },
    
    StoryFramework.SAVE_THE_CAT: {
        "name": "Save the Cat",
        "description": "Blake Snyder's 15-beat screenwriting structure",
        "beats": [
            ("Opening Image", "Visual hook that sets the tone"),
            ("Theme Stated", "Someone states the theme"),
            ("Setup", "Normal world, introduce key players"),
            ("Catalyst", "Life-changing event"),
            ("Debate", "Protagonist resists the call"),
            ("Break Into Two", "Commit to the journey"),
            ("B Story", "Subplot begins"),
            ("Fun and Games", "Promise of the premise"),
            ("Midpoint", "Stakes are raised"),
            ("Bad Guys Close In", "External pressure increases"),
            ("All Is Lost", "Darkest moment"),
            ("Dark Night of the Soul", "Emotional nadir"),
            ("Break Into Three", "Solution found"),
            ("Finale", "Final confrontation"),
            ("Final Image", "Changed world"),
        ],
    },
    
    StoryFramework.HERO_JOURNEY: {
        "name": "Hero's Journey",
        "description": "Joseph Campbell's monomyth - 12 stages",
        "beats": [
            ("Ordinary World", "Hero's normal life before the adventure"),
            ("Call to Adventure", "Challenge or quest presented"),
            ("Refusal of the Call", "Hero hesitates or declines"),
            ("Meeting the Mentor", "Guide appears with wisdom/tools"),
            ("Crossing the Threshold", "Hero commits, enters special world"),
            ("Tests, Allies, Enemies", "Hero faces challenges, makes friends/foes"),
            ("Approach to Inmost Cave", "Hero prepares for major challenge"),
            ("Ordeal", "Hero faces greatest challenge, death/rebirth"),
            ("Reward", "Hero gains prize/knowledge"),
            ("The Road Back", "Hero begins return journey"),
            ("Resurrection", "Final test, hero transformed"),
            ("Return with Elixir", "Hero returns, transformed"),
        ],
    },
    
    StoryFramework.STORY_CIRCLE: {
        "name": "Story Circle",
        "description": "Dan Harmon's 8-step circular structure",
        "beats": [
            ("You", "Character in their comfort zone"),
            ("Need", "Character feels something is missing"),
            ("Go", "Character enters unfamiliar situation"),
            ("Adapt", "Character adjusts to new world"),
            ("Get", "Character gains what they sought"),
            ("Return", "Character returns home"),
            ("Change", "Character is transformed"),
            ("Result", "Character's life is different"),
        ],
    },
    
    StoryFramework.SEVEN_POINT: {
        "name": "The 7-Point Plot",
        "description": "The Pantone method - 7 key plot points",
        "beats": [
            ("Hook", "Opening that grabs attention"),
            ("Plot Turn 1", "First major change, inciting incident"),
            ("Pinch Point 1", "Pressure from antagonist"),
            ("Midpoint", "Character commits to action"),
            ("Pinch Point 2", "Increased pressure, stakes raise"),
            ("Plot Turn 2", "Major reversal, everything changes"),
            ("Resolution", "Final confrontation, new equilibrium"),
        ],
    },
    
    StoryFramework.FICHTEAN: {
        "name": "Fichtean Curve",
        "description": "Progressive rising action - series of crises",
        "beats": [
            ("Inciting Incident", "Chain of events begins"),
            ("Rising Action 1", "First crisis"),
            ("Rising Action 2", "Second crisis"),
            ("Rising Action 3", "Third crisis"),
            ("Climax", "Maximum tension"),
            ("Falling Action", "Aftermath"),
            ("Resolution", "New status quo"),
        ],
    },
}


def get_framework_prompt(framework: StoryFramework) -> str:
    """Get the system prompt for a framework."""
    
    if framework == StoryFramework.SAVE_THE_CAT:
        return """You are an expert in Save the Cat story structure (Blake Snyder).
        
The 15 beats of Save the Cat:
1. Opening Image - Visual hook, tone setter
2. Theme Stated - Someone states the theme
3. Setup - Normal world, introduce characters
4. Catalyst - Life-changing event
5. Debate - Protagonist resists the call
6. Break Into Two - Commit to journey
7. B Story - Subplot begins
8. Fun and Games - Promise of the premise
9. Midpoint - Stakes raise
10. Bad Guys Close In - External pressure
11. All Is Lost - Darkest moment
12. Dark Night of the Soul - Emotional nadirs
13. Break Into Three - Solution found
14. Finale - Final confrontation
15. Final Image - Changed world

Use these beats to structure compelling narratives."""
    
    elif framework == StoryFramework.HERO_JOURNEY:
        return """You are an expert in the Hero's Journey (Joseph Campbell's monomyth).

The 12 stages:
1. Ordinary World - Hero's normal life
2. Call to Adventure - Challenge presented
3. Refusal of the Call - Hero hesitates
4. Meeting the Mentor - Guide appears
5. Crossing the Threshold - Enter special world
6. Tests, Allies, Enemies - Face challenges
7. Approach to Inmost Cave - Prepare for major challenge
8. Ordeal - Greatest challenge, death/rebirth
9. Reward - Gain prize/knowledge
10. The Road Back - Begin return
11. Resurrection - Final test, transformation
12. Return with Elixir - Return transformed

Use these stages to structure mythic narratives."""
    
    elif framework == StoryFramework.STORY_CIRCLE:
        return """You are an expert in Dan Harmon's Story Circle.

The 8 steps:
1. You - Character in comfort zone
2. Need - Something missing
3. Go - Enter unfamiliar situation
4. Adapt - Adjust to new world
5. Get - Gain what sought
6. Return - Return home
7. Change - Transformed
8. Result - Life different

Use this circular structure for balanced narratives."""
    
    elif framework == StoryFramework.SEVEN_POINT:
        return """You are an expert in The 7-Point Plot (The Pantone).

The 7 plot points:
1. Hook - Opening grab
2. Plot Turn 1 - First major change
3. Pinch Point 1 - Antagonist pressure
4. Midpoint - Commit to action
5. Pinch Point 2 - Stakes raise
6. Plot Turn 2 - Major reversal
7. Resolution - New equilibrium

Use this for tight, event-driven plots."""
    
    elif framework == StoryFramework.FICHTEAN:
        return """You are an expert in the Fichtean Curve.

Progressive crisis structure:
1. Inciting Incident - Chain of events begins
2. Rising Action 1 - First crisis
3. Rising Action 2 - Second crisis (bigger)
4. Rising Action 3 - Third crisis (biggest)
5. Climax - Maximum tension
6. Falling Action - Aftermath
7. Resolution - New status quo

Use this for action-driven, tension-building narratives."""
    
    elif framework == StoryFramework.THREE_ACT:
        return """You are an expert in Three-Act Structure.

Classic narrative structure:
ACT I - SETUP
- Opening Image
- Theme Stated
- Setup (normal world)
- Catalyst (inciting incident)
- Debate (protagonist resists)
- Break Into Two (commit to journey)

ACT II - CONFRONTATION
- B Story (subplot begins)
- Fun and Games (promise of premise)
- Midpoint (stakes raise)
- Bad Guys Close In (external pressure)
- All Is Lost (lowest point)
- Dark Night of the Soul (internal reckoning)
- Break Into Three (solution found)

ACT III - RESOLUTION
- Finale (climax)
- Final Image (changed world)

Use this traditional structure for any genre."""
    
    else:
        return "You are an expert story architect."


def get_framework_for_genre(genre: str) -> list[StoryFramework]:
    """Suggest frameworks based on genre."""
    
    suggestions = {
        "fantasy": [StoryFramework.HERO_JOURNEY, StoryFramework.SNOWFLAKE],
        "science-fiction": [StoryFramework.SNOWFLAKE, StoryFramework.SAVE_THE_CAT],
        "thriller": [StoryFramework.SAVE_THE_CAT, StoryFramework.SEVEN_POINT, StoryFramework.FICHTEAN],
        "horror": [StoryFramework.HERO_JOURNEY, StoryFramework.FICHTEAN],
        "romance": [StoryFramework.STORY_CIRCLE, StoryFramework.SAVE_THE_CAT],
        "mystery": [StoryFramework.SEVEN_POINT, StoryFramework.THREE_ACT],
        "literary": [StoryFramework.SNOWFLAKE, StoryFramework.HERO_JOURNEY],
        "adventure": [StoryFramework.HERO_JOURNEY, StoryFramework.FICHTEAN],
    }
    
    return suggestions.get(genre.lower(), [StoryFramework.THREE_ACT, StoryFramework.SNOWFLAKE])
