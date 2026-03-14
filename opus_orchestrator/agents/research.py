"""Research Agent for Opus Orchestrator.

Enhanced nonfiction agent with live research capabilities.
"""

import os
from typing import Any, Optional

from dotenv import load_dotenv


from opus_orchestrator.agents.base import BaseAgent, AgentResponse
from opus_orchestrator.utils.research import (
    ResearchOrchestrator,
    create_research_orchestrator,
    SearchTool,
    WikipediaTool,
    AcademicSearchTool,
)


# System prompt for research agent
RESEARCH_AGENT_SYSTEM_PROMPT = """## Role: Research Agent with Live Web Access

You are The Researcher — an AI agent with live access to the internet, academic databases, and research tools.

## Your Capabilities

1. **Web Search** - Search the current web for latest information
2. **Wikipedia** - Access encyclopedic knowledge
3. **Academic Search** - Find peer-reviewed papers (CrossRef, Semantic Scholar)
4. **Innovation Detection** - Identify gaps and new ideas beyond training data

## Your Mission

NOT just verify facts — **DISCOVER new information, trends, and innovations**.

- Find what's NEW since your training cutoff
- Identify research gaps and opportunities  
- Connect disparate ideas into novel insights
- Go beyond what you "know" to what you can FIND

## Research Process

1. **Explore** - Broad search on topic
2. **Deep Dive** - Specific searches on subtopics
3. **Cross-Reference** - Find connections between sources
4. **Innovate** - Generate original insights beyond training data

## Output Format

Provide your research in this structure:

```
## Findings (What you discovered)
- [New information 1]
- [New information 2]
- [Latest developments]

## Sources (Where you found it)
- [URL 1]: [Title]
- [URL 2]: [Title]

## Innovations (Original insights beyond training data)
- [Novel connection 1]
- [Novel connection 2]

## Research Gaps (What's not well-covered)
- [Gap 1]
- [Gap 2]
```

## Remember

You're not just fact-checking — you're RESEARCHING. Actively seek new information, 
challenge assumptions, and generate original ideas. This keeps the content fresh 
and prevents "AI slop" from repetitive training data patterns.
"""


class ResearchAgent(BaseAgent):
    """Enhanced research agent with live web access and innovation detection."""
    
    def __init__(
        self,
        config=None,
        search_provider: str = "tavily",
        use_wikipedia: bool = True,
        use_academic: bool = True,
    ):
        """Initialize research agent with tools.
        
        Args:
            config: Agent configuration
            search_provider: Search provider (tavily, serper, brave, duckduckgo)
            use_wikipedia: Include Wikipedia search
            use_academic: Include academic search
        """
        # Initialize research tools
        self.research = create_research_orchestrator(
            search_provider=search_provider,
            use_wikipedia=use_wikipedia,
            use_academic=use_academic,
        )
        
        self.search_tool = SearchTool(provider=search_provider)
        self.wikipedia = WikipediaTool() if use_wikipedia else None
        self.academic = AcademicSearchTool() if use_academic else None
        
        super().__init__(
            role="Research Agent",
            description="Live web research with innovation detection",
            system_prompt=RESEARCH_AGENT_SYSTEM_PROMPT,
            config=config,
        )

    async def execute(self, input_data: Any, context: dict[str, Any]) -> AgentResponse:
        """Execute research task with live tools.
        
        Args:
            input_data: Research query and parameters
            context: Additional context
            
        Returns:
            Research findings with sources and innovations
        """
        # Extract query
        if isinstance(input_data, dict):
            query = input_data.get("query", "")
            subtopics = input_data.get("subtopics", [])
            deep = input_data.get("deep_research", False)
        else:
            query = str(input_data)
            subtopics = []
            deep = False
        
        if not query:
            return AgentResponse(
                success=False,
                output=None,
                error="No research query provided",
                metadata={"role": "Research Agent"},
            )
        
        try:
            # Perform research
            if deep or subtopics:
                # Deep research with subtopics
                results = self.research.deep_research(query, subtopics)
            else:
                # Quick comprehensive search
                results = self.research.comprehensive_search(query)
            
            # Format results for LLM
            research_summary = self._format_research_for_llm(results)
            
            # Use LLM to synthesize and provide analysis
            synthesis = await self.call_llm(
                system_prompt=self.build_system_prompt(context),
                user_prompt=f"""Based on this research data, provide analysis and insights:

{research_summary}

Task: {query}

Provide:
1. Key findings synthesized
2. Most important innovations/discoveries
3. How this goes beyond typical training data
4. Recommendations for the manuscript""",
            )
            
            return AgentResponse(
                success=True,
                output={
                    "raw_results": results,
                    "synthesis": synthesis,
                    "query": query,
                },
                metadata={
                    "role": "Research Agent",
                    "search_provider": self.research.search.provider,
                },
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                output=None,
                error=f"Research failed: {str(e)}",
                metadata={"role": "Research Agent"},
            )
    
    def _format_research_for_llm(self, results: dict) -> str:
        """Format research results for LLM consumption."""
        output = []
        
        # Query
        output.append(f"# Research Query: {results.get('query', '')}")
        output.append(f"Timestamp: {results.get('timestamp', '')}")
        output.append("")
        
        # Web results
        web = results.get("web", [])
        if web:
            output.append("## Web Search Results")
            for i, r in enumerate(web[:5], 1):
                output.append(f"{i}. **{r.get('title', '')}**")
                output.append(f"   URL: {r.get('url', '')}")
                output.append(f"   {r.get('content', '')[:200]}...")
                output.append("")
        
        # Wikipedia
        wiki = results.get("wikipedia", [])
        if wiki:
            output.append("## Wikipedia Results")
            for r in wiki[:3]:
                output.append(f"- {r.get('title', '')}: {r.get('summary', '')[:200]}...")
            output.append("")
        
        # Academic
        academic = results.get("academic", [])
        if academic:
            output.append("## Academic Papers")
            for r in academic[:5]:
                output.append(f"- {r.get('title', '')} ({r.get('year', 'N/A')})")
                output.append(f"  {r.get('journal', '')}")
            output.append("")
        
        # Innovations
        innovations = results.get("innovations", [])
        if innovations:
            output.append("## Innovations & New Ideas")
            for i in innovations:
                output.append(f"- {i}")
            output.append("")
        
        return "\n".join(output)


