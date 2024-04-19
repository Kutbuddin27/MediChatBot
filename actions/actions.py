# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Text, Dict, List
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .translator import response_further_test,test_descript
from .calender_function import display_calendar

language = []
translator = Translator()
typ=[]
date = []
visit = []


#######################################################Medical Test Information###############################################################
class SelectLanguageText(Action):
    def name(self) -> Text:
        return "action_select_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        language.append(text)
        # Example: Fetching dynamic options from an external source
        option_to_intent_mapping = {
            '🔬'+translator.translate("MedicalTests", dest=f'{language[0][:2]}').text: "lab_tests",
            '📅'+translator.translate("Book An Appointment", dest=f'{language[0][:2]}').text: "Appointment_booking",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"/{intent_name}"})
        button_reply = translator.translate("Please choose one of the following options: ", dest=f'{language[0][:2]}').text+'👇'
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return []
    
class ActionTestType(Action):

    def name(self) -> Text:
        return "action_test_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        option_to_intent_mapping = {
            '🩸'+translator.translate("Blood-Tests", dest=f'{language[0][:2]}').text: "blood-test",
            '💧'+translator.translate("Urine-Tests", dest=f'{language[0][:2]}').text: "urine-test",
            '📷'+translator.translate("Imaging-Tests", dest=f'{language[0][:2]}').text: "imaging-test",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"{intent_name}"})
        button_reply = translator.translate("Please choose one of the following options: ", dest=f'{language[0][:2]}').text+'👇'
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return []    
    
class ActionConvertText(Action):

    def name(self) -> Text:
        return "action_further_test_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        
        if text=="blood-test":
            buttons = [
                #translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text
                {"title": translator.translate("COMPLETE BLOOD COUNT (CBC)", dest=f'{language[0][:2]}').text, "payload": "cbc"},
                {"title": translator.translate("RED BLOOD CELLS (RBC COUNT)", dest=f'{language[0][:2]}').text, "payload": "rbc"},
                # Add more buttons for other blood tests as needed
            ]
            typ.append(text)
            dispatcher.utter_message(text=translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text+"👇", buttons=buttons)
        elif text=="urine-test":
            buttons = [
                #translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text
                {"title": translator.translate("URINE EXAMINATION, ROUTINE; URINE, R/E", dest=f'{language[0][:2]}').text, "payload": "RE"},
                {"title": translator.translate("URINE EXAMINATION, ROUTINE; URINE R/E, AUTOMATED", dest=f'{language[0][:2]}').text, "payload": "REA"},
                # Add more buttons for other blood tests as needed
            ]
            typ.append(text)
            dispatcher.utter_message(text=translator.translate("select type of urine-test :", dest=f'{language[0][:2]}').text+"👇", buttons=buttons)
        elif text=="imaging-test":
            buttons = [
                #translator.translate("select type of blood-test :", dest=f'{language[0][:2]}').text
                {"title": translator.translate("Magnetic Resonance imaging(MRI)", dest=f'{language[0][:2]}').text, "payload": "mri"},
                {"title": translator.translate("X-ray", dest=f'{language[0][:2]}').text, "payload": "xray"},
                # Add more buttons for other blood tests as needed
            ]
            typ.append(text)
            dispatcher.utter_message(text=translator.translate("select type of imaging-test :", dest=f'{language[0][:2]}').text+"👇", buttons=buttons)
        # language.clear()

        return []

class ActionDisplayCard(Action):

    def name(self) -> Text:
        return "action_display_card"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        typ.append(text)
        card = test_descript(typ[0],typ[1],response_further_test)
        dispatcher.utter_message(translator.translate(card, dest=f'{language[0][:2]}').text,parse_mode="Markdown")
        language.clear()
        typ.clear()
        return []

    
#######################################################Booking of an appointment##################################################################



class ActionAskVisit(Action):
    def name(self) -> Text:
        return "action_ask_visit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        language.append(text)
        # Example: Fetching dynamic options from an external source
        option_to_intent_mapping = {
            '🏠'+translator.translate("Home Visit", dest=f'{language[0][:2]}').text: "homevisit",
            '🏥'+translator.translate("Lab Visit", dest=f'{language[0][:2]}').text: "labvisit",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"{intent_name}"})
        button_reply = translator.translate("Please choose one of the following options: ", dest=f'{language[0][:2]}').text+"👇"
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)
        
        return []
class ActionDisplayCalendarMessage(Action):
    def name(self) -> Text:
        return "action_display_calendar_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Check if the previous user event was a button click
        button_message = tracker.latest_message
        text = button_message.get('text', '')
        visit.append(text)
    #   dispatcher.utter_message(text="Please select the date in the second screen which is open for your appointment")
        return []

class ActionShowCalendar(Action):
    def name(self) -> Text:
        return "action_show_calendar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        selected_date = display_calendar()
        date.append(selected_date)
        dispatcher.utter_message(text=f"You chose {visit[0]} on {date[0]}")
        visit.clear()
        date.clear()
        return []
#rasa run -m models --enable-api --cors "*" --debug  
