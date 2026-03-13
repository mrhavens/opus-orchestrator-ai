# Nonfiction Generation Pipeline
# ==============================
# How the workflow CHANGES based on Purpose × Structure

## INPUT PHASE
## -----------
# User provides: concept, purpose (why read), category (subject), optional preferred framework
# 
# Example inputs:
#   - "Leadership for introverts" + PURPOSE=TRANSFORM + CATEGORY=LEADERSHIP
#   - "How to code in Python" + PURPOSE=LEARN_HANDS_ON + CATEGORY=TECHNOLOGY
#   - "Why nations fail" + PURPOSE=DECIDE + CATEGORY=HISTORY

## CLASSIFICATION PHASE (NEW)
## ---------------------------
# System maps: purpose → framework families → specific framework
#
# if PURPOSE == "learn_hands_on":
#     framework = select("tutorial" or "howto")
#     stages = ["prerequisites", "step 1", "step 2", ...]
#     
# elif PURPOSE == "transform":
#     framework = select("transformation_journey" or "mountain_structure")
#     stages = ["wake-up", "denial", "dark night", ...]
#     
# elif PURPOSE == "decide":
#     framework = select("big_idea" or "problem_solution")
#     stages = ["problem", "evidence", "solution", ...]

## SCAFFOLDING PHASE (CHANGES)
## ---------------------------
# Different STAGES based on framework
#
# TUTORIAL scaffold:
#   - Introduction → Prerequisites → Step 1 → Step 2 → Step 3 → Completion → Next Steps
#   
# TRANSFORMATION_JOURNEY scaffold:
#   - Wake-Up → Denial → Dark Night → Realization → Path → Struggles → Breakthrough → New Normal
#   
# BIG_IDEA scaffold:
#   - Promise → Opposition → Evidence → Implications → Counter-Arguments → Conclusion

## DRAFTING PHASE (CHANGES)
## ------------------------
# Different AGENTS activated based on purpose
#
# if PURPOSE == "learn_hands_on":
#     agent = "TutorialWriter"  # Focus on clarity, exercises, checkpoints
#     tone = "encouraging, clear, patient"
#     
# elif PURPOSE == "transform":
#     agent = "TransformationWriter"  # Focus on emotion, narrative, inspiration
#     tone = "empathetic, honest, motivational"
#     
# elif PURPOSE == "decide":
#     agent = "EvidenceWriter"  # Focus on data, proof, credibility
#     tone = "authoritative, data-driven, persuasive"

## CRITIQUE PHASE (CHANGES)
## ------------------------
# Different EVALUATION CRITERIA based on purpose
#
# if PURPOSE == "learn_hands_on":
#     check: "Can a reader actually complete the steps?"
#     check: "Are prerequisites clear?"
#     check: "Is there a sense of progression?"
#     
# elif PURPOSE == "transform":
#     check: "Does it feel emotionally honest?"
#     check: "Is the transformation arc believable?"
#     check: "Would this inspire change?"
#     
# elif PURPOSE == "decide":
#     check: "Is the evidence credible?"
#     check: "Are counter-arguments addressed?"
#     check: "Does it lead to a clear recommendation?"

## OUTPUT PHASE (CHANGES)
## ----------------------
# Different FORMAT based on purpose
#
# if PURPOSE == "learn_hands_on":
#     format = "markdown_with_code_blocks, exercises, checkpoints"
#     
# elif PURPOSE == "transform":
#     format = "narrative_chapters, emotional_arcs"
#     
# elif PURPOSE == "reference":
#     format = "indexed_sections, cross_references, searchable"
