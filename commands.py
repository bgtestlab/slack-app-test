import json
import re
import sys
from os import path
import requests

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from slack_app.logger import LOG

WORKFLOW_URL = (
    "https://api.github.com/repos/boramgwon/selenium-browser-test/actions/workflows/27257286/dispatches"
)

# Read Github token
GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")

greetings = ["hi", "hello"]
run_workflow = ["run"]


def commands(slack_client, input_message):
    global message_dash_users

    command = input_message.get("text")
    channel_id = input_message["channel"]
    message = ""

    print(command.split()[0].lower())

    # User
    if any(item in command.lower() for item in greetings):
        message = f"Hello <@{input_message['user']}>! :tada:"

    # Test run
    # Example: @Autotest run for "sanity" on server1
    elif any(item in command.lower() for item in run_workflow):
        check_test_params, check_test_server = None, None

        # Case 1. Designate both target and server
        if re.search("for(.+?)on", command):
            check_test_params = re.search("for(.+?)on", command).group(1).strip()

        # Case 2. Designate target only
        elif "for" in command:
            check_test_params = command.split("for")[1].strip()

        # Case 3. Designate server only
        elif "on" in command:
            check_test_server = command.split("on")[1].strip()

        message = trigger_ci(input_message["ts"], check_test_params, check_test_server)
    else:
        message = "Command is not supported :smiling_face_with_tear:"
    slack_client.chat_postMessage(
        channel=channel_id, text=message, thread_ts=input_message["ts"]
    )


def trigger_ci(thread_ts, test_params=None, test_server=None) -> str:
    message = ""

    # Message composition for Actions
    global AUTH_TOKEN
    headers = {
        "Content-Type": "application/vnd.github.v3+json; charset=utf-8",
        "Authorization": f"Bearer {AUTH_TOKEN}",
    }
    data = {"ref": "main", "inputs": {"thread_ts": thread_ts}}

    if test_params:
        data["inputs"]["tags"] = test_params

    if test_server:
        data["inputs"]["environment"] = test_server

    LOG.info(data)

    res = requests.post(url=WORKFLOW_URL, headers=headers, data=json.dumps(data))
    LOG.info(f"Workflow response: {res.status_code}")
    if res.status_code != 204:
        message = f"Test trigger failed :eyes: (CI status code: {res.status_code}) "

    return message

