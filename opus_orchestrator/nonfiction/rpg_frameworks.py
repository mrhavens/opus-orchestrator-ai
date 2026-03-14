"""RPG & Tabletop Gaming Frameworks.

Game Master guides, adventure modules, worldbuilding supplements, and RPG content.
The full ecosystem of tabletop roleplaying game publishing.
"""

from opus_orchestrator.nonfiction_taxonomy import (
    ReaderPurpose,
    StructuralPattern,
    NonfictionCategory,
)


RPG_FRAMEWORKS = {
    
    # ==========================================================================
    # CORE RULEBOOKS
    # ==========================================================================
    
    "core_rulebook": {
        "name": "Core Rulebook",
        "description": "The main game system book. Contains all core mechanics, character creation, and essential rules.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Introduction - What is this game",
            "How to Read This Book",
            "Chapter 1: Creating Characters",
            "Chapter 2: Races/Species",
            "Chapter 3: Classes/Roles",
            "Chapter 4: Abilities and Skills",
            "Chapter 5: Equipment",
            "Chapter 6: Combat",
            "Chapter 7: Magic/Powers",
            "Chapter 8: Exploration",
            "Chapter 9: Social Encounters",
            "Chapter 10: Gamemastering",
            "Chapter 11: Monsters/NPCs",
            "Appendix A: Reference Tables",
            "Appendix B: Spells/Powers List",
            "Appendix C: Pre-generated Characters",
            "Index",
        ],
        "prompt_template": """Write a core rulebook for: {game_system}

Include:
- Character creation (step by step)
- Core mechanics explained clearly
- Character options (races, classes)
- Combat system
- Magic/powers (if applicable)
- GM guidance
- Reference material""",
        "tone_guidance": "Clear, comprehensive, encouraging. Accessible to new players but complete for veterans.",
        "typical_length": "300-500 pages",
        "audience": "Players and Game Masters",
    },
    
    "quickstart": {
        "name": "Quickstart Rulebook",
        "description": "Condensed intro version. Get to playing fast. Usually free or cheap.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Welcome - What's this game",
            "Character Creation (abbreviated)",
            "The Basics - Core rules",
            "Combat (simplified)",
            "Adventure - Mini dungeon/campaign",
            "Character Sheet",
            "Advanced Options (optional)",
        ],
        "prompt_template": """Write a quickstart for: {game_system}

Include:
- 5-page max rule summary
- Streamlined character creation
- One complete adventure
- Character sheet""",
        "tone_guidance": "Exciting, fast, enticing. Make them want the full book.",
        "typical_length": "16-32 pages",
        "audience": "New players, convention demos",
    },
    
    # ==========================================================================
    # GAME MASTER GUIDES
    # ==========================================================================
    
    "game_master_guide": {
        "name": "Game Master Guide",
        "description": "The GM's bible. Running games, worldbuilding, NPC creation, encounter design.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Introduction - Being a GM",
            "Part 1: Foundations",
            "  - Session Zero - Setting expectations",
            "  - Preparation techniques",
            "  - Running combat",
            "  - Running social encounters",
            "  - Running exploration",
            "Part 2: Worldbuilding",
            "  - Creating campaign settings",
            "  - Factions and politics",
            "  - Religion and culture",
            "  - Economy and technology",
            "Part 3: NPC Creation",
            "  - Villains",
            "  - Allies",
            "  - Bystanders",
            "Part 4: Encounter Design",
            "  - Combat encounters",
            "  - Skill challenges",
            "  - Social encounters",
            "Part 5: Advanced GMing",
            "  - Improvisation",
            "  - Difficulty balancing",
            "  - Campaign arcs",
        ],
        "prompt_template": """Write a GM guide for: {game_system}

Include:
- How to run the game
- Worldbuilding guidance
- NPC creation
- Encounter design
- Campaign advice""",
        "tone_guidance": "Mentor-like, experienced GM sharing wisdom. Practical and inspiring.",
        "typical_length": "200-400 pages",
        "audience": "Game Masters",
    },
    
    "adventure_module": {
        "name": "Adventure Module",
        "description": "Ready-to-run adventure. Setting, NPCs, encounters, maps, treasure.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Adventure Overview",
            "Background/Setup",
            "Hook - Getting players involved",
            "Part 1: Opening encounters",
            "  - Encounter 1.1",
            "  - Encounter 1.2",
            "Part 2: Rising action",
            "  - Encounter 2.1",
            "  - Major setpiece",
            "Part 3: Climax",
            "  - Final battle/challenge",
            "Resolution",
            "Aftermath - What happens next",
            "Appendices:",
            "  - NPCs stat blocks",
            "  - Maps",
            "  - Handouts",
            "  - Treasure/awards",
        ],
        "prompt_template": """Write an adventure module:

Setting: {setting}
Level Range: {levels}
Theme: {themes}
Length: {sessions}

Include:
- Detailed encounters
- NPCs with motivations
- Maps/layouts
- Treasure and rewards
- Hooks to continue""",
        "tone_guidance": "Ready to play. Clear, organized, inspiring but practical.",
        "typical_length": "64-200 pages",
        "audience": "Game Masters",
    },
    
    "campaign_setting": {
        "name": "Campaign Setting Sourcebook",
        "description": "Complete world. History, geography, cultures, factions, adventure hooks.",
        "purpose": ReaderPurpose.REFERENCE,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Introduction to the World",
            "World Map and Overview",
            "History (Timeline)",
            "Geography and Regions",
            "Major Factions",
            "  - Faction A",
            "  - Faction B",
            "Cultures and Peoples",
            "Religion and Magic",
            "Politics and Power",
            "Major Cities/Locations",
            "  - Location A",
            "  - Location B",
            "Important NPCs",
            "Adventure Hooks",
            "Appendix: Random Tables",
        ],
        "prompt_template": """Write a campaign setting for: {world_name}

Include:
- World history
- Geography
- Cultures
- Factions
- Adventure hooks""",
        "tone_guidance": "Immersive, detailed, inspiring. Make the world feel real and lived-in.",
        "typical_length": "200-400 pages",
        "audience": "Game Masters and Players",
    },
    
    # ==========================================================================
    # SUPPLEMENTS
    # ==========================================================================
    
    "player_companion": {
        "name": "Player's Companion",
        "description": "Player-facing content. New races, classes, options. Everything players need.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Introduction",
            "New Species/Races",
            "New Classes/Archetypes",
            "New Feats/Features",
            "New Equipment",
            "New Spells/Powers",
            "New Backgrounds",
            "Flavor Options",
        ],
        "prompt_template": """Write a player companion with new options:

Core System: {system}
New Content: {what_is_new}

Include:
- Balanced new options
- Clear mechanics
- Lore/flavor""",
        "tone_guidance": "Exciting, empowering. Players should feel excited to try new things.",
        "typical_length": "100-200 pages",
        "audience": "Players",
    },
    
    "monster_manual": {
        "name": "Monster Manual",
        "description": "Catalog of creatures. Stats, lore, how to use in games.",
        "purpose": ReaderPurpose.REFERENCE,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Introduction - Using monsters",
            "Monster Statistics Explained",
            "Creature Type: Aberrations",
            "  - Creature A",
            "  - Creature B",
            "Creature Type: Beasts",
            "Creature Type: Constructs",
            "Creature Type: Dragons",
            "Creature Type: Elementals",
            "Creature Type: Fiends",
            "Creature Type: Giants",
            "Creature Type: Humanoids",
            "Creature Type: Monstrosities",
            "Creature Type: Oozes",
            "Creature Type: Plants",
            "Creature Type: Undead",
            "NPC Stat Blocks",
            "Appendix: Monster Building",
        ],
        "prompt_template": """Write a monster manual:

Creatures to include: {list}

For each:
- Lore and background
- Stats
- How to use in game""",
        "tone_guidance": "Authoritative, evocative. Monsters should feel threatening and interesting.",
        "typical_length": "200-400 pages",
        "audience": "Game Masters",
    },
    
    "sourcebook": {
        "name": "Thematic Sourcebook",
        "description": "Deep dive into one theme: specific region, organization, time period, etc.",
        "purpose": ReaderPurpose.REFERENCE,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Overview",
            "History",
            "Geography",
            "Culture",
            "Factions",
            "Key Locations",
            "Important NPCs",
            "New Rules/Mechanics",
            "New Options for Players",
            "Adventure Hooks",
        ],
        "prompt_template": """Write a sourcebook about: {topic}

Depth: {how_deep}
For: {system}

Include:
- Everything about this topic
- New mechanics
- Player options
- GM content""",
        "tone_guidance": "Deep, passionate about the topic. Fans of the theme will love it.",
        "typical_length": "150-300 pages",
        "audience": "Dedicated fans, GMs",
    },
    
    # ==========================================================================
    # ADVENTURE TYPES
    # ==========================================================================
    
    "dungeon_crawl": {
        "name": "Dungeon Crawl",
        "description": "Classic dungeon delve. Rooms, traps, monsters, treasure.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Dungeon Overview",
            "Entry Point",
            "Dungeon Level 1:",
            "  - Room 1.1: Entrance",
            "  - Room 1.2: Traps",
            "  - Room 1.3: Combat",
            "  - Room 1.4: Puzzle",
            "  - Room 1.5: Boss",
            "Dungeon Level 2 (optional)",
            "Loot and Treasure",
            "Keys and Secrets",
            "Random Tables",
        ],
        "prompt_template": """Write a dungeon crawl:

Setting: {setting}
Levels: {levels}
Theme: {theme}

Include:
- Detailed rooms
- Traps and hazards
- Monsters
- Treasure
- Secrets""",
        "tone_guidance": "Classic dungeon vibes. Challenge and reward.",
        "typical_length": "32-64 pages",
        "audience": "GMs running dungeon content",
    },
    
    "hex_crawl": {
        "name": "Hex Crawl / Sandbox",
        "description": "Open-world exploration. Multiple locations, factions, choices.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Region Overview",
            "Hex Map",
            "Settlement: Town A",
            "Settlement: Town B",
            "Point of Interest: Ruins",
            "Point of Interest: Wilderness",
            "Point of Interest: Dungeon",
            "Faction A",
            "Faction B",
            "Random Encounter Tables",
            "Travel Rules",
        ],
        "prompt_template": """Write a hex crawl sandbox:

Region: {region}
Hexes: {number}
Factions: {list}

Include:
- Multiple locations
- Factions
- Player choice
- Random tables""",
        "tone_guidance": "Sandbox freedom. Players can go anywhere, do anything.",
        "typical_length": "64-128 pages",
        "audience": "GMs running open-world games",
    },
    
    "dungeon_world_style": {
        "name": "Dungeon World Style Adventure",
        "description": "Narrative-forward adventure. Fronts, threats, moves.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Adventure Overview",
            "Background",
            "The Hook",
            "Front 1: Immediate Threat",
            "  - Grim Portents",
            "  - Stakes",
            "Front 2: Larger Threat",
            "Key Locations",
            "Key NPCs",
            "Monster thoughts",
            "Custom Moves",
            "Countdown",
        ],
        "prompt_template": """Write a Dungeon World/PBtA adventure:

Central Conflicts: {conflicts}
Threats: {threats}

Include:
- Fronts and grim portents
- Custom moves
- Monster motivations""",
        "tone_guidance": "Narrative-forward. Like a TV show outline.",
        "typical_length": "32-64 pages",
        "audience": "PBtA GMs",
    },
    
    # ==========================================================================
    # SPECIALTY CONTENT
    # ==========================================================================
    
    "worldbuilding_guide": {
        "name": "Worldbuilding Guide",
        "description": "How to build your own RPG world. Process and systems.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Why Worldbuild?",
            "Core Concept - The Big Idea",
            "Scope - How big?",
            "Geography",
            "Cultures",
            "History",
            "Politics",
            "Religion/Magic",
            "Economy",
            "Technology Level",
            "Putting It Together",
            "Running in Your World",
        ],
        "prompt_template": """Write a worldbuilding guide:

Approach: {philosophy}

Include:
- Step-by-step process
- Prompts and questions
- Example content
- How to make it playable""",
        "tone_guidance": "Mentor, encouraging. Guide their creativity.",
        "typical_length": "150-250 pages",
        "audience": "Aspiring worldbuilders and GMs",
    },
    
    "props_and_handouts": {
        "name": "Props and Handouts",
        "description": "Physical/digital props for immersion. Letters, maps, wanted posters.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Introduction - Why props matter",
            "Handout Types",
            "Letters and Documents",
            "Maps and Diagrams",
            "Images and Artwork",
            "In-Game Objects",
            "Prop Templates",
            "Digital Props",
            "Print and Play",
        ],
        "prompt_template": """Create prop templates:

Adventure: {adventure_name}
Props needed: {list}

Include:
- Text for each prop
- Design notes
- How to use in play""",
        "tone_guidance": "Practical, creative. Make the game feel real.",
        "typical_length": "32-64 pages",
        "audience": "GMs who want immersion",
    },
    
    "solo_adventure": {
        "name": "Solo Adventure / Journaling RPG",
        "description": "Playable alone. Self-contained with rules for single player.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "How to Play Solo",
            "Character Creation",
            "Rules Summary",
            "Adventure Start",
            "Chapter 1: The Beginning",
            "  - Choices and outcomes",
            "Chapter 2: Development",
            "Climax",
            "Resolution",
            "Oracles/Random Tables",
            "Character Sheet",
        ],
        "prompt_template": """Write a solo adventure:

Theme: {theme}
Length: {length}
System: {system}

Include:
- Self-contained rules
- Story branches
- Oracle/random tables""",
        "tone_guidance": "Personal, immersive. Like writing your own adventure.",
        "typical_length": "64-128 pages",
        "audience": "Solo RPG players",
    },
    
    "larp_document": {
        "name": "LARP (Live Action) Document",
        "description": "Written for live action roleplaying. Character sheets, plot, props.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.RPG,
        "stages": [
            "Event Overview",
            "Setting",
            "Background/World",
            "Factions and Goals",
            "Character Packets:",
            "  - Character A",
            "  - Character B",
            "Plot Outline",
            "Timeline of Events",
            "GM Notes",
            "Props List",
            "Safety Tools",
        ],
        "prompt_template": """Write a LARP event:

Type: {type}
Duration: {length}
Players: {number}

Include:
- Characters with secrets
- Plot that creates drama
- Safety content""",
        "tone_guidance": "Structured for live play. Clear beats and goals.",
        "typical_length": "32-100 pages",
        "audience": "LARPers and event organizers",
    },
    
}


