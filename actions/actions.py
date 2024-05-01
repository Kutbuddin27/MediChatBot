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
from .translator import response_further_test,test_descript
import mysql.connector as mc
import random

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

#####################################################Medical test information#####################################################################    
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
    
#################################################################Book an Appointment############################################################################
appoint = []
class ActionAskVisit(Action):
    def name(self) -> Text:
        return "action_ask_visit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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

class ActionAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        appoint.append(text)
        date_desc = translator.translate('Enter the date on which you want to book appointment',dest=f'{language[0][:2]}').text
        dispatcher.utter_message(text=f"📅{date_desc}<br>In dd-mm-yyyy format for eg 02-05-2024",parse_mode="Markdown")

        return []
    
class ActionShowSlots(Action):
    def name(self) -> Text:
        return "action_show_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = tracker.latest_message
        text = latest_message.get('text', '')
        appoint.append(text)  # Split the message into words
        # Connect to MySQL
        db = mc.connect(
            host="localhost",
            user="root",
            password="",
            database="medichat"
        )
        cursor = db.cursor()
        data = []
        
        if appoint[0][:4] == 'home':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Home'")
            data = cursor.fetchall()
        elif appoint[0][:3] == 'lab':
            cursor.execute("SELECT slot_time FROM slots WHERE appointment_type='Lab'")
            data = cursor.fetchall()
        buttons = []
        for slot in data:
            slot_time = str(slot[0])
            buttons.append({"title": slot_time, "payload": slot_time})
        dispatcher.utter_message(text=translator.translate(f"Available slots for {appoint[0]} on date: {appoint[1]}👇",dest=f'{language[0][:2]}').text, buttons=buttons)
        cursor.close()
        db.close()
        return []
    
class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        appoint.append(tracker.get_slot('Time'))  
        name = tracker.get_slot('Name')
        number = str(tracker.get_slot('PhoneNumber'))
        address = tracker.get_slot('Address')[0]
        random_number = random.randint(999,10000)
        print(number)
        db = mc.connect(
            host="localhost",
            user="root",
            password="",
            database="medichat"
        )
        cursor = db.cursor()

        if appoint[0][:4]=='home':
            cursor.execute("INSERT INTO user (id,name,number,address) VALUES (%s,%s,%s,%s)",(random_number,name,number,address))
            cursor.execute("INSERT INTO appointment (user_id,date,time) VALUES (%s,%s,%s)",(random_number,appoint[1],appoint[2]))
            db.commit()
            cursor.execute("SELECT user_id,date,time FROM user INNER JOIN appointment ON user.id = appointment.user_id WHERE user.id=%s",((random_number,)))
            data = cursor.fetchall()
            dispatcher.utter_message(text="✔"+translator.translate(f"The lab-testers will be arriving for 🏠 Home-visit on {data[0][1]} at {data[0][2]}<br>your <b>appointment id</b> is <b>{data[0][0]}</b> ",dest=f'{language[0][:2]}').text,parse_mode="Markdown")
        elif appoint[0][:3]=='lab':
            cursor.execute("INSERT INTO user (id,name,number,address) VALUES (%s,%s,%s,%s)",(random_number,name,str(number),'lab-visit'));
            cursor.execute("INSERT INTO appointment (user_id,date,time) VALUES (%s,%s,%s)",(random_number,appoint[1],appoint[2]))
            db.commit()   
            cursor.execute("SELECT user_id,date,time FROM user INNER JOIN appointment ON user.id = appointment.user_id WHERE user.id=%s",((random_number,)))
            data = cursor.fetchall()
            dispatcher.utter_message(text="✔"+translator.translate(f"Your appointment for 🏥 Lab-visit is fixed on {data[0][1]} at {data[0][2]}<br>your <b>appointment id</b> is <b>{data[0][0]}</b> ",dest=f'{language[0][:2]}').text,parse_mode="Markdown")
        
        cursor.close()
        db.close()
        appoint.clear()
        language.clear()
        return [AllSlotsReset() ] 
#####################################################################Admin pannel#################################################################
admin = []
class ActionCheckPassword(Action):
    def name(self) -> Text:
        return "action_check_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message.get('text', '').strip()
        print(text)
        if text=="abc@1230":
            option_to_intent_mapping = {
            "🏠Home Visit": "homevisit",
            "🏥Lab Visit": "labvisit",
        }
            # Generate buttons dynamically
            buttons = []
            for option,intent_name in option_to_intent_mapping.items():
                buttons.append({"title": option, "payload": f"{intent_name}"})
            button_reply = "In which of the following you want to change slots: "
            # Send the message with dynamic buttons
            dispatcher.utter_message(text=f"{button_reply}", buttons=buttons)
            return [SlotSet("is_authenticated",True)]
        else:
            dispatcher.utter_message(text="Wrong password!😒")
            return [SlotSet("is_authenticated",False)]


class ActionShowData(Action):
    def name(self) -> Text:
        return "action_show_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        text = latest_message.get('text','')
        admin.append(text)
        # Connect to MySQL
        db = mc.connect(
            host="localhost",
            user="root",
            password="",
            database="medichat"
        )
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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            latest_message = tracker.latest_message
            text = latest_message.get('text','')
            admin.append(text)

            db = mc.connect(
            host="localhost",
            user="root",
            password="",
            database="medichat"
            )
            cursor = db.cursor()
            data = []
            print(admin[2])
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