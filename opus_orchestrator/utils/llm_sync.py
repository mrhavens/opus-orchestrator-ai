"""LLM client for Opus Orchestrator - Synchronous version.

Uses synchronous httpx to avoid event loop issues with LangGraph.
"""

import os
from typing import Any, Optional

import requests


class LLMClient:
    """Synchronous LLM client for making API calls."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "openai",
        model: str = "gpt-4o",
        base_url: Optional[str] = None,
    ):
        """Initialize LLM client."""
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.provider = provider
        self.model = model
        
        if base_url:
            self.base_url = base_url
        elif provider == "minimax":
            self.base_url = "https://api.minimax.chat/v1"
        elif provider == "openai":
            self.base_url = "https://api.openai.com/v1"
        else:
            self.base_url = "https://api.openai.com/v1"

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Make a completion request (synchronous)."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if self.provider == "minimax":
            return self._complete_minimax(
                system_prompt, user_prompt, temperature, max_tokens, headers
            )
        elif self.provider == "openai":
            return self._complete_openai(
                system_prompt, user_prompt, temperature, max_tokens, headers
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _complete_minimax(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: Optional[int],
        headers: dict,
    ) -> str:
        """Call MiniMax API (synchronous)."""
        minimax_model = self.model.split("/")[-1] if "/" in self.model else self.model
        
        payload = {
            "model": minimax_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        response = requests.post(
            f"{self.base_url}/text/chatcompletion_v2",
            headers=headers,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        
        data = response.json()
        
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Unexpected MiniMax response: {data}")

    def _complete_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: Optional[int],
        headers: dict,
    ) -> str:
        """Call OpenAI API (synchronous)."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]


# Convenience function
def get_llm_client(config: Optional[Any] = None) -> LLMClient:
    """Get an LLM client from config."""
    from opus_orchestrator.config import get_config
    
    cfg = config or get_config()
    
    return LLMClient(
        api_key=cfg.agent.api_key,
        provider=cfg.agent.provider,
        model=cfg.agent.model,
    )
