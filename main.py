from flask import Flask, request, jsonify
from rasa_sdk import Action
from rasa_sdk.executor import ActionExecutor
from rasa_sdk.events import SlotSet

app = Flask(name)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    action = data["queryResult"]["action"]
    question = data["queryResult"]["queryText"]
    executor = ActionExecutor()
    results = executor.run(action, question)
    return jsonify(results)

if name == "main":
    app.run()