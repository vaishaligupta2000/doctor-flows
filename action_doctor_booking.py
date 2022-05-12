from typing import Any, Text, Dict, List
from urllib import response

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from twilio.rest import Client

import pandas as pd

class ValidateForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name", "number","location", "email", "age" ,"time", "doc_spec"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # No more slots to fill
        return [SlotSet("requested_slot", None)]


    
class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"
    
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        Specialisation = tracker.get_slot("doc_spec")
        df = pd.read_csv("doctor.csv")

        doc = df.where(df['Specialization'].str.lower() == Specialisation.lower())
        doc = doc.dropna()

        if not doc.empty:
            doctor = doc.iloc[0,0]
    
        dispatcher.utter_message(text=f"Thank you for giving the details! {doctor} will be seeing you!")
        dispatcher.utter_message(template="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Location = tracker.get_slot("location"),
                                 Mobile_number = tracker.get_slot("number"),
                                 Email=tracker.get_slot("email"),
                                 Age=tracker.get_slot("age"),
                                 Time=tracker.get_slot("time"), 
                                 Specialisation = tracker.get_slot('doc_spec')
                                 )  
        dispatcher.utter_message(text="Your appointment is confirmed and you will receive an SMS on your phone")

        #adding country code
        # num = tracker.get_slot("number")
        # mob = f"+91{num}"

        account_sid = 'AC4f0393d0388dd8dd0b106f4c01e709b7'
        auth_token = 'a89811b6101f2d10d8286f4025e70929' 
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='+19897350983',
            body=dispatcher.utter_message(template="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Location = tracker.get_slot("location"),
                                 Mobile_number = tracker.get_slot("number"),
                                 Email=tracker.get_slot("email"),
                                 Age=tracker.get_slot("age"),
                                 Time=tracker.get_slot("time"), 
                                 Specialisation = tracker.get_slot('doc_spec')
                                 ) ,  #'hello, this is a test message for automation',
            to = '+919418685850'  
        )

        print(message.sid)

        # dispatcher.utter_message(text="Message has been sent successfully to {}".format(tracker.get_slot("mobile_number")))
        dispatcher.utter_message(f"Message has been sent successfully sent")