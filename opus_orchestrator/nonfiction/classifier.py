"""Purpose Classifier for Nonfiction Books.

Classifies user input into ReaderPurpose - why the reader will be reading this book.
This is the foundation for the entire nonfiction pipeline.

Usage:
    from opus_orchestrator.nonfiction.classifier import PurposeClassifier, ReaderPurpose
    
    classifier = PurposeClassifier()
    result = await classifier.classify(
        concept="Leadership for introverts",
        target_audience="Introverted professionals who want to develop leadership skills",
        intended_outcome="Learn to lead with quiet confidence"
    )
    
    print(result.purpose)       # ReaderPurpose.TRANSFORM
    print(result.confidence)    # 0.87
    print(result.reasoning)    # "Target audience wants 'develop' - indicates self-transformation"
"""

import re
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ReaderPurpose(str, Enum):
    """Why is the reader reading this book?"""
    LEARN_HANDS_ON = "learn_hands_on"
    UNDERSTAND = "understand"
    TRANSFORM = "transform"
    DECIDE = "decide"
    REFERENCE = "reference"
    BE_INSPIRED = "be_inspired"


@dataclass
class ClassificationResult:
    """Result of purpose classification."""
    purpose: ReaderPurpose
    confidence: float
    reasoning: str
    alternative_purposes: Optional[list] = None


