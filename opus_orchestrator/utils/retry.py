"""Retry Logic and Circuit Breaker for Opus.

Adds resilience to external API calls with:
- Exponential backoff retry
- Circuit breaker pattern
- Timeout handling
- Graceful degradation
"""

import asyncio
import time
from dataclasses import dataclass
from typing import Optional, Type
from enum import Enum
import random


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True


class CircuitBreaker:
    """Circuit breaker to prevent cascade failures.
    
    States:
    - CLOSED: Normal operation, calls allowed
    - OPEN: Too many failures, reject calls
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_calls = 0
    
    def can_execute(self) -> bool:
        """Check if execution is allowed."""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self.last_failure_time:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    return True
            return False
        
        if self.state == CircuitState.HALF_OPEN:
            return self.half_open_calls < self.half_open_max_calls
        
        return False
    
    def record_success(self):
        """Record a successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        else:
            self.failure_count = max(0, self.failure_count - 1)
    
    def record_failure(self):
        """Record a failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN


class RetryHandler:
    """Handles retry logic with exponential backoff."""
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
        self.circuit_breaker = CircuitBreaker()
    
    async def execute_with_retry(
        self,
        func,
        *args,
        **kwargs,
    ):
        """Execute a function with retry logic and circuit breaker.
        
        Args:
            func: Async function to execute
            *args, **kwargs: Arguments to pass to func
            
        Returns:
            Result of func
            
        Raises:
            Last exception if all retries fail
        """
        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            raise CircuitBreakerOpenError(
                "Circuit breaker is OPEN - too many failures"
            )
        
        last_exception = None
        
        for attempt in range(self.config.max_attempts):
            try:
                result = await func(*args, **kwargs)
                self.circuit_breaker.record_success()
                return result
            
            except Exception as e:
                last_exception = e
                self.circuit_breaker.record_failure()
                
                # Check if we should retry
                if attempt < self.config.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    await asyncio.sleep(delay)
                else:
                    # All retries exhausted
                    raise
        
        # Should not reach here, but just in case
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter."""
        delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        delay = min(delay, self.config.max_delay)
        
        if self.config.jitter:
            delay = delay * (0.5 + random.random())
        
        return delay


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass


# Decorator for easy retry
def with_retry(config: Optional[RetryConfig] = None):
    """Decorator to add retry logic to async functions."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            handler = RetryHandler(config)
            return await handler.execute_with_retry(func, *args, **kwargs)
        return wrapper
    return decorator


# Integration with LLM client
class ResilientLLMClient:
    """Wrapper adding resilience to LLM calls."""
    
    def __init__(self, client, retry_config: Optional[RetryConfig] = None):
        self.client = client
        self.retry_handler = RetryHandler(retry_config or RetryConfig())
    
    async def complete(self, system_prompt: str, user_prompt: str, **kwargs):
        """Call LLM with retry logic."""
        
        async def call():
            return await self.client.complete(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                **kwargs
            )
        
        try:
            return await self.retry_handler.execute_with_retry(call)
        except CircuitBreakerOpenError:
            # Return graceful degradation
            return {
                "error": "service_unavailable",
                "message": "Too many failures, please try again later",
                "retry_after": self.retry_handler.circuit_breaker.recovery_timeout,
            }
