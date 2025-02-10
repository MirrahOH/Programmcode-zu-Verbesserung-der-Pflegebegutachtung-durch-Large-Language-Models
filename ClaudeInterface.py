import anthropic
from dotenv import load_dotenv
import os

"""
    Klasse welche Schnittpunkt zur Anthropic API bereitstellt.
"""

class ClaudeInterface:
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the Anthropic client with an API key and model name.

        :param model: The Anthropic model to use.
        """
        load_dotenv()
        client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )
        self.client = client
        self.model = model
        self.chat_ids = []
        self.chat_sessions = {}
        self.systemPrompt = ""

    def start_chat(self, chat_id: int, system_message: str = "You are a helpful assistant."):
        """
        Start a new chat session with a unique ID.

        :param chat_id: Unique identifier for the chat session.
        :param system_message: Initial system message to set the chat's behavior.
        """
        if chat_id in self.chat_sessions:
            print(f"Chat session {chat_id} already exists.")
        else:
            self.systemPrompt = system_message
            self.chat_sessions[chat_id] = []
            print(f"Chat session {chat_id} started.")

    def send_message(self, chat_id: int, user_message: str):
        """
        Send a user message in the context of a specific chat session.

        :param chat_id: Chat session ID.
        :param user_message: The user's input message.
        :return: The assistant's response.
        """
        if chat_id not in self.chat_sessions:
            print(f"No chat session found with ID: {chat_id}. Please start a chat first.")
            return None

        self.chat_sessions[chat_id].append({"role": "user", "content": user_message})

        try:
            # Send the conversation history to the API
            response = self.client.messages.create(
                model=self.model,
                system=self.systemPrompt,
                max_tokens=1024,
                messages=self.chat_sessions[chat_id]
            )

            # Extract the assistant's reply
            assistant_message = response.content[0].text

            # Add the assistant's message to the conversation history
            self.chat_sessions[chat_id].append({"role": "assistant", "content": assistant_message})

            return assistant_message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def generate_chat_log(self, chat_id):
        """
        Generatea concatenated chat log string for a specific chat session.

        :param chat_id: The ID of the chat session.
        :return: A single string representing the formatted chat log.
        """
        # Retrieve the chat history for the given chat_id
        chat_history = self.chat_sessions.get(chat_id, None)

        if not chat_history:
            return f"No chat history available for chat ID: {chat_id}."

        log = []
        for message in chat_history:
            role = message.get('role', 'Unknown').capitalize()
            content = message.get('content', '')
            log.append(f"{role}: {content}")

        return "\n\n".join(log)