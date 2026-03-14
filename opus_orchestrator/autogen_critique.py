"""AutoGen Critique Crew for Opus Orchestrator.

Multi-agent critique system using AutoGen.
Writers, Critics, and Editors collaborate to improve chapters.
"""

import os
from typing import Any, Optional

from dotenv import load_dotenv


from autogen import ConversableAgent, GroupChat, GroupChatManager


class CritiqueCrew:
    """Multi-agent critique crew using AutoGen."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.agents = {}
        self.group_chat = None
        self.manager = None
        
        self._create_agents()
    
    def _create_agents(self):
        """Create the critique crew agents."""
        
        # Literary Critic - evaluates prose quality
        self.agents["literary_critic"] = ConversableAgent(
            name="LiteraryCritic",
            system_message="""You are a Literary Critic with expertise in prose quality.

Evaluate chapters for:
- Sentence rhythm and variation
- Word choice and vocabulary
- Show vs. tell balance
- Prose style consistency
- Emotional resonance

Provide specific, actionable feedback. Rate strengths and weaknesses.
Return your critique as a JSON with: {"score": 0.0-1.0, "strengths": [], "weaknesses": [], "suggestions": []}""",
            llm_config={
                "model": self.model,
                "api_key": self.api_key,
                "temperature": 0.7,
            },
            human_input_mode="NEVER",
        )
        
        # Genre Expert - evaluates genre conventions
        self.agents["genre_expert"] = ConversableAgent(
            name="GenreExpert",
            system_message="""You are a Genre Expert with deep knowledge of storytelling conventions.

Evaluate chapters for:
- Genre convention adherence
- Tropes and expectations
- Subgenre-specific elements
- Reader expectation management
- Genre-specific pacing

Provide feedback on how well the chapter serves its genre.
Return your critique as a JSON with: {"score": 0.0-1.0, "strengths": [], "weaknesses": [], "suggestions": []}""",
            llm_config={
                "model": self.model,
                "api_key": self.api_key,
                "temperature": 0.7,
            },
            human_input_mode="NEVER",
        )
        
        # Story Editor - evaluates plot and structure
        self.agents["story_editor"] = ConversableAgent(
            name="StoryEditor",
            system_message="""You are a Story Editor with expertise in narrative structure.

Evaluate chapters for:
- Plot progression
- Character consistency
- Pacing and tension
- Scene purpose
- Narrative flow
- Information revelation

Provide feedback on story elements.
Return your critique as a JSON with: {"score": 0.0-1.0, "strengths": [], "weaknesses": [], "suggestions": []}""",
            llm_config={
                "model": self.model,
                "api_key": self.api_key,
                "temperature": 0.7,
            },
            human_input_mode="NEVER",
        )
        
        # The Writer - receives feedback and revises
        self.agents["writer"] = ConversableAgent(
            name="Writer",
            system_message="""You are a Professional Writer.

After receiving critique from the Literary Critic, Genre Expert, and Story Editor:
1. Consider each feedback point
2. Identify what to revise
3. Output your revision plan

