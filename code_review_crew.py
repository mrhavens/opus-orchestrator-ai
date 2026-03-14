"""Code Review CrewAI Agents.

Five hyperfocused expert agents that rigorously review the Opus codebase.
Each agent specializes in a specific domain and finds bugs/issues.
"""

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


# =============================================================================
# AGENT 1: SECURITY EXPERT
# =============================================================================

security_expert = Agent(
    name="SecurityExpert",
    role="Security & Vulnerability Researcher",
    goal="Find security vulnerabilities, auth issues, data exposure, and unsafe practices",
    backstory="""You are a security researcher with 15 years of experience in application security.
You specialize in OWASP Top 10, API security, authentication, authorization, and data protection.
You find vulnerabilities that others miss and provide actionable remediation.
Your reviews are thorough and your recommendations are precise."""
)

security_task = Task(
    description="""Conduct a comprehensive SECURITY audit of the Opus Orchestrator codebase.

Focus on:
1. Authentication/Authorization - Any security gaps?
2. Data Exposure - Sensitive data in logs, errors, responses?
3. Injection Risks - SQL, command, code injection?
4. API Security - Rate limiting, input validation?
5. Dependency Vulnerabilities - Known CVEs in requirements?
6. Secrets Management - API keys, tokens properly handled?
7. File Access - Path traversal, file inclusion risks?
8. Input Validation - All user inputs sanitized?

Files to review:
- opus_orchestrator/utils/llm.py
- opus_orchestrator/server.py
- opus_orchestrator/cli.py
- opus_orchestrator/utils/*.py
- Any authentication/authorization code

For each issue found, provide:
- File and line number
- Severity (Critical/High/Medium/Low)
- Description
- Impact
- Remediation""",
    agent=security_expert,
    expected_output="Security audit report with findings, severity, and remediation"
)


# =============================================================================
# AGENT 2: PERFORMANCE EXPERT
# =============================================================================

performance_expert = Agent(
    name="PerformanceExpert",
    role="Performance & Scalability Architect",
    goal="Find performance bottlenecks, memory issues, inefficient algorithms, and scaling problems",
    backstory="""You are a performance architect with experience optimizing large-scale systems.
You specialize in profiling, caching strategies, database queries, async patterns, and scalability.
You find the bottlenecks that cause systems to slow down under load.
Your analysis includes both immediate issues and architectural concerns."""
)

performance_task = Task(
    description="""Conduct a comprehensive PERFORMANCE audit of the Opus Orchestrator codebase.

Focus on:
1. Async/Await Issues - Blocking calls, missing awaits, thread pool exhaustion?
2. Memory Leaks - Unclosed resources, growing collections?
3. Database/API Calls - N+1 queries, redundant calls, missing batching?
4. Caching Opportunities - Repeated computations that could be cached?
5. Large Data Handling - Streaming vs loading into memory?
6. Concurrency Issues - Race conditions, deadlocks?
7. Algorithmic Complexity - O(n²) where O(n) possible?
8. Resource Cleanup - Connections, files, threads properly closed?

Files to review:
- opus_orchestrator/langgraph_workflow.py
- opus_orchestrator/orchestrator.py
- opus_orchestrator/agents/*.py
- opus_orchestrator/utils/*.py

For each issue:
- File and line number
- Severity (Critical/High/Medium/Low)
- Description
- Performance Impact
- Optimization Suggestion""",
    agent=performance_expert,
    expected_output="Performance audit report with findings and optimizations"
)


# =============================================================================
# AGENT 3: ARCHITECTURE EXPERT
# =============================================================================

architecture_expert = Agent(
    name="ArchitectureExpert",
    role="Software Architect & Design Patterns Specialist",
    goal="Find architectural weaknesses, design pattern violations, and structural issues",
    backstory="""You are a software architect with expertise in clean code, SOLID principles, and design patterns.
You specialize in identifying tight coupling, god objects, missing abstractions, and architectural smells.
Your reviews improve code maintainability and long-term viability."""
)

architecture_task = Task(
    description="""Conduct a comprehensive ARCHITECTURE audit of the Opus Orchestrator codebase.

Focus on:
1. SOLID Violations - Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion?
2. Design Patterns - Missing patterns, anti-patterns, over-engineering?
3. Coupling - Tight coupling, hidden dependencies, circular imports?
4. Abstraction - Missing abstractions, leaky abstractions?
5. God Objects - Classes doing too much?
6. Feature Envy - Classes more interested in other classes' data?
7. Shotgun Surgery - Changes require many small changes?
8. Parallel Inheritance - Two class hierarchies that mirror each other?
9. Lazy Classes - Classes doing almost nothing?
10. Speculative Generality - Code for "future" features that don't exist?

Files to review:
- opus_orchestrator/orchestrator.py
- opus_orchestrator/langgraph_workflow.py
- opus_orchestrator/cli.py
- opus_orchestrator/agents/base.py
- opus_orchestrator/nonfiction/*.py

For each issue:
- File and location
- Principle/violation
- Description
- Refactoring Suggestion""",
    agent=architecture_expert,
    expected_output="Architecture audit with violations and refactoring suggestions"
)


