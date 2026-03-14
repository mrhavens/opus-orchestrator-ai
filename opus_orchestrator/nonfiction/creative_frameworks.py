"""Creative & Interactive Frameworks.

Non-traditional, experimental, and interactive content formats.
Choose Your Own Adventure, epistolary, manifestos, and more.
"""

from opus_orchestrator.nonfiction_taxonomy import (
    ReaderPurpose,
    StructuralPattern,
    NonfictionCategory,
)


CREATIVE_FRAMEWORKS = {
    
    # ==========================================================================
    # INTERACTIVE / BRANCHING
    # ==========================================================================
    
    "choose_your_own_adventure": {
        "name": "Choose Your Own Adventure",
        "description": "Branching narrative where reader choices determine the story path. Multiple endings based on decisions.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Introduction - Set the scene",
            "Opening Choice - First decision point",
            "Path A - Option A leads here",
            "Path B - Option B leads here",
            "Branch A1 - Next choice",
            "Branch A2 - Alternative path",
            "Branch B1 - Next choice",
            "Convergence Point - Paths may rejoin",
            "Ending 1 - Success ending",
            "Ending 2 - Failure ending",
            "Ending 3 - Secret/alternate ending",
            "Choice Summary - Which choices lead where",
        ],
        "prompt_template": """Write a Choose Your Own Adventure story:

Setting: {setting}
Protagonist: {main_character}
Theme: {theme}

Include:
- Vivid opening that draws reader in
- 2-3 choice points minimum
- 3+ distinct endings
- Each choice should be meaningful
- Branch paths that may converge or stay separate""",
        "tone_guidance": "Engaging, suspenseful, clear choices. Each path should feel like a real story.",
        "typical_length": "5,000-20,000 words",
        "audience": "Young adult to adult readers",
    },
    
    "gamebook": {
        "name": "Gamebook / Fighting Fantasy",
        "description": "RPG-style adventure with combat, stats, and inventory. Reader/player is the protagonist.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Character Creation - Stats, skills",
            "Equipment List - Starting items",
            "Prologue - Setup",
            "Encounter 1 - First challenge",
            "Combat/Choice Resolution",
            "Encounter 2 - Second challenge",
            "Inventory Management",
            "Encounter 3-10 - Progressive challenges",
            "Boss Encounter - Final battle",
            "Endings based on stats/outcomes",
            "Rules Reference",
        ],
        "prompt_template": """Write a gamebook adventure:

Genre: {genre}
Setting: {world}
Difficulty: {hard/easy}

Include:
- Character stats (strength, skill, luck, etc.)
- Combat system rules
- 10+ encounters
- Multiple paths
- Loot/inventory system""",
        "tone_guidance": "Game-like, exciting, rule-abiding. Clear mechanics.",
        "typical_length": "30,000-60,000 words",
        "audience": "Gamers, fantasy readers",
    },
    
    "visual_novel": {
        "name": "Visual Novel Script",
        "description": "Game script with character dialogues, scene descriptions, and choice points. Anime/VN style.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Title Screen / Opening",
            "Prologue",
            "Chapter 1: Scene 1 - Setup",
            "Character: Character A enters",
            "Dialogue Exchange 1",
            "Choice Point - Player decision",
            "Route A: Path",
            "Route B: Alternative",
            "Character Relationship Tracking",
            "Chapter Climax",
            "Multiple Endings",
            "Credits / Bonus Content",
        ],
        "prompt_template": """Write a visual novel script:

Characters: {character_list}
Setting: {world}
Routes: {number_of_routes}

Include:
- Character sprites/dialogues
- Scene directions
- Choice points
- Relationship mechanics""",
        "tone_guidance": "Anime-style dialogue, expressive, character-driven.",
        "typical_length": "20,000-80,000 words",
        "audience": "Visual novel players",
    },
    
    # ==========================================================================
    # EPISTOLARY / DOCUMENTS
    # ==========================================================================
    
    "epistolary_novel": {
        "name": "Epistolary Novel",
        "description": "Story told entirely through documents: letters, emails, texts, diary entries, etc.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Editor's Note - Frame narrative",
            "Document 1: Letter/Email/Text",
            "Document 2: Reply",
            "Document 3: Another perspective",
            "Time Jump - Dates progress",
            "Document N: Crisis point",
            "Documents reveal backstory",
            "Rising action through exchanges",
            "Climax - Major revelation",
            "Final document(s)",
            "Editor's Note - Conclusion",
        ],
        "prompt_template": """Write an epistolary novel:

Documents: letters / emails / texts / diary
Perspectives: {number}
Time Span: {time_period}

Include:
- Each document has distinct voice
- Documents reveal backstory gradually
- Format variety (long letters, quick texts)
- What can't be shown, only hinted""",
        "tone_guidance": "Distinct voices per document type. Intimate, immediate.",
        "typical_length": "40,000-80,000 words",
        "audience": "Literary fiction readers",
    },
    
    "found_documents": {
        "name": "Found Documents / Artifacts",
        "description": "A story revealed through discovered materials: redacted files, journal fragments, annotated maps.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Foreword - How these were found",
            "Artifact 1: Document type",
            "Artifact 2: Different type",
            "Annotation/Commentary layer",
            "Artifact 3: Reveals更多信息",
            "Redactions gradually filled in",
            "Maps/Photographs with notes",
            "Pattern emerges for reader",
            "Final artifact - Key revelation",
            "Afterword - What it means",
        ],
        "prompt_template": """Write using found documents:

Types of artifacts: {list}
Mystery: {central_question}
What reader pieces together: {revelation}

Include:
- Varied document formats
- Redactions that hint
- Annotations from finders""",
        "tone_guidance": "Mysterious, fragmented, cumulative. Reader is detective.",
        "typical_length": "30,000-60,000 words",
        "audience": "Mystery/literary fiction readers",
    },
    
    # ==========================================================================
    # MANIFESTO / CALL TO ACTION
    # ==========================================================================
    
    "manifesto": {
        "name": "Manifesto",
        "description": "Revolutionary call to action. A passionate argument for change.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Opening - The problem we've ignored",
            "Part 1: What Is - Current state",
            "Part 2: What Could Be - Vision",
            "Part 3: What Must Change - The demands",
            "The Enemy - What opposes us",
            "The Solution - Our path forward",
            "Why Now - Urgency",
            "Who We Are - Call to identity",
            "The Future - What we build",
            "Closing - Final call to action",
        ],
        "prompt_template": """Write a manifesto:

Cause: {topic}
Position: {revolutionary_stance}
Audience: {who_needs_to_hear}

Include:
- Passionate, powerful language
- Clear enemy/opposition
- Vision of better future
- Specific demands
- Call to action""",
        "tone_guidance": "Passionate, urgent, powerful, rhythmic. Speak to hearts and minds.",
        "typical_length": "3,000-10,000 words",
        "audience": "Activists, believers, movement builders",
    },
    
    "open_letter": {
        "name": "Open Letter",
        "description": "Public letter to a specific person/entity. Makes a point through direct address.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Salutation - Dear [Name/Entity]",
            "Opening - Why I'm writing publicly",
            "The Issue - What you did/said",
            "The Impact - Consequences",
            "What I Expect - The ask",
            "The Vision - What could be",
            "Deadline/Urgency - When",
            "Sign-off - Name and call to action",
        ],
        "prompt_template": """Write an open letter:

Recipient: {who}
Issue: {what}
Position: {your_stance}
Desired Outcome: {what_you_want}

Include:
- Direct address
- Emotional resonance
- Logical argument
- Clear ask""",
        "tone_guidance": "Direct, passionate, public. Written to be shared.",
        "typical_length": "500-3,000 words",
        "audience": "Public, media, social networks",
    },
    
    # ==========================================================================
    # EXPERIMENTAL STRUCTURES
    # ==========================================================================
    
    "infinite_story": {
        "name": "Infinite Story / Serial",
        "description": "Endlessly extensible story. Each chapter ends with a new beginning. For serialization.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Episode 1: Complete arc",
            "Episode 1 Cliffhanger - Link to next",
            "Episode 2: New situation",
            "Episode 2 Thread - Continues to next",
            "Recurring Elements - That persist",
            "Episode N: Milestone chapter",
            "Thread 1 Resolution",
            "Thread 2 Introduced",
            "Final Episode (for now) - Open ending",
            "Hooks for continuation",
        ],
        "prompt_template": """Write an infinite story:

Format: Serial / Web fiction
Episode Length: {length}
Ongoing Threads: {number}

Include:
- Each episode has complete mini-arc
- Cliffhangers or hooks
- Persistent story threads
- Can continue indefinitely""",
        "tone_guidance": "Engaging, episodic, addictive. Each episode demands the next.",
        "typical_length": "Ongoing (1,000-5,000 words per episode)",
        "audience": "Web fiction readers, serial fans",
    },
    
    "fractal_narrative": {
        "name": "Fractal Narrative",
        "description": "Story that repeats at different scales. Chapter mirrors scene mirrors paragraph.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Macro Level: The Overall Arc",
            "Structure mirrors down",
            "Chapter 1: Major section",
            "Each chapter contains:",
            "  - Scene 1: Subsection",
            "    - Each scene: paragraph",
            "      - Each paragraph: sentence",
            "        - Each sentence mirrors all",
            "Pattern emerges on reread",
        ],
        "prompt_template": """Write a fractal narrative:

Core Pattern: {repeating_element}
Scales: {how_many_levels}

Include:
- Same pattern at each level
- New meaning emerges on scale
- Reader discovers pattern""",
        "tone_guidance": "Literary, structured, rewarding on re-reading.",
        "typical_length": "20,000-60,000 words",
        "audience": "Literary fiction readers, puzzle lovers",
    },
    
    "scrapbook": {
        "name": "Scrapbook / Assemblage",
        "description": "Non-linear collection of fragments: memories, images (described), ticket stubs, recipes, etc.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.SPIRAL,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Opening Spread - First impressions",
            "Fragment 1: Memory/Image",
            "Fragment 2: Different type",
            "Fragment 3: Connection emerges",
            "Theme 1: Around theme A",
            "Theme 2: Around theme B",
            "Pattern emerges through collection",
            "Central Image/Moment",
            "Return to beginning - New meaning",
            "Closing - What it means",
        ],
        "prompt_template": """Write a scrapbook narrative:

Format: Non-linear fragments
Themes: {central_themes}
Fragments to include: {list_types}

Include:
- Varied fragment types
- Gaps create meaning
- Pattern through accumulation""",
        "tone_guidance": "Nostalgic, associative, intimate. Memory-like.",
        "typical_length": "15,000-40,000 words",
        "audience": "Literary fiction, memoir readers",
    },
    
    # ==========================================================================
    # AUDIO / PERFORMANCE
    # ==========================================================================
    
    "podcast_script": {
        "name": "Podcast Script",
        "description": "Script for spoken audio. Includes banter, segments, transitions.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Intro - Hook + branding",
            "Cold Open - Tease",
            "Segment 1: Setup/Context",
            "Segment 2: Main content",
            "Segment 3: Deep dive",
            "Guest Interview (if applicable)",
            "Takeaways - Key points",
            "Wrap-up + preview",
            "Call to action",
            "Outro - Sign-off",
        ],
        "prompt_template": """Write a podcast script:

Format: {interview/conversation/solo}
Duration: {length}
Topic: {subject}

Include:
- Verbal hooks
- Segment timing cues
- Ad reads (if applicable)
- Engagement prompts""",
        "tone_guidance": "Conversational, energetic, intimate. Like talking to a friend.",
        "typical_length": "2,000-8,000 words (20-60 min audio)",
        "audience": "Podcast listeners",
    },
    
    "screenplay": {
        "name": "Screenplay / Film Script",
        "description": "Hollywood standard screenplay format. Visual storytelling through action and dialogue.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Title Page",
            "Fade In",
            "Scene Heading 1 - EXT./INT. LOCATION - TIME",
            "Action/Description",
            "CHARACTER NAME",
            "Dialogue",
            "Parenthetical",
            "Transition",
            "Scene Heading 2",
            "... (continues)",
            "FADE OUT",
            "THE END",
        ],
        "prompt_template": """Write a screenplay:

Genre: {genre}
Length: {pages} pages (1 min/page)
Setting: {world}

Include:
- Visual storytelling
- Economy of words
- Character through action
- Standard formatting""",
        "tone_guidance": "Visual, efficient, cinematic. Show don't tell.",
        "typical_length": "90-120 pages (screenplay format)",
        "audience": "Filmmakers, screenwriters",
    },
    
    "stage_play": {
        "name": "Stage Play Script",
        "description": "Theatrical script with scenes, stage directions, and dialogue.",
        "purpose": ReaderPurpose.BE_INSPIRED,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.CREATIVITY,
        "stages": [
            "Title Page",
            "Dramatis Personae - Characters",
            "Scene 1: Location",
            "Stage Directions",
            "Character Dialogue",
            "Scene 2",
            "Act Break",
            "Scene 3-N",
            "Intermission",
            "Final Scene",
            "Curtain Call",
        ],
        "prompt_template": """Write a stage play:

Genre: {drama/comedy/tragedy}
Acts: {number}
Characters: {cast_size}

Include:
- Stage directions
- Character development through dialogue
- Scenic requirements (practical)
- Theatrical conventions""",
        "tone_guidance": "Dramatic, dialogue-forward, theatrical.",
        "typical_length": "60-120 pages",
        "audience": "Theater practitioners, playwrights",
    },
    
}