You do NOT rewrite - you plan revisions. Return: {"revision_plan": [], "priorities": []}""",
            llm_config={
                "model": self.model,
                "api_key": self.api_key,
                "temperature": 0.7,
            },
            human_input_mode="NEVER",
        )
        
        # Create group chat for multi-agent discussion
        self.group_chat = GroupChat(
            agents=[
                self.agents["literary_critic"],
                self.agents["genre_expert"],
                self.agents["story_editor"],
            ],
            messages=[],
            max_round=3,
        )
        
        # FIX: Add LLM config to manager
        self.manager = GroupChatManager(
            groupchat=self.group_chat,
            llm_config={
                "model": self.model,
                "api_key": self.api_key,
                "temperature": 0.7,
            }
        )
    
    def critique_chapter(
        self,
        chapter_content: str,
        chapter_num: int,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Run critique on a chapter.
        
        Args:
            chapter_content: The chapter text
            chapter_num: Chapter number
            context: Story context (one_sentence, genre, etc.)
            
        Returns:
            Aggregated critique with scores and suggestions
        """
        # Prepare the critique request
        critique_request = f"""Critique Chapter {chapter_num}.

## Chapter Content:
{chapter_content[:3000]}...

## Story Context:
- Genre: {context.get('genre', 'general')}
- One Sentence: {context.get('one_sentence', 'N/A')}
- Chapter Summary: {context.get('summary', 'N/A')}

## Your Task:
Each of you evaluate the chapter from your specialty perspective.
After each critique, discuss and reach consensus on:
1. Overall score (0.0-1.0)
2. Top 3 strengths
3. Top 3 weaknesses
4. Priority revision suggestions

End with a final verdict: APPROVED, MINOR_REVISIONS, or MAJOR_REVISIONS.
"""
        
        # Initiate group chat critique
        result = self.agents["literary_critic"].initiate_chat(
            self.manager,
            message=critique_request,
            summary_method="reflection_with_llm",
        )
        
        # Parse the result (simplified - in production would extract structured data)
        return self._parse_critique_result(result, chapter_num)
    
    def _parse_critique_result(self, result: Any, chapter_num: int) -> dict[str, Any]:
        """Parse the AutoGen result into structured critique."""
        # Simplified parsing - in production would use structured output
        summary = result.summary if hasattr(result, 'summary') else str(result)
        
        # Try to extract scores
        score = 0.75  # Default
        if 'APPROVED' in summary.upper():
            score = 0.9
        elif 'MAJOR' in summary.upper():
            score = 0.5
        elif 'MINOR' in summary.upper():
            score = 0.7
        
        return {
            "chapter_number": chapter_num,
            "overall_score": score,
            "summary": summary[:1000],
            "critics": ["LiteraryCritic", "GenreExpert", "StoryEditor"],
            "approved": score >= 0.8,
            "revision_priority": "approved" if score >= 0.8 else ("minor_revisions" if score >= 0.6 else "major_revisions"),
        }
    
    def iterate_chapter(
        self,
        chapter_content: str,
        chapter_num: int,
        context: dict[str, Any],
        max_iterations: int = 2,
    ) -> dict[str, Any]:
        """Iterate on a chapter until approved or max iterations.
        
        Args:
            chapter_content: Initial chapter text
            chapter_num: Chapter number
            context: Story context
            max_iterations: Maximum revision rounds
            
        Returns:
            Final critique result
        """
        current_content = chapter_content
        
        for iteration in range(1, max_iterations + 1):
            print(f"   🔄 Critique iteration {iteration}/{max_iterations}")
            
            # Get critique
            critique = self.critique_chapter(current_content, chapter_num, context)
            
            # Check if approved
            if critique["approved"]:
                print(f"   ✅ Chapter {chapter_num} approved!")
                return {
                    **critique,
                    "revised_content": current_content,
                }
            
            # Not approved - get revision suggestions and apply them
            if iteration < max_iterations:
                print(f"   📝 Score: {critique['overall_score']:.2f} - applying revisions...")
                
                # Use the Writer agent to revise based on critique
                revision_suggestions = critique.get("summary", "")[:2000]
                
                try:
                    # Request revision from Writer agent
                    revision_request = f"""Revise Chapter {chapter_num} based on critique feedback.

## Current Chapter Content:
{current_content[:3000]}...

## Critique Feedback:
{revision_suggestions}

## Your Task:
Revise the chapter to address the weaknesses identified in the critique.
Preserve the strengths. Improve the story, pacing, and prose.
"""
                    # Use the writer agent to revise
                    revision_result = self.agents["writer"].initiate_chat(
                        self.manager,
                        message=revision_request,
                        summary_method="reflection_with_llm",
                    )
                    
                    # Extract revised content from the chat
                    if hasattr(revision_result, 'chat_history'):
                        # Get the last response as revised content
                        revised = revision_result.chat_history[-1].get('content', '') if revision_result.chat_history else current_content
                        if revised and len(revised) > 100:
                            current_content = revised
                            print(f"   ✏️  Revision applied, new length: {len(current_content)} chars")
                        else:
                            print(f"   ⚠️  No valid revision received, keeping current content")
                    
                except Exception as e:
                    print(f"   ⚠️  Revision failed: {e}, continuing with current content")
        
        # Return last critique with final content
        print(f"   ⚠️  Max iterations reached")
        return {
            **critique,
            "revised_content": current_content,
        }


def create_critique_crew(
    api_key: Optional[str] = None,
    model: str = "gpt-4o",
) -> CritiqueCrew:
    """Factory function to create a critique crew."""
    return CritiqueCrew(api_key=api_key, model=model)
