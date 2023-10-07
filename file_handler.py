import json
class FileManager:
    def __init__(self, username):
        self.username = username
        self.history_file = "history.json"
        self.complete_history = "complete_history.json"

    def store_data(self, response_text, user_prompt, max_history=5):
        try:
            with open(f"history/{self.history_file}", 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if self.username not in data:
            data[self.username] = []

        conversation_history_list = list(data[self.username])

        message = {'text': user_prompt, 'response': response_text}
        conversation_history_list.append(message)

        conversation_history_list = conversation_history_list[-max_history:]

        data[self.username] = conversation_history_list

        with open(f"history/{self.history_file}", 'w') as f:
            json.dump(data, f, indent=4)

    def load_conversation_history(self):
        try:
            with open(f"history/{self.history_file}", 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        conversation_history = list(data.get(self.username, []))

        return conversation_history
    
    def store_complete_data(self, response_text, user_prompt):
        try:
            with open(f"history/{self.history_file}", 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if self.username not in data:
            data[self.username] = []

        conversation_history_list = list(data[self.username])

        message = {'text': user_prompt, 'response': response_text}
        conversation_history_list.append(message)

        data[self.username] = conversation_history_list

        with open(f"history/{self.history_file}", 'w') as f:
            json.dump(data, f, indent=4)