def get_rpg_frameworks() -> dict:
    """Get all RPG frameworks."""
    return RPG_FRAMEWORKS


def suggest_rpg_framework(
    content_type: str = "",
    audience: str = "",
) -> str:
    """Suggest the best RPG framework.
    
    Args:
        content_type: core / adventure / supplement / etc.
        audience: players / GMs / etc.
        
    Returns:
        Framework ID
    """
    content_type = (content_type or "").lower()
    
    # Core books
    if "core" in content_type or "rulebook" in content_type:
        return "core_rulebook"
    if "quick" in content_type:
        return "quickstart"
    
    # GM content
    if "gm guide" in content_type or "game master" in content_type:
        return "game_master_guide"
    if "adventure" in content_type:
        if "dungeon" in content_type:
            return "dungeon_crawl"
        if "hex" in content_type or "sandbox" in content_type:
            return "hex_crawl"
        return "adventure_module"
    if "campaign" in content_type or "setting" in content_type:
        return "campaign_setting"
    if "world" in content_type:
        return "worldbuilding_guide"
    
    # Supplements
    if "monster" in content_type or "creature" in content_type:
        return "monster_manual"
    if "player" in content_type:
        return "player_companion"
    if "sourcebook" in content_type or "supplement" in content_type:
        return "sourcebook"
    
    # Special
    if "solo" in content_type or "journal" in content_type:
        return "solo_adventure"
    if "larp" in content_type or "live" in content_type:
        return "larp_document"
    if "prop" in content_type or "handout" in content_type:
        return "props_and_handouts"
    
    # Default
    return "core_rulebook"
