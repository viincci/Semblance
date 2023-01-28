from flask import Flask, request
from flask_restful import Resource, Api
import json
import openai
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

# Load the custom intents from the json file
with open("intents.json", "r") as file:
    intents = json.load(file)

# Add your OpenAI API key
openai.api_key = "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"

# Define the function to generate responses
def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message


def all_lower(my_list):
    return list(map(lambda x: x.lower(), my_list))

# Define the chatbot function
def chatbot(question):
    # Check if the question matches any of the custom intents
    for intent in intents:
        lst = intent["questions"]
        if question.lower() in all_lower(lst):
            return intent["answer"]
    
    # Use GPT-2 to generate a response for other questions
    return generate_response(question)

# Start the chatbot in a while loop
app = Flask(__name__)
api = Api(app)

class Chatbot(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        question = json_data['question']
        answer = chatbot(question)
        return {'response': answer}

api.add_resource(Chatbot, '/chatbot')

if __name__ == '__main__':
    trainer = Trainer(config.load("config_spacy.yml"))
    training_data = load_data('demo-rasa.json')
    interpreter = trainer.train(training_data)
    app.run(port=5000, debug=True)
