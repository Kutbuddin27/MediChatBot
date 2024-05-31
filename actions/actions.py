# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Text, Dict, List
from googletrans import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector as mc

from .Functions.translator import database_cred
from .Functions.test_information import SelectLanguageText,ActionConvertText,ActionDisplayCard,language
from .Functions.appointment import ActionAskVisit,ActionAskDate,ActionShowSlots,ActionBookAppointment
from .Functions.FAQ import SelectComplainFeedback,SelectTypeComplainFeedback,ActionSubmitComplainFeedback

translator = Translator()
#####################################################Medical test information#####################################################################       

#####################################################Book an Appointment##########################################################################

#####################################################Admin pannel#################################################################################
admin = []    
admin_test=[]
class ActionCheckPassword(Action):
    def name(self) -> Text:
        return "action_check_password"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message.get('text', '').strip()
        if text=="abc@1230":
            option_to_intent_mapping = {
            '🔬'+"MedicalTests": "lab_tests1",
            '📅'+"Book An Appointment": "Appointment_booking1",
        }
            # Generate buttons dynamically
            buttons = []
            for option,intent_name in option_to_intent_mapping.items():
                buttons.append({"title": option, "payload": f"/{intent_name}"})
            button_reply = "In which of the following you want to make changes:🤔 "
            # Send the message with dynamic buttons
            dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)  
        else:
            dispatcher.utter_message(text="Wrong password!😒")
        
        return []

class AdminSelectSelTestDetail(Action):
    test_buttons = {
        "a": {
            "text": "blood-test",
            "options": [
                {"title": "COMPLETE BLOOD COUNT (CBC)", "payload": "cbc"},
                {"title": "RED BLOOD CELLS (RBC COUNT)", "payload": "rbc"},
                # Add more buttons for other blood tests as needed
            ],},
        "b": {
            "text": "urine-test",
            "options": [
                {"title": "URINE EXAMINATION, ROUTINE; URINE, R/E", "payload": "RE"},
                {"title": "URINE EXAMINATION, ROUTINE; URINE R/E, AUTOMATED", "payload": "REA"},
                # Add more buttons for other urine tests as needed
            ],},
        "c": {
            "text": "imaging-test",
            "options": [
                {"title": "Magnetic Resonance imaging(MRI)", "payload": "mri"},
                {"title": "X-ray", "payload": "xray"},
                # Add more buttons for other imaging tests as needed
            ],},
            }
    def name(self) -> Text:
        return "action_get_selected_test_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '').lower()     

        if  text[0] in self.test_buttons:
            button_data = self.test_buttons[text[0]]
            admin_test.append(button_data['text'])
            buttons = button_data["options"]
            dispatcher.utter_message(text=f"Select type of {button_data['text']} 👇", buttons=buttons)
        else:
            dispatcher.utter_message(text="To be released soon")

        return []
    
class AdminSelectLanguageText(Action):
    def name(self) -> Text:
        return "action_testtype_details_askchange"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        admin_test.append(text)
        db = database_cred(mc)  # Assuming mc is defined elsewhere
        cursor = db.cursor()
        cursor.execute("SELECT test_type, test_type_type, name, description, price, precondition, reporting FROM test INNER JOIN card ON test.test_type_type = card.test_t_t WHERE test_type_type = %s",(text,))
        data = cursor.fetchall()
        cursor.close()
        db.close()
        if data:
            result = ""
            for row in data:
                test_type, test_type_type, name, description, price, precondition, reporting = row
                result += f"<b>Tests:</b> {test_type}<br><b>Test Type</b> : {test_type_type}<br><b>Name:</b> {name}<br><b>Description:</b> {description[:100] + '...' if len(description) > 100 else description}<br><b>Price:</b> {price}<br><b>Precondition:</b> {precondition}<br><b>Reporting:</b> {reporting}\n\n"
            dispatcher.utter_message(result)
            dispatcher.utter_message("Type one of the following character of column in which you want to change<br><b>a </b>Tests<br><b>b </b>Test Type<br><b>c </b>Name<br><b>d </b>Description<br><b>e </b>Price<br><b>f </b>Precondition<br><b>g </b>Reporting")
        else:
            dispatcher.utter_message(text="No test details found for the provided criteria.")
        
        return []

class AdminSelectTestTypeChange(Action):
    columns = {
        'a': 'test_type',
        'b': 'test_type_type',
        'c': 'name',
        'd': 'description',
        'e': 'price',
        'f': 'precondition',
        'g': 'reporting'
    }
    def name(self) -> Text:
        return "action_testtype_asktypechange"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')

        db = database_cred(mc)
        cursor = db.cursor()
        if text[0] in self.columns:
            col = self.columns[text[0]]
            admin_test.append(col)
            print(col)
            print(admin_test)
            query = f"SELECT {col} FROM test INNER JOIN card ON test.test_type_type = card.test_t_t WHERE test_type_type = %s"
            cursor.execute(query, (admin_test[1],)) 
            data = cursor.fetchall()
            db.commit()
            dispatcher.utter_message(text=f"Previouslt it was written {data[0][0]}")
            dispatcher.utter_message(text="What you want to edit in it just write down.👇")

        return []