class PurposeClassifier:
    """Classifies user input into ReaderPurpose.
    
    Uses keyword-based classification with optional LLM enhancement.
    """
    
    PURPOSE_KEYWORDS = {
        ReaderPurpose.LEARN_HANDS_ON: [
            "how to", "how-to", "learn to", "master", "step by step",
            "beginner's guide", "tutorial", "practical", "hands-on",
            "skills", "do it yourself", "build", "create", "make",
            "implement", "develop skills", "learn skills", "course",
            "workshop", "training", "teach yourself", "guide to",
            "becoming", "learn the basics", "fundamentals",
        ],
        ReaderPurpose.UNDERSTAND: [
            "understand", "why", "how it works", "explain", "concept",
            "mental model", "deep dive", "exploration", "the nature of",
            "the truth about", "what is", "meaning", "philosophy",
            "theory", "framework", "principles", "inside story",
            "real story", "hidden", "secret", "science of",
            "psychology of", "the way", "essence", "sapiens",
        ],
        ReaderPurpose.TRANSFORM: [
            "transform", "change", "become", "develop", "improve",
            "better", "overcome", "heal", "grow", "personal growth",
            "self-improvement", "self help", "empower", "breakthrough",
            "awakening", "journey", "awaken", "reinvent",
            "reclaim", "freedom", "love yourself", "healing",
            "recovery", "manifest", "attract", "abundance",
            "habits", "routines", "mindset", "productivity",
        ],
        ReaderPurpose.DECIDE: [
            "decide", "choose", "compare", "vs", "versus",
            "which is better", "pros and cons", "trade-off", "decision",
            "guide", "strategies", "strategy", "choosing", "selecting",
            "investment", "where to put", "how to allocate", "prioritize",
            "business case", "roi", "worth it", "should i", "analysis",
        ],
        ReaderPurpose.REFERENCE: [
            "reference", "manual", "handbook", "dictionary", "encyclopedia",
            "comprehensive", "complete guide", "all about", "definitive",
            "bible", "catalog", "directory", "index", "lookup",
            "specification", "documentation", "api", "technical",
            "architecture", "system design", "best practices",
        ],
        ReaderPurpose.BE_INSPIRED: [
            "inspire", "motivational", "biography", "memoir", "story",
            "life", "journey", "triumph", "overcoming", "against all odds",
            "unstoppable", "dream", "vision", "legacy", "purpose",
            "calling", "warrior", "hero", "legend", "icon",
        ],
    }
    
    PURPOSE_NEGATIONS = {
        ReaderPurpose.LEARN_HANDS_ON: ["understand", "explain", "why", "concept"],
        ReaderPurpose.TRANSFORM: ["reference", "manual", "tutorial"],
        ReaderPurpose.UNDERSTAND: ["how to", "step by step", "tutorial"],
    }
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
    
    async def classify(
        self,
        concept: str,
        target_audience: str = "",
        intended_outcome: str = "",
    ) -> ClassificationResult:
        """Classify user input into ReaderPurpose."""
        keyword_result = self._keyword_classify(concept, target_audience, intended_outcome)
        
        if keyword_result.confidence >= 0.8:
            return keyword_result
        
        if self.llm_client:
            try:
                llm_result = await self._llm_classify(concept, target_audience, intended_outcome)
                if llm_result.confidence > keyword_result.confidence:
                    return llm_result
            except Exception:
                pass
        
        return keyword_result
    
    def _keyword_classify(
        self,
        concept: str,
        target_audience: str,
        intended_outcome: str,
    ) -> ClassificationResult:
        """Fast keyword-based classification."""
        text = f"{concept} {target_audience} {intended_outcome}".lower()
        
        scores = {p: 0 for p in ReaderPurpose}
        
        for purpose, keywords in self.PURPOSE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    scores[purpose] += 1
        
        for purpose, negations in self.PURPOSE_NEGATIONS.items():
            for negation in negations:
                if negation.lower() in text:
                    scores[purpose] = max(0, scores[purpose] - 1)
        
        if max(scores.values()) == 0:
            return ClassificationResult(
                purpose=ReaderPurpose.UNDERSTAND,
                confidence=0.3,
                reasoning="No clear purpose keywords found, defaulting to UNDERSTAND",
            )
        
        sorted_purposes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_purpose, top_score = sorted_purposes[0]
        
        total_score = sum(1 for s in scores.values() if s > 0)
        confidence = min(0.95, top_score / max(1, total_score)) if total_score > 0 else 0.3
        
        matched_keywords = [kw for kw in self.PURPOSE_KEYWORDS[top_purpose] 
                         if kw.lower() in text]
        
        return ClassificationResult(
            purpose=top_purpose,
            confidence=confidence,
            reasoning=f"Keywords matched: {', '.join(matched_keywords[:5])}",
        )
    
    async def _llm_classify(
        self,
        concept: str,
        target_audience: str,
        intended_outcome: str,
    ) -> ClassificationResult:
        """LLM-based classification."""
        prompt = f"""Analyze this book concept and determine WHY a reader would read this book.

## Input
- Concept/Title: {concept}
- Target Audience: {target_audience or '(not specified)'}
- Intended Outcome: {intended_outcome or '(not specified)'}

## Options
1. LEARN_HANDS_ON: Reader wants to DO something specific
2. UNDERSTAND: Reader wants to GRASP a concept deeply  
3. TRANSFORM: Reader wants to CHANGE themselves
4. DECIDE: Reader wants to make an informed decision
5. REFERENCE: Reader wants to LOOK UP information
6. BE_INSPIRED: Reader wants to feel motivated

## Output Format (JSON only)
{{
  "purpose": "one of: learn_hands_on, understand, transform, decide, reference, be_inspired",
  "confidence": 0.0 to 1.0,
  "reasoning": "1-2 sentences explaining why"
}}

Analyze:"""

        result = await self.llm_client.complete_async(
            system_prompt="You are a book categorization system. Return ONLY valid JSON.",
            user_prompt=prompt,
            temperature=0.3,
            max_tokens=500,
        )
        
        return self._parse_llm_result(result)
    
    def _parse_llm_result(self, result: str) -> ClassificationResult:
        """Parse LLM response."""
        try:
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                json_str = result.split("```")[1].split("```")[0]
            else:
                start, end = result.find("{"), result.rfind("}") + 1
                if start >= 0 and end > start:
                    json_str = result[start:end]
                else:
                    raise ValueError("No JSON found")
            
            data = json.loads(json_str)
            
            purpose_map = {
                "learn_hands_on": ReaderPurpose.LEARN_HANDS_ON,
                "learn": ReaderPurpose.LEARN_HANDS_ON,
                "understand": ReaderPurpose.UNDERSTAND,
                "transform": ReaderPurpose.TRANSFORM,
                "decide": ReaderPurpose.DECIDE,
                "reference": ReaderPurpose.REFERENCE,
                "be_inspired": ReaderPurpose.BE_INSPIRED,
                "be inspired": ReaderPurpose.BE_INSPIRED,
            }
            
            purpose_str = data.get("purpose", "").lower()
            purpose = purpose_map.get(purpose_str, ReaderPurpose.UNDERSTAND)
            
            return ClassificationResult(
                purpose=purpose,
                confidence=float(data.get("confidence", 0.7)),
                reasoning=data.get("reasoning", "LLM classification"),
            )
        except (json.JSONDecodeError, ValueError) as e:
            return ClassificationResult(
                purpose=ReaderPurpose.UNDERSTAND,
                confidence=0.3,
                reasoning=f"LLM parse failed, defaulting to UNDERSTAND",
            )


async def classify_purpose(
    concept: str,
    target_audience: str = "",
    intended_outcome: str = "",
    llm_client=None,
) -> ClassificationResult:
    """Convenience function to classify purpose."""
    classifier = PurposeClassifier(llm_client)
    return await classifier.classify(concept, target_audience, intended_outcome)
