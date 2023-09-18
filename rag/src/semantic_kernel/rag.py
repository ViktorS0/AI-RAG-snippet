"""
Bring your own data to an OpenAI LLM using Azure Cognitive Search with vector search.
Uses Semantic Kernel.
"""
import asyncio
import os

import semantic_kernel as sk
from chatbot import Chatbot
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from semantic_kernel.connectors.memory.azure_cognitive_search import (
    AzureCognitiveSearchMemoryStore,
)

# Config for Azure Search.
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = "blog-posts-index-3"

# Config for Azure OpenAI.
OPENAI_API_TYPE = "azure"
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = "2023-03-15-preview"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_DEPLOYMENT = "embedding-deployment"


def log(title: str, content: str) -> str:
    """
    Prints a title and content to the console.
    """
    print(f"*****\n{title.upper()}:\n{content}\n*****\n")


async def get_context(query: str) -> list[str]:
    """
    Gets the relevant documents from Azure Cognitive Search.
    """
    kernel = sk.Kernel()
    kernel.add_text_embedding_generation_service(
        "openai-embedding",
        OpenAITextEmbedding(
            model_id=OPENAI_EMBEDDING_DEPLOYMENT,
            api_key=OPENAI_API_KEY,
            endpoint=OPENAI_API_BASE,
            api_type=OPENAI_API_TYPE,
            api_version=OPENAI_API_VERSION,
        ),
    )
    kernel.register_memory_store(
        memory_store=AzureCognitiveSearchMemoryStore(
            vector_size=1536,
            search_endpoint=AZURE_SEARCH_ENDPOINT,
            admin_key=AZURE_SEARCH_KEY,
        )
    )

    docs = await kernel.memory.search_async(AZURE_SEARCH_INDEX_NAME, query, limit=1)
    context = [doc.text for doc in docs]

    return context


async def ask_question(chat: Chatbot, question: str):
    """
    Get the context for the user's question, and ask the Chatbot that question.
    """
    log("QUESTION", question)
    context_list = await get_context(question)
    response = await chat.ask(context_list, question)
    log("RESPONSE", response)


async def main():
    load_dotenv()

    chat = Chatbot()
    await ask_question(chat, "Explain in one or two sentences how attention works.")
    await ask_question(chat, "Is it used by the GPT Transformer?")
    await ask_question(chat, "Explain how whales communicate.")


if __name__ == "__main__":
    asyncio.run(main())