# =============================================================================
# AGENT 4: TESTING EXPERT
# =============================================================================

testing_expert = Agent(
    name="TestingExpert",
    role="Test Automation & QA Specialist",
    goal="Find missing tests, coverage gaps, and quality issues in test suite",
    backstory="""You are a QA specialist with expertise in test strategy, coverage analysis, and test automation.
You specialize in identifying what isn't tested, what should be tested, and test quality issues.
Your recommendations improve confidence in code correctness."""
)

testing_task = Task(
    description="""Conduct a comprehensive TESTING audit of the Opus Orchestrator codebase.

Focus on:
1. Test Coverage - What's NOT tested? Coverage gaps?
2. Edge Cases - What boundary conditions are untested?
3. Error Paths - Are exceptions properly tested?
4. Integration Tests - Do components work together?
5. Mock Usage - Are mocks overused (hiding bugs)?
6. Test Quality - Flaky tests, assertions, setup/teardown?
7. Test Data - Realistic vs mocked data?
8. Happy Path Bias - Only success cases tested?
9. Regression Coverage - Can we detect breaking changes?
10. Performance Tests - Any load/stress testing?

Files to review:
- tests/*.py
- Any test-related files

Also review:
- Are critical paths in orchestrator tested?
- Are the agents tested?
- Is the CLI tested?
- Are the frameworks tested?

For each gap:
- What should be tested
- Why it's important
- Suggested test approach""",
    agent=testing_expert,
    expected_output="Testing audit with coverage gaps and test recommendations"
)


# =============================================================================
# AGENT 5: ERROR HANDLING EXPERT
# =============================================================================

error_expert = Agent(
    name="ErrorHandlingExpert",
    role="Exception Handling & Reliability Specialist",
    goal="Find error handling anti-patterns, uncaught exceptions, and reliability issues",
    backstory="""You are a reliability specialist with expertise in exception handling and fault tolerance.
You specialize in finding swallowed exceptions, improper error messages, and reliability gaps.
Your reviews make systems more robust and debuggable."""
)

error_task = Task(
    description="""Conduct a comprehensive ERROR HANDLING audit of the Opus Orchestrator codebase.

Focus on:
1. Swallowed Exceptions - try/except with pass or empty except?
2. Bare Except - except: catching everything?
3. Error Messages - Generic vs specific, exposing internals?
4. Logging Issues - Sensitive data in logs? Missing context?
5. Retry Logic - Failed operations retried properly?
6. Circuit Breakers - External API failures handled?
7. Timeout Handling - Long-running operations have timeouts?
8. Graceful Degradation - What happens when components fail?
9. Error Recovery - Can the system recover from errors?
10. Debug Info - Enough info to diagnose issues?

Files to review:
- opus_orchestrator/orchestrator.py
- opus_orchestrator/langgraph_workflow.py
- opus_orchestrator/agents/*.py
- opus_orchestrator/utils/*.py
- opus_orchestrator/server.py

For each issue:
- File and location
- Issue type
- Description
- Reliability Impact
- Better Approach""",
    agent=error_expert,
    expected_output="Error handling audit with reliability issues and fixes"
)


# =============================================================================
# RUN ALL AGENTS
# =============================================================================

def run_code_review() -> dict:
    """Run all 5 code review agents."""
    
    crews = [
        ("Security", security_expert, security_task),
        ("Performance", performance_expert, performance_task),
        ("Architecture", architecture_expert, architecture_task),
        ("Testing", testing_expert, testing_task),
        ("Error Handling", error_expert, error_task),
    ]
    
    results = {}
    
    for name, agent, task in crews:
        print(f"\n{'='*60}")
        print(f"Running {name} Expert Review...")
        print('='*60)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
        )
        
        try:
            result = crew.kickoff()
            results[name] = {
                "status": "success",
                "findings": result,
            }
        except Exception as e:
            results[name] = {
                "status": "error",
                "error": str(e),
            }
    
    return results


if __name__ == "__main__":
    results = run_code_review()
    
    print("\n" + "="*60)
    print("CODE REVIEW SUMMARY")
    print("="*60)
    
    for name, result in results.items():
        status = result["status"]
        emoji = "✅" if status == "success" else "❌"
        print(f"{emoji} {name}: {status}")
