from typing import Any, Text, Dict, List
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector as mc
from .test_information import language
from .translator import database_cred
translator = Translator()
feedback = []

class SelectComplainFeedback(Action):
    def name(self) -> Text:
        return "action_complain_feedback"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Example: Fetching dynamic options from an external source
        option_to_intent_mapping = {
            translator.translate("Complain", dest=f'{language[0][:2]}').text: "complain",
            translator.translate("Feedback", dest=f'{language[0][:2]}').text: "feedback",
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"{intent_name}"})
        button_reply = translator.translate("What do you want to tell: ", dest=f'{language[0][:2]}').text+'👇'
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return []
    
class SelectTypeComplainFeedback(Action):
    def name(self) -> Text:
        return "action_type_complain_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        feedback.append(text)
        button_reply = ''
        if text=='complain':
            button_reply ="😔"+translator.translate("Sorry, for the inconvinience, please type your complain and we will take necessary steps for that ", dest=f'{language[0][:2]}').text+'👇'
        elif text=='feedback':
            button_reply ="😃"+translator.translate("Thankyou for selecting, please type your feedback and we will review it ", dest=f'{language[0][:2]}').text+'👇'    
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}")

        return []    
    
class ActionSubmitComplainFeedback(Action):
    def name(self) -> Text:
        return "action_submit_complain_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        db = database_cred(mc)
        cursor = db.cursor()
        if feedback[0]=='complain':
            query = "INSERT INTO faq (complain) VALUES (%s)"
            cursor.execute(query, (text,))
            dispatcher.utter_message(text="Your Complain is submited successfully, the management will review it soon")
        elif feedback[0]=='feedback':
            query = "INSERT INTO faq (feedback) VALUES (%s)"
            cursor.execute(query, (text,))
            dispatcher.utter_message(text="Your Feedback is submited successfully, the management will review it soon")
        db.commit()
        cursor.close()
        db.close()
        feedback.clear()
        return []    