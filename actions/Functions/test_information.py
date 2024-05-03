from typing import Any, Text, Dict, List
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from .translator import response_further_test,test_descript

language = []
translator = Translator()
typ=[]

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
        
        test_buttons = {
            "blood-test": [
                {"title": translator.translate("COMPLETE BLOOD COUNT (CBC)", dest=f'{language[0][:2]}').text, "payload": "cbc"},
                {"title": translator.translate("RED BLOOD CELLS (RBC COUNT)", dest=f'{language[0][:2]}').text, "payload": "rbc"},
                # Add more buttons for other blood tests as needed
            ],
            "urine-test": [
                {"title": translator.translate("URINE EXAMINATION, ROUTINE; URINE, R/E", dest=f'{language[0][:2]}').text, "payload": "RE"},
                {"title": translator.translate("URINE EXAMINATION, ROUTINE; URINE R/E, AUTOMATED", dest=f'{language[0][:2]}').text, "payload": "REA"},
                # Add more buttons for other urine tests as needed
            ],
            "imaging-test": [
                {"title": translator.translate("Magnetic Resonance imaging(MRI)", dest=f'{language[0][:2]}').text, "payload": "mri"},
                {"title": translator.translate("X-ray", dest=f'{language[0][:2]}').text, "payload": "xray"},
                # Add more buttons for other imaging tests as needed
            ]}
  # Check the test type and fetch corresponding buttons from the dictionary
        if text in test_buttons:
            buttons = test_buttons[text]
            typ.append(text)
            dispatcher.utter_message(text=translator.translate(f"select type of {text} :", dest=f'{language[0][:2]}').text + "👇", buttons=buttons)

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