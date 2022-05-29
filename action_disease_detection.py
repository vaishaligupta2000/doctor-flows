# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import logging
import random
from helper import Diagnosis


bot_diagnosis = Diagnosis()
bot_diagnosis.train()

suggested_so_far = []

class ActionHandleSymptom(Action):

    def name(self) -> Text:
        return "action_handle_symptom"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the last message sent by user
        message = tracker.latest_message.get('text')

        # Get symptoms slot
        syms = tracker.get_slot("symptom_list")

        if syms is None:
            syms = []

        '''
        #let a symptom list - symps exits
        if message not in syms:
            temp = process.extraction("message", symps)
            syms.append(temp[0])
        '''

        # Check if symptom in list
        if message not in syms:
            temp = bot_diagnosis.fuzzy_symptoms(message)
            logging.info(f"{temp}")
            logging.info(type(temp))
            logging.info(type(message))
            syms.append(temp)
    
        else:
            dispatcher.utter_message("Already noted that you have: "+message)
            return []
        
        # Update slot
        SlotSet("symptom_list", syms)

        # Get suggested symptom based on input
        suggested_symptom = bot_diagnosis.suggest_symptoms(syms)
        
        # Check if symptom not already suggested
        clean_syms=[] #use this

        for symp in suggested_symptom:
            if symp not in syms and symp not in suggested_so_far:
                clean_syms.append(symp)
            else:
                suggested_so_far.append(symp)

        if(len(clean_syms)>0):
            num = random.randrange(0,len(clean_syms))
        else:
            dispatcher.utter_template('utter_alternative', tracker)
            return [SlotSet("symptom_list", syms)]

    
        buttons = [{"title": "Yes", "payload": clean_syms[num]},{"title":"No", "payload": "/deny"}]

        dispatcher.utter_message("You said you have: "+ temp)
        dispatcher.utter_button_message("Do you also have "+clean_syms[num]+"?", buttons)

        return [SlotSet("symptom_list", syms)]

class ActionDiagnosis(Action):

    def name(self) -> Text:
        return "action_diagnosis"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get symptoms slot
        syms = tracker.get_slot("symptom_list")

        # Get diagnosis
        diag = bot_diagnosis.predict(syms)


        # Send message
        dispatcher.utter_message("Diagnosis: "+str(diag[0]))
        
        return [AllSlotsReset()]