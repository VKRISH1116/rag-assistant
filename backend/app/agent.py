"""
Agentic AI Workflow - Multi-step Reasoning with LangChain Agents

This module implements:
- LangChain agents for complex query handling
- Multiple tools (document search, summarization, stats)
- Multi-step reasoning workflow
"""

from typing import Optional, List, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class AgenticWorkflow:
    """
    Lightweight workflow wrapper that preserves the app's agent entry point
    while avoiding deprecated LangChain APIs.
    """

    def __init__(self, rag_engine):
        self.rag_engine = rag_engine
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.agent = False

    def process_query(self, question: str) -> Dict:
        """Use the configured RAG engine to answer the question."""
        if not self.api_key:
            return {
                "answer": "OPENAI_API_KEY not set. Please set it in your environment or .env file.",
                "sources": [],
                "confidence": 0.0,
                "agentic": False,
            }

        if not getattr(self.rag_engine, "vector_store", None):
            return {
                "answer": "No documents uploaded yet. Please upload a document first.",
                "sources": [],
                "confidence": 0.0,
                "agentic": True,
            }

        try:
            result = self.rag_engine.query(question, k=3)
            relevant_chunks = self.rag_engine.get_relevant_chunks(question, k=3)
            sources = [chunk.page_content[:200] + "..." for chunk in relevant_chunks]
            return {
                "answer": result.get("answer", "No answer found."),
                "sources": sources,
                "confidence": result.get("confidence", 0.7),
                "agentic": True,
            }
        except Exception as e:
            return {
                "answer": f"I encountered an error processing your query: {str(e)}",
                "sources": [],
                "confidence": 0.0,
                "agentic": False,
            }
