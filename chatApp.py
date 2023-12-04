from response import ResponseGenerator
from file_handler import FileManager
from conversation_analyser import ConversationAnalyzer as Conv_analyzer 
class ChatApp:

    '''
    __init__(self, username: str): Initializes the ChatApp class. Sets up the ResponseGenerator, FileManager, and ConversationAnalyzer for the given username.

    get_response(self, user_prompt: str) -> str: Generates a response for the given user_prompt. It loads the conversation history, analyzes the conversation, creates a prompt if necessary, generates a response, stores the response and user prompt, and returns the response.
    '''

    def __init__(self, username):
        self.username = username 
        self.response = ResponseGenerator() 
        self.fileHandler = FileManager(username)
        self.analysis = Conv_analyzer()

    def get_response(self, user_prompt):
        conversation_history = self.fileHandler.load_conversation_history()
        response_generator = self.response
        self.analysis.analyze_conversation(self.username, conversation_history)
        prompt = user_prompt if len(user_prompt) < 5 else response_generator.create_prompt(user_prompt)
        response = response_generator.get_response(prompt, conversation_history)
        self.fileHandler.store_data(response, user_prompt)
        self.fileHandler.training_data(response, user_prompt)
        return response

