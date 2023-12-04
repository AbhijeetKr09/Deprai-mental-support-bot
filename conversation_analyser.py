from nltk.sentiment import SentimentIntensityAnalyzer
import os
from datetime import datetime

class ConversationAnalyzer:

    '''
    __init__(self): This is the constructor method that initializes the SentimentIntensityAnalyzer from the NLTK library.

    analyze_conversation(self, username, conversation_data): This method calculates the sentiment scores for each message in the conversation data using the SentimentIntensityAnalyzer. It then calculates the average sentiment score and determines the sentiment label (positive, negative, or neutral). It generates a report based on these values and saves the report using the save_report method. It returns the generated report.

    get_sentiment_label(self, sentiment_score): This method determines the sentiment label based on the sentiment score. If the score is greater than 0.05, it returns “positive”. If it’s less than -0.05, it returns “negative”. Otherwise, it returns “neutral”.

    generate_report(average_sentiment_score, sentiment_label): This static method generates a report based on the average sentiment score and the sentiment label. It returns a string that describes the sentiment of the conversation.

    save_report(username, report, sentiment_score): This static method saves the generated report in a text file. The filename is based on the username and the files are stored in a directory named “reports”. If the directory does not exist, it creates one.

    '''

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    # calculate polarity score using sia. 
    def analyze_conversation(self, username, conversation_data):
        self.sentiment_scores = [self.sia.polarity_scores(message['text'])['compound'] for message in conversation_data]
        average_sentiment_score = sum(self.sentiment_scores) / len(self.sentiment_scores) if self.sentiment_scores else 0

        sentiment_label = self.get_sentiment_label(average_sentiment_score)
        report = self.generate_report(average_sentiment_score, sentiment_label)
        self.save_report(username, report, average_sentiment_score)

        return report

    def get_sentiment_label(self, sentiment_score):
        print(f"score: {sentiment_score} of user.")
        if sentiment_score > 0.05:
            return "positive"
        elif sentiment_score < -0.05:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def generate_report(average_sentiment_score, sentiment_label):
        print(f"Average sentiment score: {average_sentiment_score} \n Sentiment Label: {sentiment_label}")
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
