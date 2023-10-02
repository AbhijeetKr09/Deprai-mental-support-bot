from nltk.sentiment import SentimentIntensityAnalyzer
import os
from datetime import datetime
import re

class ConversationAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze_conversation(self, username, conversation_data):
        self.sentiment_scores = [self.sia.polarity_scores(message['text'])['compound'] for message in conversation_data]
        average_sentiment_score = sum(self.sentiment_scores) / len(self.sentiment_scores) if self.sentiment_scores else 0

        sentiment_label = self.get_sentiment_label(average_sentiment_score)
        report = self.generate_report(average_sentiment_score, sentiment_label)
        self.save_report(username, report, average_sentiment_score)

        return report

    def get_sentiment_label(self, sentiment_score):
        if sentiment_score > 0.05:
            return "positive"
        elif sentiment_score < -0.05:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def generate_report(average_sentiment_score, sentiment_label):
        if sentiment_label == "positive":
            report = f"Your recent conversations show a positive sentiment."
        elif sentiment_label == "negative":
            report = f"Your recent conversations show a negative sentiment."
        else:
            report = f"Your recent conversations show a neutral sentiment."

        report += f"\nAverage Sentiment Score: {average_sentiment_score:.2f}"
        return report

    @staticmethod
    def save_report(username, report, sentiment_score):
        if not os.path.exists('reports'):
            os.makedirs('reports')

        report_filename = f'reports/{username}.txt'

        with open(report_filename, 'a') as file:
            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d %H:%M:%S")
            report_with_score = f"\n\nReport generated on {date_string}:\n{report}\nAverage Sentiment Score: {sentiment_score:.2f}"
            file.write(report_with_score)
