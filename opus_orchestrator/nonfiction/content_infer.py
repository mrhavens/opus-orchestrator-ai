"""Content-Based Purpose Inference.

Analyzes existing content to infer the reader purpose.
This allows the system to determine purpose from blog posts, articles, etc.
"""

from dataclasses import dataclass
from typing import Optional

from opus_orchestrator.nonfiction.classifier import ReaderPurpose


@dataclass
class ContentAnalysis:
    """Result of analyzing content for purpose."""
    purpose: ReaderPurpose
    confidence: float
    reasoning: str
    signals: dict


class ContentPurposeInferer:
    """Infers reader purpose from existing content.
    
    Analyzes blog posts, articles, or other content to determine
    what kind of book this content would become.
    """
    
    # Content patterns that indicate purpose
    CONTENT_SIGNALS = {
        ReaderPurpose.LEARN_HANDS_ON: {
            "indicators": [
                "step by step", "how to", "tutorial", "guide to",
                "instructions", "learn to", "course", "workshop",
                "example code", "exercise", "practice", "build a",
                "create a", "implement", "getting started",
            ],
            "structure": ["step", "chapter", "lesson", "module", "exercise"],
        },
        ReaderPurpose.UNDERSTAND: {
            "indicators": [
                "why", "explains", "understand", "concept of",
                "the nature of", "how it works", "mechanism",
                "deep dive", "analysis", "framework", "principles",
                "mental model", "theory", "psychology", "science",
            ],
            "structure": ["overview", "background", "core concepts", "implications"],
        },
        ReaderPurpose.TRANSFORM: {
            "indicators": [
                "i was", "i became", "my journey", "transformation",
                "overcoming", "struggle", "breakthrough", "changed my life",
                "how i", "from", "to", "becoming", "awakening",
                "healing", "recovery", "manifest", "empower",
            ],
            "structure": ["before", "after", "journey", "struggle", "triumph"],
        },
        ReaderPurpose.DECIDE: {
            "indicators": [
                "compared to", "versus", "pros and cons", "should you",
                "which is better", "is it worth", "decision", "choose",
                "analysis", "recommendation", "best", "top", "ranking",
                "tradeoff", "evaluation", "case study",
            ],
            "structure": ["comparison", "versus", "pros", "cons", "verdict"],
        },
        ReaderPurpose.REFERENCE: {
            "indicators": [
                "reference", "documentation", "api", "specification",
                "manual", "handbook", "comprehensive", "complete guide",
                "all about", "definitive", "index", "table of contents",
            ],
            "structure": ["reference", "api", "syntax", "parameters", "examples"],
        },
        ReaderPurpose.BE_INSPIRED: {
            "indicators": [
                "story", "journey", "triumph", "against all odds",
                "inspiration", "motivation", "life lesson", "wisdom",
                "legacy", "calling", "warrior", "hero", "unstoppable",
            ],
            "structure": ["chapter one", "the beginning", "the end", "epilogue"],
        },
    }
    
    # Negative signals (reduce confidence)
    NEGATION_PATTERNS = {
        ReaderPurpose.LEARN_HANDS_ON: ["theory", "why", "explain", "concept"],
        ReaderPurpose.TRANSFORM: ["reference", "documentation", "api"],
    }
    
    def analyze(
        self,
        content: str,
        title: str = "",
        meta_description: str = "",
    ) -> ContentAnalysis:
        """Analyze content to infer purpose.
        
        Args:
            content: The text content to analyze
            title: Title of the content
            meta_description: Meta description if available
            
        Returns:
            ContentAnalysis with inferred purpose
        """
        # Combine all text
        full_text = f"{title} {meta_description} {content}".lower()
        
        # Score each purpose
        scores: dict[ReaderPurpose, float] = {p: 0.0 for p in ReaderPurpose}
        signal_counts: dict[ReaderPurpose, list[str]] = {p: [] for p in ReaderPurpose}
        
        for purpose, patterns in self.CONTENT_SIGNALS.items():
            # Count indicator matches
            for indicator in patterns["indicators"]:
                if indicator.lower() in full_text:
                    scores[purpose] += 1.0
                    signal_counts[purpose].append(indicator)
            
            # Check structure patterns
            for structure in patterns.get("structure", []):
                if structure.lower() in full_text:
                    scores[purpose] += 0.5
        
        # Apply negations (reduce scores)
        for purpose, negations in self.NEGATION_PATTERNS.items():
            for negation in negations:
                if negation.lower() in full_text:
                    scores[purpose] = max(0, scores[purpose] - 0.5)
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            normalized = {p: s / total_score for p, s in scores.items()}
        else:
            normalized = {p: 0.1 for p in ReaderPurpose}  # Uniform if no matches
        
        # Find best match
        best_purpose = max(normalized, key=normalized.get)
        best_score = normalized[best_purpose]
        
        # Calculate confidence
        if best_score > 0.5:
            confidence = min(0.95, 0.5 + best_score * 0.5)
        elif best_score > 0.2:
            confidence = min(0.7, 0.3 + best_score * 0.4)
        else:
            confidence = 0.3
        
        # Build reasoning
        signals = signal_counts[best_purpose]
        if signals:
            reasoning = f"Content signals: {', '.join(signals[:5])}"
        else:
            reasoning = "No strong signals - purpose unclear"
        
        return ContentAnalysis(
            purpose=best_purpose,
            confidence=confidence,
            reasoning=reasoning,
            signals={p.value: c for p, c in signal_counts.items() if c},
        )
    
    def infer_from_blog(self, blog_posts: list[dict]) -> ContentAnalysis:
        """Infer purpose from multiple blog posts.
        
        Args:
            blog_posts: List of dicts with 'title', 'content', 'excerpt'
            
        Returns:
            Aggregated ContentAnalysis
        """
        all_text = ""
        titles = []
        
        for post in blog_posts:
            all_text += post.get("content", "") + " "
            all_text += post.get("excerpt", "") + " "
            titles.append(post.get("title", ""))
        
        result = self.analyze(all_text, title="; ".join(titles))
        
        # If multiple posts, boost confidence slightly
        if len(blog_posts) > 3:
            result.confidence = min(0.95, result.confidence + 0.1)
        
        return result


# Convenience function
def infer_purpose_from_content(
    content: str,
    title: str = "",
    meta_description: str = "",
) -> ContentAnalysis:
    """Convenience function to infer purpose from content.
    
    Args:
        content: The text content
        title: Title of the content
        meta_description: Optional meta description
        
    Returns:
        ContentAnalysis with inferred purpose
    """
    inferer = ContentPurposeInferer()
    return inferer.analyze(content, title, meta_description)
