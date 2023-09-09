"""
Chatbot with context and memory.
"""
import os

import openai

# Config for Azure OpenAI.
OPENAI_API_TYPE = "azure"
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = "2023-03-15-preview"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CHATGPT_DEPLOYMENT = "chatgpt-deployment"

# Chat roles
SYSTEM = "system"
USER = "user"
ASSISTANT = "assistant"


class Chatbot:
    """Chat with an LLM. Keeps chat history in memory."""

    chat_history = None

    def __init__(self):
        openai.api_type = OPENAI_API_TYPE
        openai.api_base = OPENAI_API_BASE
        openai.api_version = OPENAI_API_VERSION
        openai.api_key = OPENAI_API_KEY

        system_message = (
            "You're an assistant helping users learn about GPT models.\n"
            "Please answer the user's question using only information you can find in "
            "the chat history and context, which are enclosed by back ticks in the "
            "user prompt.\n"
            "If the user's question is unrelated to GPT models, say you don't know.\n"
        )

        self.chat_history = [{"role": SYSTEM, "content": system_message}]

    def ask(self, context_list: list[str], question: str) -> str:
        """
        Queries the LLM including relevant context from our own data.
        """
        context = "\n\n".join(context_list)
        user_message = (
            f"Here's the context: ```{context}```\n "
            f"Here's my question: ```{question}```\n"
        )
        self.chat_history.append({"role": USER, "content": user_message})

        chat_completion = openai.ChatCompletion.create(
            deployment_id=OPENAI_CHATGPT_DEPLOYMENT,
            messages=self.chat_history,
            temperature=0.7,
            max_tokens=1024,
            n=1,
        )
        response = chat_completion.choices[0].message.content
        # No need to keep the context for every question in the history.
        self.chat_history[-1] = {
            "role": USER,
            "content": f"Here's my question: ```{question}```\n",
        }
        self.chat_history.append({"role": ASSISTANT, "content": response})

        return response
