"""Academic Paper Frameworks - Established Types.

All the well-established academic paper types used in universities and research.
"""

from opus_orchestrator.nonfiction_taxonomy import (
    ReaderPurpose,
    StructuralPattern,
    NonfictionCategory,
)


ACADEMIC_PAPER_TYPES = {
    
    # ==========================================================================
    # RESEARCH PAPERS
    # ==========================================================================
    
    "empirical_paper": {
        "name": "Empirical Research Paper",
        "description": "Based on experiments, observations, or data collection. Reports original findings.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title - Specific and descriptive",
            "Abstract - Complete summary (250 words)",
            "Introduction - Problem, significance, research questions",
            "Literature Review - Prior work",
            "Hypotheses - What you predict",
            "Method - Participants, materials, procedure",
            "Results - What you found (with statistics)",
            "Discussion - What it means",
            "Limitations - What could be better",
            "Future Work - Next steps",
            "Conclusion - Summary",
            "References",
            "Appendices - Supplementary material",
        ],
        "prompt_template": """Write an empirical research paper:

Research Question: {research_question}
Hypotheses: {hypotheses}
Method: {method_description}
Key Findings: {findings}

Follow IMRAD structure: Introduction, Methods, Results, And Discussion.""",
        "tone_guidance": "Objective, precise, evidence-based. Data speaks for itself.",
        "typical_length": "5,000-15,000 words",
        "audience": "Academic peer reviewers, researchers",
    },
    
    "theoretical_paper": {
        "name": "Theoretical / Conceptual Paper",
        "description": "Builds or tests theory. Mathematical proofs, conceptual frameworks, new models.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title - Clear and specific",
            "Abstract - Summary",
            "Introduction - Problem and motivation",
            "Theoretical Background - Foundation",
            "Theoretical Contribution - What you're adding",
            "Core Arguments - The theory itself",
            "Implications - What follows from theory",
            "Limitations - Scope boundaries",
            "Future Research - What to explore",
            "Conclusion",
            "References",
        ],
        "prompt_template": """Write a theoretical paper:

Theoretical Question: {question}
Existing Theory: {prior_work}
Your Contribution: {new_theory}
Implications: {implications}""",
        "tone_guidance": "Logical, rigorous, precise. Mathematical thinking in prose.",
        "typical_length": "8,000-20,000 words",
        "audience": "Theory researchers, academics",
    },
    
    "methodology_paper": {
        "name": "Methodology Paper",
        "description": "Presents a new method, technique, or tool for research. Focus on how something is done.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title",
            "Abstract",
            "Introduction - Why this method matters",
            "Related Methods - What's out there",
            "Proposed Method - Your approach in detail",
            "Theoretical Foundation - Why it works",
            "Implementation - How to use it",
            "Evaluation - How you tested it",
            "Comparison - How it compares to alternatives",
            "Limitations",
            "Future Work",
            "Conclusion",
            "References",
        ],
        "prompt_template": """Write a methodology paper:

Method Name: {method_name}
Problem Solved: {problem}
How It Works: {description}
Comparison to Existing: {comparison}""",
        "tone_guidance": "Technical, detailed, practical. Engineers talking to engineers.",
        "typical_length": "8,000-25,000 words",
        "audience": "Researchers needing to apply the method",
    },
    
    "case_study_paper": {
        "name": "Case Study Paper",
        "description": "In-depth analysis of a specific instance. Qualitative, descriptive, contextual.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title",
            "Abstract",
            "Introduction - Why this case matters",
            "Case Description - The facts",
            "Context - Background",
            "Analysis - What the case reveals",
            "Discussion - What it means generally",
            "Limitations - Generalizability",
            "Conclusion",
            "References",
            "Appendices - Raw data, interview transcripts",
        ],
        "prompt_template": """Write a case study:

Case: {case_description}
Context: {background}
Analysis: {your_analysis}
Key Findings: {findings}
Implications: {what_it_means}""",
        "tone_guidance": "Narrative, rich in detail, analytical. Story + evidence.",
        "typical_length": "5,000-15,000 words",
        "audience": "Practitioners, qualitative researchers",
    },
    
    "survey_paper": {
        "name": "Survey Paper / Literature Survey",
        "description": "Comprehensive overview of the state of a field. Maps what's been done, identifies gaps.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.COMPARATIVE,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title",
            "Abstract",
            "Introduction - Scope and motivation",
            "Taxonomy / Categorization - How to organize the field",
            "Theme 1: Foundational Work",
            "Theme 2: Core Approaches",
            "Theme 3: Recent Advances",
            "Methodological Approaches - How research is done",
            "Key Findings - What's been discovered",
            "Gaps - What's missing",
            "Challenges - Open problems",
            "Future Directions",
            "Conclusion",
            "References (can be 100+)",
        ],
        "prompt_template": """Write a comprehensive survey on: {topic}

Cover:
- All major approaches in the field
- Historical development
- Current state of the art
- Open problems and challenges
- Future directions""",
        "tone_guidance": "Comprehensive, synthetic, authoritative. Bird's eye view.",
        "typical_length": "15,000-50,000 words",
        "audience": "Researchers entering the field",
    },
    
    # ==========================================================================
    # ARGUMENTATIVE PAPERS
    # ==========================================================================
    
    "position_paper": {
        "name": "Position Paper",
        "description": "Argues for a specific stance on an issue. Used in politics, ethics, policy debates.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title - Clear stance",
            "Abstract",
            "Introduction - The issue and why it matters",
            "Background - Context",
            "Position - Your argument",
            "Supporting Arguments - Point 1 with evidence",
            "Supporting Arguments - Point 2 with evidence",
            "Supporting Arguments - Point 3 with evidence",
            "Counterarguments - Objections addressed",
            "Rebuttals - Why objections fail",
            "Implications - Why this matters",
            "Conclusion - Summary and call to action",
            "References",
        ],
        "prompt_template": """Write a position paper:

Issue: {controversial_topic}
Your Position: {your_stance}
Supporting Evidence: {evidence_1}, {evidence_2}, {evidence_3}
Counterarguments: {objections}
Rebuttals: {responses}""",
        "tone_guidance": "Persuasive, evidence-based, fair to opposing views. Concedes ground where valid.",
        "typical_length": "3,000-8,000 words",
        "audience": "Policy makers, debate teams, academic discourse",
    },
    
    "policy_brief": {
        "name": "Policy Brief / White Paper",
        "description": "Recommends action to decision-makers. Short, practical, action-oriented.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.PROBLEM_SOLUTION,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title - Action-oriented",
            "Executive Summary - One page overview",
            "Problem Statement - What's wrong",
            "Current Policy - What's being done",
            "Evidence - What research shows",
            "Options - Possible solutions",
            "Recommendations - What to do",
            "Implementation - How to do it",
            "Cost / Benefits",
            "Risks - What could go wrong",
            "Conclusion",
            "References",
        ],
        "prompt_template": """Write a policy brief:

Policy Issue: {issue}
Current Situation: {status_quo}
Evidence: {research}
Recommendation: {proposed_action}
Why This Works: {rationale}
Costs and Benefits: {analysis}""",
        "tone_guidance": "Practical, concise, actionable. Written for busy executives.",
        "typical_length": "2,000-5,000 words",
        "audience": "Policy makers, executives, advocacy groups",
    },
    
    # ==========================================================================
    # CRITICAL ANALYSIS
    # ==========================================================================
    
    "critical_review": {
        "name": "Critical Review / Critique",
        "description": "Evaluates an existing work (book, article, film). Analysis + judgment.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title - Work being reviewed",
            "Introduction - What you're reviewing, your credentials",
            "Summary - Brief overview of the work",
            "Strengths - What works well",
            "Weaknesses - What doesn't work",
            "Analysis - Deep dive into key aspects",
            "Contribution - What it adds to the field",
            "Comparison - How it compares to similar works",
            "Verdict - Overall evaluation",
            "Conclusion - Who should read it",
            "References",
        ],
        "prompt_template": """Write a critical review of: {work_title}

Your Evaluation: {your_judgment}
Strengths: {what_works}
Weaknesses: {what_doesnt}
Contribution: {what_it_adds}
Who Should Read: {audience}""",
        "tone_guidance": "Analytical, fair, evidence-based. Judgment backed by analysis.",
        "typical_length": "2,000-5,000 words",
        "audience": "Academics, practitioners, general readers",
    },
    
    "meta_analysis": {
        "name": "Meta-Analysis",
        "description": "Statistical synthesis of multiple studies. Quantifies overall effect size.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title",
            "Abstract",
            "Introduction - Question and rationale",
            "Methods - Search strategy, inclusion criteria",
            "PRISMA Flow Diagram - Studies identified",
            "Study Characteristics - What's included",
            "Risk of Bias Assessment",
            "Results - Effect sizes",
            "Heterogeneity - Why studies differ",
            "Publication Bias",
            "Discussion - What findings mean",
            "Limitations",
            "Conclusions",
            "References",
        ],
        "prompt_template": """Write a meta-analysis:

Research Question: {question}
Studies Included: {number}
Overall Effect: {effect_size}
Heterogeneity: {variation}
Conclusion: {implications}""",
        "tone_guidance": "Statistical, precise, transparent about methods.",
        "typical_length": "10,000-30,000 words",
        "audience": "Researchers, clinicians, evidence synthesists",
    },
    
    # ==========================================================================
    # SHORT ACADEMIC
    # ==========================================================================
    
    "short_communication": {
        "name": "Short Communication / Letter",
        "description": "Brief report of significant finding. Fast publication, narrow focus.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.NARRATIVE,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title",
            "Abstract (150 words)",
            "Introduction - Brief context",
            "Methods - Concise",
            "Results - Key findings only",
            "Discussion - Brief implications",
            "Conclusion",
            "References",
        ],
        "prompt_template": "Write a short communication: {key_finding}",
        "tone_guidance": "Concise, direct, no fluff. Maximum information, minimum words.",
        "typical_length": "1,000-2,500 words",
        "audience": "Quick dissemination of important findings",
    },
    
    "conference_proposal": {
        "name": "Conference Proposal / Abstract",
        "description": "Proposes to present at a conference. Pitch your research.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title",
            "Abstract (250-500 words)",
            "Background - Why this matters",
            "Research Question",
            "Method - Brief",
            "Key Findings (expected or actual)",
            "Contribution - What's new",
            "Relevance to Conference Theme",
            "References (optional)",
        ],
        "prompt_template": """Write a conference proposal:

Presentation Title: {title}
Key Message: {main_point}
Why Attendees Care: {audience_value}""",
        "tone_guidance": "Persuasive, clear, engaging. Make them want to attend.",
        "typical_length": "250-1,000 words",
        "audience": "Conference reviewers",
    },
    
    "thesis_proposal": {
        "name": "Thesis / Dissertation Proposal",
        "description": "Proposes the research you'll do for your degree. Gets you the green light.",
        "purpose": ReaderPurpose.DECIDE,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title",
            "Abstract",
            "Introduction - Topic and significance",
            "Literature Review - What's known",
            "Research Questions / Hypotheses",
            "Methodology - How you'll do it",
            "Timeline - When you'll do it",
            "Expected Contributions - What you'll add",
            "Limitations - What you're not doing",
            "Preliminary Findings (if any)",
            "Bibliography",
        ],
        "prompt_template": """Write a thesis proposal:

Research Question: {question}
Why It Matters: {significance}
How You'll Answer: {method}
What You'll Find: {expected_outcomes}""",
        "tone_guidance": "Professional, confident, realistic. Make the case you can do this.",
        "typical_length": "5,000-15,000 words",
        "audience": "Thesis committee",
    },
    
}


