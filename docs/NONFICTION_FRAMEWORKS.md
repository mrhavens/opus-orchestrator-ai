# Nonfiction Framework Library

Opus supports 100+ frameworks organized by content type.

## Reader Purposes

Every nonfiction book serves a **reader purpose** - why someone reads it:

| Purpose | Description | Example Frameworks |
|---------|-------------|------------------|
| `learn` | Do something hands-on | Tutorial, How-To, Course |
| `understand` | Grasp a concept | Explainer, Socratic Method |
| `transform` | Change themselves | Self-Help, Memoir |
| `decide` | Make a decision | Big Idea, Case Study |
| `reference` | Look up information | Manual, Encyclopedia |
| `inspire` | Feel motivated | Manifesto, Story |

## Framework Categories

### Tutorial/How-To
- Tutorial
- Howto  
- Minimalist How-To
- Challenge-Response
- Reverse Engineering
- PAS (Problem-Agitation-Solution)

### Explanation/Concept
- Concept Explainer
- Explainer (Pinker-style)
- Socratic Method
- Danish Philosopher
- Argumentative Essay
- Mental Models

### Transformation/Self-Help
- Transformation Journey
- Mountain Structure
- Atomic Habits Style
- Loss and Gain
- Mistake → Learning

### Decision/Business
- Big Idea (Jim Collins)
- Problem-Solution
- Case Study
- Blue Ocean Strategy
- The One Thing
- 4 Disciplines of Execution

### Reference/Technical
- Technical Manual
- Quick Reference Guide
- Knowledge Base
- API Documentation
- Encyclopedia

### Inspiration/Manifesto
- Visionary
- Manifesto
- Open Letter
- Biography
- Memoir

## Textbook/Educational

| Framework | Description |
|-----------|-------------|
| Comprehensive Textbook | Complete academic textbook |
| Textbook Chapter | Single modular chapter |
| Online Course / MOOC | Video-friendly course |
| Curriculum / Syllabus | Course planning document |
| Study Guide | Exam prep |
| Workbook | Interactive exercises |

## Academic Papers

| Framework | Description |
|-----------|-------------|
| Empirical Paper | IMRAD research format |
| Theoretical Paper | Models, proofs |
| Methodology Paper | New methods |
| Case Study | Single case analysis |
| Survey Paper | Field overview |
| Position Paper | Argumentative stance |
| Policy Brief | Recommendations |
| Literature Review | Systematic synthesis |
| Thesis/Dissertation | Graduate research |
| Meta-Analysis | Statistical synthesis |

## Creative/Interactive

| Framework | Description |
|-----------|-------------|
| Choose Your Own Adventure | Branching narrative |
| Gamebook | RPG-style adventure |
| Visual Novel | Anime-style script |
| Epistolary Novel | Letters/emails/texts |
| Found Documents | Discovered artifacts |
| Manifesto | Revolutionary call |
| Open Letter | Public letter |
| Infinite Story | Serial/neverending |
| Fractal Narrative | Self-similar structure |
| Podcast Script | Spoken audio |
| Screenplay | Film script |
| Stage Play | Theatrical script |

## RPG/Tabletop

| Framework | Description |
|-----------|-------------|
| Core Rulebook | Main game system |
| Quickstart | Condensed intro |
| Game Master Guide | Running games |
| Adventure Module | Ready-to-run |
| Campaign Setting | World sourcebook |
| Player's Companion | New options |
| Monster Manual | Creatures catalog |
| Dungeon Crawl | Classic dungeon |
| Hex Crawl | Sandbox exploration |
| Worldbuilding Guide | How to build worlds |
| Solo Adventure | Single player |
| LARP Document | Live action |

## Usage

```bash
# List all frameworks
opus frameworks

# Generate with purpose
opus generate --book-type nonfiction --purpose learn "How to code in Python"

# Generate with category
opus generate --book-type nonfiction --category business --framework big_idea

# Specific framework
opus generate --book-type nonfiction --framework transformation_journey
```

## Programmatic Usage

```python
from opus_orchestrator.nonfiction import (
    determine_intake,
    suggest_framework_for_book,
    suggest_textbook_framework,
    suggest_academic_paper,
    suggest_creative_framework,
    suggest_rpg_framework,
)

# Auto-suggest framework
result = await determine_intake(
    concept="How to build an AI startup",
    purpose="learn",
    category="business"
)
# → Purpose: learn_hands_on
# → Framework: Tutorial / How-To

# Suggest for specific use case
framework = suggest_textbook_framework(
    use_case="online course",
    audience="beginners",
    length="medium"
)
```
