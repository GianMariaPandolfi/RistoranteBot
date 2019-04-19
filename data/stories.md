## saluto
* saluto
  - utter_saluto


## informazioni apertura happy
* saluto
  - utter_saluto
* informazioni_apertura
  - utter_informazioni_apertura
* ringraziamenti
  - utter_ringraziamenti


## informazioni apertura e richiesta_di_prenotazione happy
* saluto
  - utter_saluto
* informazioni_apertura
  - utter_informazioni_apertura
* richiesta_di_prenotazione
  - action_controllo_richiesta
  - prenotazione_form
  - form{"name": "prenotazione_form"}
  - form{"name": null}
  - utter_riepilogo_prenotazione
* afferma
  - action_conferma_prenotazione
* saluto_finale
  - utter_saluto_finale

## saluto e richiesta_di_prenotazione happy
* saluto
  - utter_saluto
* richiesta_di_prenotazione
  - action_controllo_richiesta
  - prenotazione_form
  - form{"name": "prenotazione_form"}
  - form{"name": null}
  - utter_riepilogo_prenotazione
* nega
  - action_conferma_prenotazione
* saluto_finale
  - utter_saluto_finale

## informazioni di apertura unhappy
* saluto
  - utter_saluto
* chitchat
  - utter_chitchat
* informazioni_apertura
  - utter_informazioni_apertura
* ringraziamenti
  - utter_ringraziamenti

## saluto e richiesta di prenotazione unhappy
* saluto
  - utter_saluto
* richiesta_di_prenotazione
  - action_controllo_richiesta
  - prenotazione_form
  - form{"name": "prenotazione_form"}
* chitchat
  - utter_chitchat
  - prenotazione_form
  - form{"name": null}
  - utter_riepilogo_prenotazione
* afferma
  - action_conferma_prenotazione
* saluto_finale
    - utter_saluto_finale

## richiesta_di_prenotazione

* richiesta_di_prenotazione
  - action_controllo_richiesta
  - prenotazione_form
  - form{"name": "prenotazione_form"}
  - form{"name": null}
  - utter_riepilogo_prenotazione
* afferma
  - action_conferma_prenotazione
* saluto_finale
  - utter_saluto_finale
