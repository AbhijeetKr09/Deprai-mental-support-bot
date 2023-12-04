import json
import os
class FileManager:
   
    '''
    This class essentially provides a way to manage the storage and retrieval of conversation data, making it easier to maintain and analyze the data. It uses the built-in json module to handle the data in JSON format, and the os module to manage directories and files. The if __name__ == "__main__" block at the end is used to test the class methods.
    '''

    def __init__(self, username):
        self.username = username
        self.history_file = "history.json"
        self.user_data = "user_data.json"
        self.complete_history = "complete_history.json"

    def store_data(self, response_text, user_prompt, max_history=5):
        if not os.path.exists("history"):
            os.makedirs("history")
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

    def training_data(self, response_text, user_prompt):
        if not os.path.exists("dataset"):
            os.makedirs("dataset")

        try:
            with open(f"dataset/{self.user_data}", 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        message = {'text': user_prompt, 'response': response_text}
        data.append(message)

        with open(f"dataset/{self.user_data}", 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    file = FileManager("sysblaze")
    result = file.store_data("anything", "nothing")
    result = file.load_conversation_history()
    print(result)