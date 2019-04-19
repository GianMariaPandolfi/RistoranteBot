from typing import Dict, Text, Any, List, Union, Optional
from rasa_core_sdk import Action, Tracker, ActionExecutionRejection
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import SlotSet
import unicodedata


class PrenotazioneForm(FormAction):

    def name(self):
        return "prenotazione_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["giorno", "orario", "num_persone"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {"giorno": self.from_entity(entity="giorno", intent=["informa", "richiesta_di_prenotazione"],),
                "orario": [self.from_entity(entity="orario", intent=["informa", "richiesta_di_prenotazione"]),
                           self.from_entity(entity="numero")],
                "num_persone": [self.from_entity(entity="num_persone", intent=["informa", "richiesta_di_prenotazione"]),
                                self.from_entity(entity="numero")],
                }

    @staticmethod
    def giorno_db() -> List[Text]:

        return ["oggi",
                "domani",
                "lunedi",
                "martedi",
                "mercoledi",
                "giovedi",
                "venerdi",
                "sabato",
                "domenica"]

    @staticmethod
    def is_int(string: Text) -> bool:

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_giorno(self,
                        value: Text,
                        dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> Optional[Text]:
        value = unicodedata.normalize('NFD', value) \
            .encode('ascii', 'ignore') \
            .decode("utf-8")  # elimina gli accenti
        if value.lower() == "lunedi":
            dispatcher.utter_template('utter_lunedi_chiuso', tracker)
            dispatcher.utter_template('utter_informazioni_apertura', tracker)
            return None
        elif value.lower() in self.giorno_db():
            return value
        else:
            dispatcher.utter_template('utter_default_incomprensione', tracker)
            return None

    def validate_orario(self,
                        value: Text,
                        dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]
                        ):

        if self.is_int(value) and ((11 <= int(value) <= 15) or (18 <= int(value) <= 23)):
            return value
        elif self.is_int(value):
            dispatcher.utter_template('utter_orario_chiuso', tracker)
            dispatcher.utter_template('utter_informazioni_apertura', tracker)
        else:
            dispatcher.utter_template('utter_default_incomprensione', tracker)
            return None

    def validate_num_persone(self,
                             value: Text,
                             dispatcher: CollectingDispatcher,
                             tracker: Tracker,
                             domain: Dict[Text, Any]
                             ):

        if self.is_int(value):
            return value
        else:
            dispatcher.utter_template('utter_default_incomprensione', tracker)
            return None

    def validate(self, dispatcher, tracker, domain):
        try:
            return super().validate(dispatcher, tracker, domain)
        except ActionExecutionRejection as e:
            # could not extract entity
            dispatcher.utter_template('utter_default_incomprensione', tracker)
            return []

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:

        dispatcher.utter_template('utter_data_complete', tracker)
        return []


class ActionConfermaPrenotazione(Action):
    def name(self):
        return "action_conferma_prenotazione"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')
        if intent == "afferma":
            dispatcher.utter_template('utter_prenotazione_confermata', tracker)
            return [SlotSet('conferma_prenotazione', True)]
        if intent == "nega":
            dispatcher.utter_template('utter_prenotazione_non_confermata', tracker)
            return [SlotSet('conferma_prenotazione', False)]


class ActionControlloRichiesta(Action):
    def name(self):
        return "action_controllo_richiesta"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):  # type: (...) -> List[Dict[Text, Any]]

            giorno = next(tracker.get_latest_entity_values('giorno'), None)
            orario = next(tracker.get_latest_entity_values('orario'), None)

            if giorno is not None:
                giorno = unicodedata.normalize('NFD', giorno) \
                    .encode('ascii', 'ignore') \
                    .decode("utf-8")
                if giorno.lower() == 'lunedi':
                    dispatcher.utter_template('utter_lunedi_chiuso', tracker)
                    dispatcher.utter_template('utter_informazioni_apertura', tracker)
                    giorno = None
                elif giorno.lower() not in self.giorno_db():
                    giorno = None

            if orario is not None:
                if self.is_int(orario) and not((11 <= int(orario) <= 15) or (18 <= int(orario) <= 23)):
                    orario = None
                    dispatcher.utter_template('utter_orario_chiuso', tracker)
                    dispatcher.utter_template('utter_informazioni_apertura', tracker)

            return [SlotSet('giorno', giorno),
                    SlotSet('orario', orario)]

    @staticmethod
    def giorno_db() -> List[Text]:

        return ["oggi",
                "domani",
                "lunedi",
                "martedi",
                "mercoledi",
                "giovedi",
                "venerdi",
                "sabato",
                "domenica"]

    @staticmethod
    def is_int(string: Text) -> bool:

        try:
            int(string)
            return True
        except ValueError:
            return False
