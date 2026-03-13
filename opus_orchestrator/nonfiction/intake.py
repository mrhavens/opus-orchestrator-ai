"""Intake Agent for Nonfiction Book Classification.

A conversational agent that determines the reader purpose and best framework
by asking clarifying questions or using available signals.

This agent intelligently combines:
1. Explicit user flags (--purpose learn)
2. Keyword classification from concept
3. Content inference from existing blog/posts
4. Conversational intake (asking questions)

The agent weights all inputs to make the best decision.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from opus_orchestrator.nonfiction.classifier import PurposeClassifier, ReaderPurpose
from opus_orchestrator.nonfiction.content_infer import ContentPurposeInferer, ContentAnalysis
from opus_orchestrator.nonfiction_taxonomy import (
    select_framework,
    get_frameworks_for_purpose,
    NonfictionCategory,
)


class IntakeMode(str, Enum):
    """How the intake agent operates."""
    CONVERSATIONAL = "conversational"  # Ask questions
    AUTO = "auto"                      # Use classifier only
    EXPLICIT = "explicit"              # Trust flags only


@dataclass
class IntakeInput:
    """All possible inputs to the intake agent."""
    # Option 1: Explicit flags (highest priority if provided)
    explicit_purpose: Optional[str] = None
    explicit_category: Optional[str] = None
    explicit_framework: Optional[str] = None
    
    # Option 2: Concept for classification
    concept: str = ""
    target_audience: str = ""
    intended_outcome: str = ""
    
    # Option 3: Existing content (for inference)
    content: str = ""
    content_title: str = ""
    blog_posts: list = field(default_factory=list)
    
    # Option 4: Previous Q&A (if conversational)
    answers: dict[str, str] = field(default_factory=dict)


@dataclass
class IntakeResult:
    """Result from the intake agent."""
    purpose: ReaderPurpose
    confidence: float
    category: Optional[NonfictionCategory]
    framework: dict
    reasoning: str
    source: str  # "explicit" | "classifier" | "content" | "hybrid"
    content_analysis: Optional[ContentAnalysis] = None
    all_signals: dict = field(default_factory=dict)


class IntakeAgent:
    """Intelligent agent for determining book purpose and framework.
    
    This agent acts as a decision layer that:
    1. Respects explicit user choices (highest priority)
    2. Uses keyword classification when input is clear
    3. Asks clarifying questions when ambiguous
    4. Combines all signals for best accuracy
    """
    
    # Questions for each purpose (for conversational mode)
    PURPOSE_QUESTIONS = {
        ReaderPurpose.LEARN_HANDS_ON: [
            "Should readers be able to DO something specific after reading?",
            "Is this about learning a skill or completing a project?",
            "Do you want step-by-step instructions?",
        ],
        ReaderPurpose.UNDERSTAND: [
            "Is the goal to GRASP a concept or theory?",
            "Do you want readers to understand how something works?",
            "Is this about building mental models?",
        ],
        ReaderPurpose.TRANSFORM: [
            "Is this about personal CHANGE or growth?",
            "Do you want readers to become different?",
            "Is this a self-help or motivational book?",
        ],
        ReaderPurpose.DECIDE: [
            "Is this helping readers MAKE A DECISION?",
            "Are you comparing options or choices?",
            "Do you want to help them choose between alternatives?",
        ],
        ReaderPurpose.REFERENCE: [
            "Is this a COMPREHENSIVE REFERENCE or manual?",
            "Will readers look up specific information?",
            "Is completeness more important than narrative?",
        ],
        ReaderPurpose.BE_INSPIRED: [
            "Is this an INSPIRATIONAL story or biography?",
            "Do you want readers to feel motivated?",
            "Is this about a journey or triumph?",
        ],
    }
    
    # Content inference
    CONTENT_INFERENCE_WEIGHT = 0.4  # Weight for content-based inference
    
    def __init__(self, llm_client=None):
        self.classifier = PurposeClassifier(llm_client)
        self.content_inferer = ContentPurposeInferer()
        self.llm_client = llm_client
    
    async def process(self, intake: IntakeInput, mode: IntakeMode = IntakeMode.AUTO) -> IntakeResult:
        """Process intake and determine purpose and framework.
        
        All signals are weighted:
        1. Explicit flags (weight: 1.0) - highest priority
        2. Content inference (weight: 0.4) - from existing blog/posts
        3. Keyword classification (weight: 0.3) - from concept
        4. Conversational (weight: 0.5) - from Q&A
        
        Args:
            intake: All available input signals
            mode: How to resolve (conversational, auto, explicit)
            
        Returns:
            IntakeResult with purpose, framework, and reasoning
        """
        signals = {}  # Track all signals for reasoning
        
        # Step 1: Check explicit flags (highest priority)
        if intake.explicit_purpose:
            return self._process_explicit(intake)
        
        if mode == IntakeMode.EXPLICIT:
            return self._need_more_info(intake)
        
        # Step 2: Content inference (if content provided)
        content_result = None
        if intake.content or intake.blog_posts:
            if intake.blog_posts:
                content_result = self.content_inferer.infer_from_blog(intake.blog_posts)
            elif intake.content:
                content_result = self.content_inferer.analyze(
                    intake.content, 
                    title=intake.content_title
                )
            signals["content"] = content_result
        
        # Step 3: Keyword classification from concept
        classifier_result = self.classifier._keyword_classify(
            concept=intake.concept,
            target_audience=intake.target_audience,
            intended_outcome=intake.intended_outcome,
        )
        signals["concept"] = classifier_result
        
        # Step 4: WEIGHTED DECISION - combine signals
        purpose_scores: dict[ReaderPurpose, float] = {p: 0.0 for p in ReaderPurpose}
        
        # Add content inference (if available)
        if content_result and content_result.confidence > 0.3:
            purpose_scores[content_result.purpose] += (
                content_result.confidence * self.CONTENT_INFERENCE_WEIGHT
            )
        
        # Add classifier result
        purpose_scores[classifier_result.purpose] += (
            classifier_result.confidence * 0.3
        )
        
        # Find winning purpose
        best_purpose = max(purpose_scores, key=purpose_scores.get)
        best_score = purpose_scores[best_purpose]
        
        # Calculate final confidence
        confidence = min(0.95, best_score)
        
        # If confidence is low and in conversational mode, ask questions
        if confidence < 0.4 and mode == IntakeMode.CONVERSATIONAL:
            return self._need_more_info(intake)
        
        # Determine source
        if content_result and content_result.confidence > 0.5:
            source = "content"
        elif content_result and classifier_result.confidence > 0.3:
            source = "hybrid"
        else:
            source = "classifier"
        
        # Get category from input
        category = None
        if intake.explicit_category:
            try:
                category = NonfictionCategory(intake.explicit_category.lower())
            except ValueError:
                pass
        
        # Select framework
        framework = select_framework(
            purpose=best_purpose,
            category=category,
        )
        
        # Build reasoning
        reasons = []
        if content_result:
            reasons.append(f"content: {content_result.reasoning}")
        reasons.append(f"concept: {classifier_result.reasoning}")
        
        return IntakeResult(
            purpose=best_purpose,
            confidence=confidence,
            category=category,
            framework=framework,
            reasoning=" | ".join(reasons),
            source=source,
            content_analysis=content_result,
            all_signals=signals,
        )
    
    def _process_explicit(self, intake: IntakeInput) -> IntakeResult:
        """Process when user provided explicit purpose."""
        try:
            purpose = ReaderPurpose(intake.explicit_purpose.lower())
        except ValueError:
            # Invalid purpose, fall back to classifier
            return self._process_auto(intake)
        
        # Select framework
        category = None
        if intake.explicit_category:
            try:
                category = NonfictionCategory(intake.explicit_category.lower())
            except ValueError:
                pass
        
        framework = select_framework(
            purpose=purpose,
            category=category,
            user_preferred_framework=intake.explicit_framework,
        )
        
        return IntakeResult(
            purpose=purpose,
            confidence=1.0,
            category=category,
            framework=framework,
            reasoning=f"Explicit user selection: {intake.explicit_purpose}",
            source="explicit",
            content_analysis=None,
            all_signals={"explicit": intake.explicit_purpose},
        )
    
    def _process_auto(self, intake: IntakeInput) -> IntakeResult:
        """Auto-classify from concept."""
        result = self.classifier._keyword_classify(
            concept=intake.concept,
            target_audience=intake.target_audience,
            intended_outcome=intake.intended_outcome,
        )
        return self._build_result_from_classification(intake, result, "classifier")
    
    def _build_result_from_classification(
        self,
        intake: IntakeInput,
        classifier_result,
        source: str,
    ) -> IntakeResult:
        """Build result from classification."""
        purpose = classifier_result.purpose
        
        # Get category from input
        category = None
        if intake.explicit_category:
            try:
                category = NonfictionCategory(intake.explicit_category.lower())
            except ValueError:
                pass
        
        framework = select_framework(
            purpose=purpose,
            category=category,
        )
        
        return IntakeResult(
            purpose=purpose,
            confidence=classifier_result.confidence,
            category=category,
            framework=framework,
            reasoning=classifier_result.reasoning,
            source=source,
        )
    
    def _need_more_info(self, intake: IntakeInput) -> IntakeResult:
        """Return questions needed when input is ambiguous."""
        # This would be used in conversational mode
        # For now, default to UNDERSTAND with low confidence
        return IntakeResult(
            purpose=ReaderPurpose.UNDERSTAND,
            confidence=0.3,
            category=None,
            framework=select_framework(purpose=ReaderPurpose.UNDERSTAND),
            reasoning="Input ambiguous - defaulted to UNDERSTAND. Use --purpose flag for explicit selection.",
            source="intake",
            content_analysis=None,
            all_signals={},
        )
    
    def get_questions(self, purpose: Optional[ReaderPurpose] = None) -> list[str]:
        """Get clarifying questions for a purpose.
        
        Args:
            purpose: The purpose to get questions for, or None for general
            
        Returns:
            List of questions to ask
        """
        if purpose and purpose in self.PURPOSE_QUESTIONS:
            return self.PURPOSE_QUESTIONS[purpose]
        
        # Return all questions
        questions = []
        for q_list in self.PURPOSE_QUESTIONS.values():
            questions.extend(q_list)
        return questions[:5]  # Limit to 5
    
    def get_available_purposes(self) -> list[str]:
        """Get list of available purpose options for menu."""
        return [p.value for p in ReaderPurpose]
    
    def get_available_categories(self) -> list[str]:
        """Get list of available category options."""
        return [c.value for c in NonfictionCategory]


# Convenience function
async def determine_intake(
    concept: str = "",
    purpose: Optional[str] = None,
    category: Optional[str] = None,
    framework: Optional[str] = None,
    target_audience: str = "",
    intended_outcome: str = "",
    mode: str = "auto",
) -> IntakeResult:
    """Convenience function to process intake.
    
    Args:
        concept: Book concept/title
        purpose: Explicit purpose (overrides classification)
        category: Explicit category
        framework: Explicit framework
        target_audience: Target audience description
        intended_outcome: What the book achieves
        mode: "auto", "conversational", or "explicit"
        
    Returns:
        IntakeResult with purpose, framework, etc.
    """
    intake = IntakeInput(
        explicit_purpose=purpose,
        explicit_category=category,
        explicit_framework=framework,
        concept=concept,
        target_audience=target_audience,
        intended_outcome=intended_outcome,
    )
    
    agent = IntakeAgent()
    mode_enum = IntakeMode(mode)
    
    return await agent.process(intake, mode_enum)
