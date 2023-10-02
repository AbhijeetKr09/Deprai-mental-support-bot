import openai
from dotenv import load_dotenv
import os
import spacy
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from conversation_analyser import ConversationAnalyzer as Conv_a
import json

class ResponseGenerator:
    def __init__(self):
        load_dotenv("data.env")
        self.nlp = spacy.load("en_core_web_sm")
        openai.api_key = os.getenv('OPENAI_API')
        authenticator = IAMAuthenticator(os.getenv('NLU_API'))
        self.conversation = []
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=os.getenv('NLU_version'),
            authenticator=authenticator
        )

        self.natural_language_understanding.set_service_url(os.getenv('NLU_URL'))

    def get_response(self, username, user_prompt):
        conversation = self.load_conversation_history(str(username))
        doc = self.nlp(user_prompt)
        entities = [ent.text for ent in doc.ents]
        nlu_response = self.natural_language_understanding.analyze(
            text=user_prompt,
            features=Features(entities=EntitiesOptions(), sentiment=SentimentOptions())
        ).get_result()

        sentiment = nlu_response['sentiment']['document']['label']
        if not nlu_response['entities']:
            intent = 'Unknown'
        else:
            intent = nlu_response['entities'][0]['type']
        user_prompt = f" last conversation History: {conversation}. \n The user is feeling {sentiment} and their intent is {intent} and entities in text: {entities}. Provide a response that addresses their needs. \n prompt from user: {user_prompt}."
        
        print(user_prompt)
        self.conversation.append(user_prompt)
        print(self.conversation)
        # Conv_a.analyze_conversation(username, self.conversation)
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=1.0,
            top_p=0.9
        )

        response_text = response.choices[0].text.strip()
        self.store_data(str(username), user_prompt, response_text)
        return response_text, sentiment, intent
    
    def store_data(self, username, user_text, response_text, filename='history.json', max_history=5):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if username not in data:
            data[username] = []

        conversation_history_list = list(data[username])

        message = {'text': user_text, 'response': response_text}
        conversation_history_list.append(message)

        conversation_history_list = conversation_history_list[-max_history:]

        data[username] = conversation_history_list

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_conversation_history(self, username, filename='history.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        conversation_history = list(data.get(username, []))

        return conversation_history

if __name__ == "__main__":
    generator = ResponseGenerator()
    print(generator.get_response('username', 'any random quote'))