def get_creative_frameworks() -> dict:
    """Get all creative and interactive frameworks."""
    return CREATIVE_FRAMEWORKS


def suggest_creative_framework(
    format_type: str = "",
    audience: str = "",
) -> str:
    """Suggest the best creative framework.
    
    Args:
        format_type: creative / interactive / epistolary / etc.
        audience: Who is this for
        
    Returns:
        Framework ID
    """
    format_type = (format_type or "").lower()
    
    # Interactive
    if "choose" in format_type or "adventure" in format_type:
        return "choose_your_own_adventure"
    if "gamebook" in format_type or "rpg" in format_type:
        return "gamebook"
    if "visual novel" in format_type or "vn" in format_type:
        return "visual_novel"
    
    # Epistolary
    if "letter" in format_type:
        return "epistolary_novel"
    if "found" in format_type or "document" in format_type:
        return "found_documents"
    
    # Manifesto
    if "manifesto" in format_type:
        return "manifesto"
    if "letter" in format_type and "open" in format_type:
        return "open_letter"
    
    # Experimental
    if "serial" in format_type or "infinite" in format_type:
        return "infinite_story"
    if "fractal" in format_type or "recursive" in format_type:
        return "fractal_narrative"
    if "scrapbook" in format_type or "fragment" in format_type:
        return "scrapbook"
    
    # Audio/Performance
    if "podcast" in format_type or "audio" in format_type:
        return "podcast_script"
    if "screenplay" in format_type or "film" in format_type:
        return "screenplay"
    if "play" in format_type or "theater" in format_type or "stage" in format_type:
        return "stage_play"
    
    # Default
    return "choose_your_own_adventure"
