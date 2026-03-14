"""Textbook & Academic Frameworks for Nonfiction.

Educational frameworks for textbooks, courses, curricula, and academic content.
These are the foundational "Field Anchors" for structured learning.
"""

from opus_orchestrator.nonfiction_taxonomy import (
    ReaderPurpose,
    StructuralPattern,
    NonfictionCategory,
)


# =============================================================================
# TEXTBOOK & ACADEMIC FRAMEWORKS
# =============================================================================

TEXTBOOK_FRAMEWORKS = {
    
    # ==========================================================================
    # COMPREHENSIVE TEXTBOOK
    # ==========================================================================
    
    "comprehensive_textbook": {
        "name": "Comprehensive Textbook",
        "description": "The classic academic textbook. Complete coverage of a subject with learning objectives, exercises, and assessment. The gold standard for educational content.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.EDUCATION,
        "stages": [
            "Preface - How to use this book",
            "Chapter 1: Introduction and Foundations",
            "Chapter 2: Core Concepts",
            "Chapter 3: Theory and Principles",
            "Chapter 4: Methods and Techniques",
            "Chapter 5: Applications",
            "Chapter 6: Advanced Topics",
            "Chapter 7: Case Studies",
            "Chapter 8: Synthesis and Integration",
            "Chapter 9: Current Research and Future Directions",
            "Chapter 10: Review and Assessment",
            "Appendix A: Reference Materials",
            "Appendix B: Solutions to Exercises",
            "Glossary",
            "Bibliography",
            "Index",
        ],
        "prompt_template": """Write a comprehensive textbook chapter for: {topic}

Include:
- Learning objectives at the start
- Clear explanations with examples
- Diagrams described in text
- Key terms highlighted
- Exercises at the end
- Summary of key points""",
        "tone_guidance": "Academic, precise, clear. Authoritative but accessible. Like a MIT OpenCourseWare textbook.",
        "typical_length": "50,000-200,000 words",
        "audience": "University students, professionals seeking certification",
        "key_elements": [
            "Learning objectives (Bloom's taxonomy)",
            "Key terms and definitions",
            "Theoretical foundations",
            "Practical applications",
            "Exercises and problems",
            "Case studies",
            "Chapter summaries",
            "Discussion questions",
        ],
    },
    
    # ==========================================================================
    # CHAPTER-BY-CHAPTER TEXTBOOK
    # ==========================================================================
    
    "textbook_chapter": {
        "name": "Textbook Chapter",
        "description": "A single chapter from a comprehensive textbook. Modular, self-contained, but references other chapters.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.EDUCATION,
        "stages": [
            "Opening: Why this matters",
            "Learning Objectives",
            "Core Concept 1: The Fundamentals",
            "Core Concept 2: Building on the Basics",
            "Core Concept 3: Advanced Applications",
            "Real-World Application",
            "Case Study",
            "Common Misconceptions",
            "Exercises (Easy)",
            "Exercises (Intermediate)", 
            "Exercises (Advanced)",
            "Summary",
            "Key Terms",
            "Further Reading",
        ],
        "prompt_template": """Write a complete textbook chapter:

Title: {chapter_title}

Include:
1. Motivating introduction - why this matters
2. Learning objectives (3-5 specific outcomes)
3. Clear explanations with examples
4. Visual descriptions (for figures/diagrams)
5. Key terminology
6. Application to real problems
7. Case study
8. Common mistakes to avoid
9. Exercises at 3 levels
10. Summary
11. Glossary of new terms
12. Recommended further reading""",
        "tone_guidance": "Clear, methodical, encouraging. Patient with difficult concepts.",
        "typical_length": "5,000-15,000 words",
        "audience": "Students in a course using this textbook",
    },
    
    # ==========================================================================
    # ONLINE COURSE / MOOC
    # ==========================================================================
    
    "online_course": {
        "name": "Online Course / MOOC",
        "description": "Massive Open Online Course structure. Modular, video-friendly, with quizzes and assignments. Optimized for self-paced learning.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.EDUCATION,
        "stages": [
            "Course Overview - Welcome and What You'll Learn",
            "Module 1: Foundations",
            "  - Lesson 1.1: Video + Text",
            "  - Lesson 1.2: Video + Text",
            "  - Quiz 1",
            "Module 2: Core Skills",
            "  - Lesson 2.1: Video + Text",
            "  - Lesson 2.2: Video + Text",
            "  - Quiz 2",
            "Module 3: Intermediate Concepts",
            "  - Lesson 3.1: Video + Text",
            "  - Assignment 1",
            "Module 4: Advanced Applications",
            "  - Lesson 4.1: Video + Text",
            "  - Lesson 4.2: Video + Text",
            "  - Final Project",
            "Course Review and Assessment",
            "Certificate Requirements",
            "Next Steps and Further Learning",
        ],
        "prompt_template": """Design an online course module:

Module: {module_name}
Topic: {topic}

For each lesson, provide:
- Learning outcome
- Video script (5-10 min)
- Supplementary text
- Quiz questions (3-5)
- Discussion prompt""",
        "tone_guidance": "Energetic, engaging, conversational. Like the best Coursera or edX instructors.",
        "typical_length": "Variable - can be assembled from lessons",
        "audience": "Online learners of all ages",
    },
    
    # ==========================================================================
    # CURRICULUM / SYLLABUS
    # ==========================================================================
    
    "curriculum": {
        "name": "Curriculum / Syllabus",
        "description": "Complete course curriculum with learning outcomes, assessment criteria, and sequence. Used by educators to plan instruction.",
        "purpose": ReaderPurpose.REFERENCE,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.EDUCATION,
        "stages": [
            "Course Description and Overview",
            "Learning Outcomes (aligned to standards)",
            "Course Schedule / Calendar",
            "Weekly Topics and Readings",
            "Assessment Overview",
            "Grading Policy",
            "Required Materials and Resources",
            "Attendance and Participation Policy",
            "Academic Integrity Policy",
            "Course Policies",
            "Student Support Services",
            "Schedule Detail:",
            "  - Week 1: Topic, Readings, Assignments",
            "  - Week 2: ...",
            "  - ...",
            "Final Assessment Description",
        ],
        "prompt_template": """Create a complete curriculum/syllabus:

Course: {course_name}
Level: {level}
Duration: {weeks} weeks

Include:
1. Course description
2. Learning outcomes (measurable)
3. Weekly schedule with topics and readings
4. Assignment descriptions
5. Grading breakdown
6. Policies
7. Resources""",
        "tone_guidance": "Professional, clear, comprehensive. Official document style.",
        "typical_length": "2,000-5,000 words",
        "audience": "Educators, students, administrators",
    },
    
    # ==========================================================================
    # STUDY GUIDE
    # ==========================================================================
    
    "study_guide": {
        "name": "Study Guide",
        "description": "Student-focused guide for exam preparation. Summarizes key concepts, provides practice problems, includes test-taking strategies.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.EDUCATION,
        "stages": [
            "How to Use This Study Guide",
            "Quick Review: Key Concepts (summary)",
            "Topic 1: Review + Practice Questions",
            "Topic 2: Review + Practice Questions",
            "Topic 3: Review + Practice Questions",
            "Topic 4: Review + Practice Questions",
            "Practice Test 1 (full length)",
            "Practice Test 2 (full length)",
            "Answer Key with Explanations",
            "Test-Taking Strategies",
            "Common Mistakes to Avoid",
            "Last-Minute Review Sheet",
        ],
        "prompt_template": """Create a comprehensive study guide for: {exam_name}

Include:
- Key concepts to know (concise summaries)
- Practice questions per topic
- Full practice tests
- Detailed answer explanations
- Test-taking strategies""",
        "tone_guidance": "Supportive, clear, encouraging. Like a tutor helping you prepare.",
        "typical_length": "10,000-50,000 words",
        "audience": "Students preparing for exams",
    },
    
    # ==========================================================================
    # ACADEMIC PAPER / RESEARCH ARTICLE
    # ==========================================================================
    
    "academic_paper": {
        "name": "Academic Research Paper",
        "description": "Standard academic research article format. IMRAD: Introduction, Methods, Results, And Discussion.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title - Descriptive and specific",
            "Abstract - Complete summary (150-300 words)",
            "Introduction - Background and problem statement",
            "Literature Review - Prior research",
            "Research Questions / Hypotheses",
            "Methodology",
            "Results",
            "Discussion",
            "Limitations",
            "Future Work",
            "Conclusion",
            "References",
            "Appendices",
        ],
        "prompt_template": """Write an academic research paper on: {topic}

Structure: IMRAD (Introduction, Methods, Results, And Discussion)
- Abstract: Summary of entire paper
- Introduction: Problem, significance, research questions
- Methods: How you conducted the research
- Results: What you found
- Discussion: What it means, limitations""",
        "tone_guidance": "Formal, precise, objective. Third person. Hedged appropriately.",
        "typical_length": "5,000-15,000 words",
        "audience": "Academic researchers, peer reviewers",
    },
    
    # ==========================================================================
    # LITERATURE REVIEW
    # ==========================================================================
    
    "literature_review": {
        "name": "Systematic Literature Review",
        "description": "Comprehensive synthesis of existing research on a topic. Used in academia to identify gaps and establish foundations.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.COMPARATIVE,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Introduction - Scope and purpose",
            "Search Methodology - How papers were found",
            "Inclusion/Exclusion Criteria",
            "The Landscape - Overview of research",
            "Theme 1: Foundational Studies",
            "Theme 2: Key Developments",
            "Theme 3: Current State",
            "Methodological Approaches",
            "Gaps in the Literature",
            "Theoretical Framework",
            "Implications for Future Research",
            "Conclusion",
            "References",
        ],
        "prompt_template": """Write a systematic literature review on: {topic}

Structure:
1. How you searched (databases, keywords, dates)
2. What you found (overview)
3. Themes in the literature
4. Methodological approaches used
5. Gaps in the research
6. Implications for future work""",
        "tone_guidance": "Formal, systematic, thorough. Transparent about methodology.",
        "typical_length": "10,000-30,000 words",
        "audience": "Academic researchers, graduate students",
    },
    
    # ==========================================================================
    # THESIS / DISSERTATION
    # ==========================================================================
    
    "thesis": {
        "name": "Thesis / Dissertation",
        "description": "Long-form academic document presenting original research. The definitive form for graduate degrees.",
        "purpose": ReaderPurpose.UNDERSTAND,
        "structure": StructuralPattern.ARGUMENT,
        "category": NonfictionCategory.ACADEMIC,
        "stages": [
            "Title Page",
            "Abstract",
            "Acknowledgments",
            "Table of Contents",
            "List of Figures/Tables",
            "Chapter 1: Introduction",
            "Chapter 2: Literature Review",
            "Chapter 3: Methodology",
            "Chapter 4: Results",
            "Chapter 5: Discussion",
            "Chapter 6: Conclusion",
            "References",
            "Appendices",
        ],
        "prompt_template": """Create a thesis framework for: {research_topic}

Include all standard thesis chapters with guidance on what each should contain.""",
        "tone_guidance": "Formal, rigorous, original contribution. Definitive scholarly voice.",
        "typical_length": "20,000-100,000 words",
        "audience": "Thesis committee, academic community",
    },
    
    # ==========================================================================
    # WORKBOOK / PRACTICE BOOK
    # ==========================================================================
    
    "workbook": {
        "name": "Workbook / Practice Book",
        "description": "Interactive learning with fill-in-the-blank exercises, practice problems, and activities. Active learning focus.",
        "purpose": ReaderPurpose.LEARN_HANDS_ON,
        "structure": StructuralPattern.SEQUENTIAL,
        "category": NonfictionCategory.EDUCATION,
        "stages": [
            "How to Use This Workbook",
            "Unit 1: Foundations",
            "  - Exercise 1.1: Practice",
            "  - Exercise 1.2: Application",
            "  - Exercise 1.3: Challenge",
            "Unit 2: Core Skills",
            "  - Exercise 2.1: Practice",
            "  - Exercise 2.2: Application",
            "  - Exercise 2.3: Challenge",
            "Unit 3: Advanced Applications",
            "  - Exercise 3.1: Practice",
            "  - Exercise 3.2: Integration",
            "  - Exercise 3.3: Mastery",
            "Answer Key",
            "Quick Reference Guide",
        ],
        "prompt_template": """Create an interactive workbook for: {topic}

Include:
- Fill-in-the-blank exercises
- Practice problems at increasing difficulty
- Real-world application activities
- Reflection prompts
- Self-assessment checklists""",
        "tone_guidance": "Active, engaging, interactive. Prompts the learner to participate.",
        "typical_length": "20,000-50,000 words",
        "audience": "Students, self-learners, corporate training",
    },
    
    # ==========================================================================
    # QUICK REFERENCE GUIDE / CHEAT SHEET
    # ==========================================================================
    
    "quick_reference": {
        "name": "Quick Reference Guide",
        "description": "Condensed reference for practitioners. Key concepts, formulas, procedures in portable format. The 'cheat sheet' for professionals.",
        "purpose": ReaderPurpose.REFERENCE,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.EDUCATION,
        "stages": [
            "Introduction - What this covers",
            "Section 1: Key Concepts (quick)",
            "Section 2: Formulas / Rules",
            "Section 3: Procedures / Steps",
            "Section 4: Common Patterns",
            "Section 5: Troubleshooting",
            "Section 6: Tips and Tricks",
            "Quick Examples",
            "Cross-References",
            "Where to Learn More",
        ],
        "prompt_template": """Create a quick reference guide for: {topic}

Format: Condensed, scannable, practical
- Key points only
- No lengthy explanations
- Formulas, rules, procedures
- Common issues and solutions
- Tips from experts""",
        "tone_guidance": "Concise, practical, scannable. Maximum information, minimum words.",
        "typical_length": "2,000-5,000 words",
        "audience": "Practitioners who need quick reminders",
    },
    
    # ==========================================================================
    # KNOWLEDGE BASE / WIKI
    # ==========================================================================
    
    "knowledge_base": {
        "name": "Knowledge Base / Wiki",
        "description": "Organized collection of articles for lookup. Hierarchical, searchable, cross-linked. For organizations and products.",
        "purpose": ReaderPurpose.REFERENCE,
        "structure": StructuralPattern.MODULAR,
        "category": NonfictionCategory.TECHNOLOGY,
        "stages": [
            "Getting Started Guide",
            "Category 1: Core Concepts",
            "  - Article 1.1",
            "  - Article 1.2",
            "Category 2: How-To Guides",
            "  - Article 2.1",
            "  - Article 2.2",
            "Category 3: Troubleshooting",
            "  - Article 3.1",
            "Category 4: Reference",
            "  - Article 4.1",
            "FAQ",
            "Glossary",
            "Index",
        ],
        "prompt_template": """Build a knowledge base article for: {topic}

Include:
- What it is (brief)
- How to use it
- Common use cases
- Troubleshooting
- Related topics""",
        "tone_guidance": "Clear, structured, searchable. Optimized for finding answers.",
        "typical_length": "500-2,000 words per article",
        "audience": "Users looking for specific answers",
    },
    
}


