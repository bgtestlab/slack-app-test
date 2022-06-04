import os
import json
import sys
from os import path

from flask import Flask, Response, jsonify
from slackeventsapi import SlackEventAdapter
from threading import Thread
from slack import WebClient

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from slack_app.commands import commands
from slack_app.logger import LOG

LOG.info("server is running!")


def create_app(test_config=None):
    # Create an app
    app = Flask(__name__)

    # Read slack configs
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SIGNING_SECRET = os.getenv("SIGNING_SECRET")
    VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")

    # Initiate Slack client
    slack_client = WebClient(SLACK_BOT_TOKEN)

    # Routes
    @app.route("/healthz")
    def healthcheck():
        return jsonify({"success": True, "status": "healthy"})

    @app.route("/")
    def event_hook(request):
        json_dict = json.loads(request.body.decode("utf-8"))
        if json_dict["token"] != VERIFICATION_TOKEN:
            return {"status": 403}

        if "type" in json_dict:
            if json_dict["type"] == "url_verification":
                response_dict = {"challenge": json_dict["challenge"]}
                return response_dict
        return {"status": 500}

    slack_events_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)

    @slack_events_adapter.on("app_mention")
    def handle_message(event_data):
        def send_reply(value):
            event_data = value
            message = event_data["event"]
            if message.get("subtype") is None:
                commands(slack_client, message)

        thread = Thread(target=send_reply, kwargs={"value": event_data})
        thread.start()
        return Response(status=200)

    # Error Handling
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    return app


app = create_app()


# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)