# Add to expanded frameworks
def get_academic_paper_types() -> dict:
    """Get all academic paper frameworks."""
    return ACADEMIC_PAPER_TYPES


def suggest_academic_paper(
    research_type: str = "",
    purpose: str = "",
    length: str = "",
) -> str:
    """Suggest the best paper type for your needs.
    
    Args:
        research_type: empirical, theoretical, case study, etc.
        purpose: argue, report, analyze, etc.
        length: short, medium, long
        
    Returns:
        Framework ID
    """
    research_type = (research_type or "").lower()
    purpose = (purpose or "").lower()
    length = (length or "").lower()
    
    # Match by research type
    if "empiric" in research_type or "experiment" in research_type or "data" in research_type:
        return "empirical_paper"
    
    if "theoret" in research_type or "conceptual" in research_type or "model" in research_type:
        return "theoretical_paper"
    
    if "method" in research_type or "technique" in research_type:
        return "methodology_paper"
    
    if "case" in research_type:
        return "case_study_paper"
    
    if "survey" in research_type or "literature" in research_type or "review" in research_type:
        return "survey_paper"
    
    if "position" in research_type or "argument" in research_type:
        return "position_paper"
    
    if "policy" in research_type or "white" in research_type:
        return "policy_brief"
    
    if "critical" in research_type or "review" in research_type:
        return "critical_review"
    
    if "meta" in research_type:
        return "meta_analysis"
    
    # Match by purpose
    if "decide" in purpose or "recommend" in purpose or "action" in purpose:
        return "policy_brief"
    
    if "understand" in purpose or "synthesize" in purpose:
        return "survey_paper"
    
    # Default
    return "empirical_paper"