# Add to main frameworks
def get_textbook_frameworks() -> dict:
    """Get all textbook and academic frameworks."""
    return TEXTBOOK_FRAMEWORKS


def suggest_textbook_framework(
    use_case: str,
    audience: str,
    length: str,
) -> str:
    """Suggest the best framework for your use case.
    
    Args:
        use_case: How you'll use it (course, self-study, reference, etc.)
        audience: Who it's for (students, professionals, etc.)
        length: Target length (short, medium, long)
        
    Returns:
        Framework ID
    """
    use_case = use_case.lower()
    audience = audience.lower()
    length = length.lower()
    
    # Course/MOOC
    if "course" in use_case or "mooc" in use_case:
        return "online_course"
    
    # Exam prep
    if "exam" in use_case or "test" in use_case or "prep" in use_case:
        return "study_guide"
    
    # Academic paper
    if "paper" in use_case or "research" in use_case or "academic" in use_case:
        return "academic_paper"
    
    # Thesis
    if "thesis" in use_case or "dissertation" in use_case:
        return "thesis"
    
    # Curriculum
    if "curriculum" in use_case or "syllabus" in use_case:
        return "curriculum"
    
    # Comprehensive textbook
    if "textbook" in use_case:
        if length == "short" or length == "medium":
            return "textbook_chapter"
        return "comprehensive_textbook"
    
    # Workbook/practice
    if "workbook" in use_case or "practice" in use_case or "exercise" in use_case:
        return "workbook"
    
    # Quick reference
    if "quick" in use_case or "reference" in use_case or "cheat" in use_case:
        return "quick_reference"
    
    # Knowledge base
    if "wiki" in use_case or "knowledge" in use_case or "docs" in use_case:
        return "knowledge_base"
    
    # Literature review
    if "literature" in use_case or "review" in use_case:
        return "literature_review"
    
    # Default to textbook chapter
    return "textbook_chapter"
