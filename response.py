import openai
from dotenv import load_dotenv
import os
import spacy
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from conversation_analyser import ConversationAnalyzer as Conv_a


class ResponseGenerator:
    def __init__(self):
        load_dotenv("data.env")
        self.nlp = spacy.load("en_core_web_sm")
        openai.api_key = os.getenv('OPENAI_API')
        authenticator = IAMAuthenticator(os.getenv('NLU_API'))
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=os.getenv('NLU_version'),
            authenticator=authenticator
        )

        self.natural_language_understanding.set_service_url(os.getenv('NLU_URL'))

    def create_prompt(self, query):

        doc = self.nlp(query)

        entities = [ent.text for ent in doc.ents]

        nlu_response = self.natural_language_understanding.analyze(
            text = query,
            features=Features(entities=EntitiesOptions(), sentiment=SentimentOptions())
        ).get_result()

        sentiment = nlu_response['sentiment']['document']['label']

        if not nlu_response['entities']:
            intent = 'Unknown'
        else:
            intent = nlu_response['entities'][0]['type']

        user_prompt = f"The user is feeling {sentiment} and their intent is {intent} and entities in text: {entities}. Provide a response that addresses their needs. \n this is user text: {query}."
        print(user_prompt)
        return user_prompt

    def get_response(self, user_prompt, conversation_history, model="text-davinci-002"):

        if not conversation_history:
            str_conversation_history = ''
        else:
            str_conversation_history = "\n".join(
                f"{message['text']}\n{message['response']}" for message in conversation_history
            )
        
        user_prompt = f"last conversation History:{str_conversation_history} \n New prompt from user: {user_prompt}"
        
        response = openai.Completion.create(
            engine=model,
            prompt=user_prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=1.0,
            top_p=0.9
        )
        return response['choices'][0]['text']

    
    

if __name__ == "__main__":
    generator = ResponseGenerator()

