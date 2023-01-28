from rasa_sdk import Action

class CustomActions(Action):
    def __init__(self):
        with open("intents.json", "r") as file:
            self.intents = json.load(file)

    def action(self, question):
        for intent in self.intents:
            lst = intent["questions"]
            if question.lower() in all_lower(lst):
                return intent["answer"]


