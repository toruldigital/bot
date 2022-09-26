# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, ConversationPaused
import smtplib
from email.message import EmailMessage
#from actions import config
#
# from actions.api.rasaxapi import RasaXAPI

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionTagDocsSearch(Action):
    """Tag a conversation in Rasa X according to whether the docs search was helpful"""

    def name(self):
        return "action_tag_docs_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")

        if intent == "nlu_fallback":
            label = '[{"value":"docs search helpful","color":"e5ff00"}]'
        elif intent == "deny":
            label = '[{"value":"docs search unhelpful","color":"eb8f34"}]'
        else:
            return []

        rasax = RasaXAPI()
        rasax.tag_convo(tracker, label)

        return []

class ActionMail(Action):

    def name(self) -> Text:
        return "action_mail"

    def run(self, dispatcher, tracker, domain):
        sender_email = "" # senders Gmail id over here
        password = "" # senders Gmail's Password over here

        rec_email = "" # Receiver of the Mail

        conversation = tracker.events
        body = [] # Body of the Mail
        
        for i in conversation:
            if i['event'] == 'user':
                user = 'User: {}'.format(i['text'])
                body.append(user) # add user input to the body of the email
                #user = print('user: {}'.format(i['text']))
            elif i['event'] == 'bot': 
                bot = 'Bot: {}'.format(i['text'])
                body.append(bot) # add bot response to the body of the email
                #bot = print('Bot: {}'.format(i['text']))


        msg = EmailMessage()
        msg['Subject'] = "Rasa X - Torul Bot" # Subject of Email
        msg['From'] = sender_email
        msg['To'] = rec_email

        msg.set_content("Please review this conversation: \n\n" + "\n\n".join(body)) # Email body or Content

        #### >> Code from here will send the message << ####
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # Added Gmails SMTP Server
            smtp.login(sender_email, password) # This command Login SMTP Library using your GMAIL
            smtp.send_message(msg) # This Sends the message
            print('Mail sent')

        return []

class PauseConversation(Action):
    """Pause the conversation so the the
    assistant won't respond"""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "pause_conversation"

    def run(self, dispatcher, tracker, domain):
        print("Conversation paused")
        return [ConversationPaused()]