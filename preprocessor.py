import nltk
import os
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet # I want to use it, it can increase deprai's efficiency


class EmotionFilter:

    '''
    This class essentially provides a way to analyze the emotional content of a text by filtering out words that are likely to convey emotion. It uses the NLTK library to tokenize the text and assign part-of-speech tags to the tokens. The if __name__ == "__main__" block at the end is used to test the class methods.
    '''

    def __init__(self):
        self.emotion_keywords = ["JJ", "JJR", "JJS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

    def filter_emotions(self, user_text):
        tokens = word_tokenize(user_text)
        pos_tags = nltk.pos_tag(tokens)
        filtered_words = [word for word, tag in pos_tags if tag in self.emotion_keywords]
        return filtered_words

    def save_to_json(self, user_text, filtered_content, filename="dataset.json"):
        if not os.path.exists("dataset"):
            os.makedirs("dataset")
        try:
            with open(f"dataset/{filename}", 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append({'input': user_text, 'output': filtered_content})

        with open(f"dataset/{filename}", 'w') as f:
            json.dump(data, f, indent=4)



if __name__ == "__main__":
    user_text = " this is user text:"
    filter_obj = EmotionFilter()
    filtered_content = filter_obj.filter_emotions(user_text)
    filter_obj.save_to_json(user_text, filtered_content)
