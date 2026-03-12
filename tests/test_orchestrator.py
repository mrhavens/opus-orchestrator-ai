"""Tests for Opus Orchestrator."""

import pytest
from opus_orchestrator import OpusOrchestrator, BookType, BookIntent
from opus_orchestrator.schemas import RawContent, Chapter, Manuscript


@pytest.fixture
def basic_intent():
    return BookIntent(
        book_type=BookType.FICTION,
        genre="science-fiction",
        target_audience="adult sci-fi readers",
        intended_outcome="complete novel ~80k words",
        tone="epic",
        target_word_count=80000,
    )


@pytest.fixture
def basic_content():
    return RawContent(
        content_type="outline",
        text="A space explorer discovers a new civilization...",
    )


class TestOpusOrchestrator:
    """Test suite for OpusOrchestrator."""

    def test_init_fiction(self, basic_intent):
        """Test initialization with fiction."""
        orch = OpusOrchestrator(
            book_type="fiction",
            genre="science-fiction",
            target_audience="adult sci-fi readers",
            intended_outcome="complete novel",
        )

        assert orch.book_type == BookType.FICTION
        assert "architect" in orch.agents
        assert "voice" in orch.agents

    def test_init_nonfiction(self):
        """Test initialization with nonfiction."""
        orch = OpusOrchestrator(
            book_type="nonfiction",
            genre="business",
            target_audience="professionals",
            intended_outcome="complete business book",
        )

        assert orch.book_type == BookType.NONFICTION
        assert "researcher" in orch.agents
        assert "analyst" in orch.agents

    @pytest.mark.asyncio
    async def test_ingest(self, basic_content):
        """Test content ingestion."""
        orch = OpusOrchestrator(
            book_type="fiction",
            genre="fantasy",
            target_audience="general",
            intended_outcome="novel",
        )

        state = await orch.ingest(basic_content)

        assert state.raw_content == basic_content
        assert state.current_stage == "ingestion"

    @pytest.mark.asyncio
    async def test_generate_blueprint(self, basic_content):
        """Test blueprint generation."""
        orch = OpusOrchestrator(
            book_type="fiction",
            genre="mystery",
            target_audience="general",
            intended_outcome="novel",
        )

        await orch.ingest(basic_content)
        blueprint = await orch.generate_blueprint()

        assert blueprint.title == "Untitled"
        assert blueprint.target_word_count == 80000


class TestSchemas:
    """Test schema validation."""

    def test_book_intent_fiction(self):
        """Test BookIntent for fiction."""
        intent = BookIntent(
            book_type=BookType.FICTION,
            genre="thriller",
            target_audience="adult thriller readers",
            intended_outcome="complete thriller novel",
            target_word_count=90000,
        )

        assert intent.book_type == BookType.FICTION
        assert intent.target_word_count == 90000

    def test_manuscript_to_markdown(self):
        """Test manuscript markdown conversion."""
        manuscript = Manuscript(
            title="Test Book",
            subtitle="A Test",
            book_type=BookType.FICTION,
            genre="fantasy",
            chapters=[
                Chapter(chapter_number=1, title="The Beginning", content="Content 1", word_count=1000),
                Chapter(chapter_number=2, title="The Middle", content="Content 2", word_count=1500),
            ],
            total_word_count=2500,
            frontmatter={"include_toc": True, "dedication": "To test"},
        )

        md = manuscript.to_markdown()

        assert "# Test Book" in md
        assert "## A Test" in md
        assert "## Table of Contents" in md
        assert "Chapter 1: The Beginning" in md
        assert "Chapter 2: The Middle" in md
        assert "*To test*" in md
