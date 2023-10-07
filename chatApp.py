from response import ResponseGenerator
from file_handler import FileManager

class ChatApp:
    def __init__(self, username):
        self.username = username
        self.response = ResponseGenerator()
        self.fileHandler = FileManager(username)

    def get_response(self, user_prompt):
        conversation_history = self.fileHandler.load_conversation_history()
        response_generator = self.response
        prompt = user_prompt if len(user_prompt) < 5 else response_generator.create_prompt(user_prompt)
        response = response_generator.get_response(prompt, conversation_history)
        self.fileHandler.store_data(response, user_prompt)
        return response