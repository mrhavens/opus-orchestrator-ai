"""LLM client for Opus Orchestrator.

Supports MiniMax and OpenAI providers.
"""

import os
from typing import Any, Optional

import httpx


class LLMClient:
    """Simple LLM client for making API calls."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "minimax",
        model: str = "MiniMax/MiniMax-M2.1",
        base_url: Optional[str] = None,
    ):
        """Initialize LLM client."""
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.provider = provider
        self.model = model
        
        # Normalize model name for MiniMax
        if provider == "minimax":
            # MiniMax uses model names like "abab6.5s-chat" or "MiniMax-M2.1"
            self.minimax_model = model.split("/")[-1] if "/" in model else model
        
        # Set base URL based on provider
        if base_url:
            self.base_url = base_url
        elif provider == "minimax":
            self.base_url = "https://api.minimax.chat/v1"
        elif provider == "openai":
            self.base_url = "https://api.openai.com/v1"
        else:
            self.base_url = "https://api.openai.com/v1"
        
        self.client = httpx.AsyncClient(timeout=120.0)

    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Make a completion request."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if self.provider == "minimax":
            return await self._complete_minimax(
                system_prompt, user_prompt, temperature, max_tokens, headers
            )
        elif self.provider == "openai":
            return await self._complete_openai(
                system_prompt, user_prompt, temperature, max_tokens, headers
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def _complete_minimax(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: Optional[int],
        headers: dict,
    ) -> str:
        """Call MiniMax API."""
        # MiniMax chat completion format
        payload = {
            "model": self.minimax_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        response = await self.client.post(
            f"{self.base_url}/text/chatcompletion_v2",
            headers=headers,
            json=payload,
        )
        
        # Debug output
        if response.status_code != 200:
            print(f"MiniMax API error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            response.raise_for_status()
        
        data = response.json()
        
        # Handle different response formats
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "choices" in data.get("data", {}):
            return data["data"]["choices"][0]["message"]["content"]
        else:
            # Try to find content in response
            raise Exception(f"Unexpected MiniMax response: {data}")

    async def _complete_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: Optional[int],
        headers: dict,
    ) -> str:
        """Call OpenAI API."""
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
        
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


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