# Fact-checking with live verification
class VerifiedFactChecker:
    """Fact checker with live source verification."""
    
    def __init__(self, search_provider: str = "tavily"):
        """Initialize verified fact checker."""
        self.search = SearchTool(provider=search_provider)
        self.wikipedia = WikipediaTool()
    
    async def verify_claim(
        self,
        claim: str,
        context: str = "",
    ) -> dict:
        """Verify a factual claim against live sources.
        
        Args:
            claim: The claim to verify
            context: Additional context
            
        Returns:
            Verification result with confidence and sources
        """
        # Search for the claim
        results = self.search.search(claim, num_results=5)
        
        # Check Wikipedia
        wiki_results = self.wikipedia.search(claim, num_results=2)
        
        # Analyze
        supporting = []
        contradicting = []
        neutral = []
        
        for r in results:
            content = r.get("content", "").lower()
            claim_lower = claim.lower()
            
            # Simple keyword matching
            claim_words = set(claim_lower.split())
            content_words = set(content.split())
            overlap = claim_words & content_words
            
            if len(overlap) > len(claim_words) * 0.7:
                supporting.append(r)
            elif "not" in content or "false" in content or "incorrect" in content:
                contradicting.append(r)
            else:
                neutral.append(r)
        
        # Calculate confidence
        total = len(supporting) + len(contradicting) + len(neutral)
        if total == 0:
            confidence = 0.0
        else:
            confidence = len(supporting) / total
        
        return {
            "claim": claim,
            "verified": len(supporting) > 0,
            "confidence": confidence,
            "supporting_sources": supporting,
            "contradicting_sources": contradicting,
            "neutral_sources": neutral,
            "needs_citation": confidence < 0.8,
        }
    
    async def verify_batch(
        self,
        claims: list[str],
    ) -> list[dict]:
        """Verify multiple claims.
        
        Args:
            claims: List of claims to verify
            
        Returns:
            List of verification results
        """
        results = []
        for claim in claims:
            result = await self.verify_claim(claim)
            results.append(result)
        return results


def create_research_agent(
    search_provider: str = "tavily",
) -> ResearchAgent:
    """Factory to create a research agent.
    
    Args:
        search_provider: Search provider
        
    Returns:
        Configured ResearchAgent
    """
    return ResearchAgent(search_provider=search_provider)
