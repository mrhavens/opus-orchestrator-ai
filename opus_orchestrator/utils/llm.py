"""LLM client for Opus Orchestrator.

Supports MiniMax and OpenAI providers - both async and sync.
Includes retry logic with exponential backoff and circuit breaker.
"""

import os
import asyncio
from typing import Any, Optional

import httpx
import requests

from opus_orchestrator.utils.retry import RetryHandler, RetryConfig


class LLMClient:
    """Simple LLM client for making API calls - supports both sync and async.
    
    Includes built-in retry logic with circuit breaker for resilience.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "minimax",
        model: str = "MiniMax/MiniMax-M2.1",
        base_url: Optional[str] = None,
        max_retries: int = 3,
    ):
        """Initialize LLM client.
        
        Args:
            api_key: API key for the provider
            provider: LLM provider (minimax, openai)
            model: Model name
            base_url: Optional custom base URL
            max_retries: Maximum retry attempts (default 3)
        """
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.provider = provider
        self.model = model
        
        # Normalize model name for MiniMax
        if provider == "minimax":
            self.minimax_model = model.split("/")[-1] if "/" in model else model
        
        # Set base URL based on provider
        if base_url:
            self.base_url = base_url
        elif provider == "minimax":
            # Use Anthropic-compatible API (like OpenClaw uses)
            self.base_url = "https://api.minimax.io/anthropic"
        elif provider == "openai":
            self.base_url = "https://api.openai.com/v1"
        else:
            self.base_url = "https://api.openai.com/v1"
        
        # Async client
        self._async_client = httpx.AsyncClient(timeout=120.0)
        
        # Initialize retry handler
        retry_config = RetryConfig(
            max_attempts=max_retries,
            base_delay=1.0,
            max_delay=30.0,
            exponential_base=2.0,
            jitter=True,
        )
        self._retry_handler = RetryHandler(retry_config)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Make a completion request (SYNC - for LangGraph compatibility)."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if self.provider == "minimax":
            return self._complete_minimax_sync(
                system_prompt, user_prompt, temperature, max_tokens, headers
            )
        elif self.provider == "openai":
            return self._complete_openai_sync(
                system_prompt, user_prompt, temperature, max_tokens, headers
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def complete_async(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Make a completion request (ASYNC) with retry logic."""
        
        async def _make_request():
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            if self.provider == "minimax":
                return await self._complete_minimax_async(
                    system_prompt, user_prompt, temperature, max_tokens, headers
                )
            elif self.provider == "openai":
                return await self._complete_openai_async(
                    system_prompt, user_prompt, temperature, max_tokens, headers
                )
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        
        # Use retry handler for resilience
        try:
            return await self._retry_handler.execute_with_retry(_make_request)
        except Exception as e:
            # Log and re-raise with context
            raise RuntimeError(f"LLM request failed after retries: {e}") from e

    async def _complete_minimax_async(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: Optional[int],
        headers: dict,
    ) -> str:
        """Call MiniMax API using Anthropic-compatible endpoint."""
        # Anthropic-compatible format
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
        
        # Use Anthropic-compatible endpoint
        response = await self._async_client.post(
            f"{self.base_url}/v1/messages",
            headers={**headers, "Content-Type": "application/json"},
            json=payload,
        )
        
        # Debug output
        if response.status_code != 200:
            print(f"MiniMax API error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            response.raise_for_status()
        
        data = response.json()
        
        # Handle Anthropic-compatible response format
        if "content" in data:
            # Return the text content
            if isinstance(data["content"], list) and len(data["content"]) > 0:
                return data["content"][0].get("text", str(data["content"][0]))
            return str(data["content"])
        else:
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
        
        response = await self._async_client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def close(self):
        """Close the HTTP client."""
        await self._async_client.aclose()

    # =========================================================================
    # SYNC VERSIONS (for LangGraph compatibility)
    # =========================================================================

    def _complete_minimax_sync(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: Optional[int],
        headers: dict,
    ) -> str:
        """Call MiniMax API (sync) using Anthropic-compatible endpoint."""
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
        
        # Use Anthropic-compatible endpoint
        response = requests.post(
            f"{self.base_url}/v1/messages",
            headers={**headers, "Content-Type": "application/json"},
            json=payload,
            timeout=120,
        )
        
        if response.status_code != 200:
            print(f"MiniMax API error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            response.raise_for_status()
        
        data = response.json()
        
        # Handle Anthropic-compatible response format
        if "content" in data:
            if isinstance(data["content"], list) and len(data["content"]) > 0:
                # Look for text content, skip thinking
                text_parts = []
                for item in data["content"]:
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                if text_parts:
                    return "".join(text_parts)
                # If no text found, return first item as string
                return str(data["content"][0])
            return str(data["content"])
        else:
            raise Exception(f"Unexpected MiniMax response: {data}")

    def _complete_openai_sync(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: Optional[int],
        headers: dict,
    ) -> str:
        """Call OpenAI API (sync)."""
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
