"""
Bring your own data to an OpenAI LLM using Azure Cognitive Search with vector search
and semantic ranking.
"""
from chatbot_1 import Chatbot
from dotenv import load_dotenv


def main():
    load_dotenv()

    chatbot = Chatbot()
    chatbot.ask("I need a large backpack. Which one do you recommend?")
    chatbot.ask("How much does it cost?")
    chatbot.ask("And how much for a donut?")


if __name__ == "__main__":
    main()