class AdminSelectTestTypeChange(Action):

    def name(self) -> Text:
        return "action_testinformation_change"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        db = database_cred(mc)
        cursor = db.cursor()
        if admin_test[2]=='test_type':
            query = f"UPDATE test SET test_type = %s WHERE test_type_type = %s"
            cursor.execute(query,(text,admin_test[1]))
        elif admin_test[2]=='test_type_type':
            query = f"UPDATE test INNER JOIN card ON test.test_type_type = card.test_t_t SET test.test_type_type = {text},card.test_t_t={text} WHERE test.test_type_type = {admin_test[1]}"
            cursor.execute(query)
        else:
            query = f"UPDATE card SET {admin_test[2]} = %s WHERE test_t_t = %s"
            cursor.execute(query,(text,admin_test[1]))

        db.commit()
        dispatcher.utter_message(text="Your changes are commited successfully")
        cursor.execute("SELECT  name, description, price, precondition, reporting FROM  card  WHERE test_t_t = %s",(admin_test[1],))
        data = cursor.fetchall()
        cursor.close()
        db.close()
        if data:
            result = ""
            for row in data:
                name, description, price, precondition, reporting = row
                result += f"<b>Name:</b> {name}<br><b>Description:</b> {description[:100] + '...' if len(description) > 100 else description}<br><b>Price:</b> {price}<br><b>Precondition:</b> {precondition}<br><b>Reporting:</b> {reporting}\n\n"
                dispatcher.utter_message(result)
        admin_test.clear()
        return []
           
class AdminSelectLanguageText(Action):
    def name(self) -> Text:
        return "action_booking_change"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Example: Fetching dynamic options from an external source
        option_to_intent_mapping = {
            '🏠'+"Home Visit": "homevisit",
            '🏥'+"Lab Visit": "labvisit",
                        # Add more mappings as needed
        }
        # Generate buttons dynamically
        buttons = []
        for option,intent_name in option_to_intent_mapping.items():
            buttons.append({"title": option, "payload": f"{intent_name}"})
        button_reply ="Please choose one of the following options: "
        # Send the message with dynamic buttons
        dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)

        return [] 

class ActionShowData(Action):
    def name(self) -> Text:
        return "action_show_data"
 #   @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        text = latest_message.get('text','')
        admin.append(text)
        # Connect to MySQL
        db = database_cred(mc)
        cursor = db.cursor()
        data = []
        
        if admin[0][:4] == 'home':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Home'")
            data = cursor.fetchall()
        elif admin[0][:3] == 'lab':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Lab'")
            data = cursor.fetchall()
        cursor.close()
        db.close()
        data_text = "Here is the previous slots mentioned <br>"
        for i in data:
            data_text+=i[0]+"<br>"
        dispatcher.utter_message(text=data_text,parse_mode="Markdown")        
        return []


class ActionAddDel(Action):
    def name(self) -> Text:
        return "action_add_upd_del"
  #  @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            option_to_intent_mapping = {
            "✔Add": "add",
            "❌Delete": "delete"
        }
            # Generate buttons dynamically
            buttons = []
            for option,intent_name in option_to_intent_mapping.items():
                buttons.append({"title": option, "payload": f"{intent_name}"})
            button_reply = "In which of the following you want change in your slots: "
            # Send the message with dynamic buttons
            dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)   

            return []

class ActionAskTime(Action):
    def name(self) -> Text:
        return "action_ask_time"
  #  @action_timeout    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            latest_message = tracker.latest_message
            text = latest_message.get('text','')
            admin.append(text)

            dispatcher.utter_message(text=f"Enter the slot time which you want to {admin[1]}<br>Example: 10:00 <b>HH:MM</b>")

            return []

class  ActionChangeTime(Action):
    def name(self) -> Text:
        return "action_change_time"
  #  @action_timeout
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            latest_message = tracker.latest_message
            text = latest_message.get('text','')
            admin.append(text)

            db =  database_cred(mc)
            cursor = db.cursor()
            data = []
            if admin[0][:4]=='home':
                if admin[1]=='add':
                    cursor.execute("INSERT INTO slots (slot_time,appointment_type) VALUES (%s,%s)",(admin[2]+":00",'Home',))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='Home'")
                    data = cursor.fetchall()
                    db.commit()
                elif admin[1]=='delete':
                    cursor.execute("DELETE FROM slots WHERE slot_time= %s ",(admin[2]+":00",))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='Home'")
                    data = cursor.fetchall()
                    db.commit()
            elif admin[0][:3]=='lab':
                if admin[1]=='add':
                    cursor.execute("INSERT INTO slots (slot_time,appointment_type) VALUES (%s,%s)",(admin[2]+":00",'Lab',))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='lab'")
                    data = cursor.fetchall()
                    db.commit()
                elif admin[1]=='delete':
                    cursor.execute("DELETE FROM slots WHERE slot_time= %s ",(admin[2]+":00",))
                    cursor.execute("SELECT slot_time,appointment_type FROM slots WHERE appointment_type='lab'")
                    data = cursor.fetchall()
                    db.commit()        

            cursor.close()
            db.close()
            text = "Updated Slots: <br>"
            for i in data:
                text+="  "+i[0]+'<br>'
            dispatcher.utter_message(text=text,parse_mode="Markdown")  
            admin.clear()      
            return [SlotSet("is_authenticated", None)]
         
#rasa run -m models --enable-api --cors "*" --debug  