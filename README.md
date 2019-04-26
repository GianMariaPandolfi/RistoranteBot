# RistoranteBot

To install the bot and run it on Docker, please clone the repo and run:

```
docker run -v ${pwd}:/app/project -v ${pwd}/models/rasa_nlu:/app/models giambo/spacy_it:latest run python -m rasa_nlu.train -c project/config/nlu_config.yml -d project/data/nlu.md  -o models  --project current

```
This will train the NLU model

To train the core model, please run: 

```
docker run -v ${pwd}:/app/project -v ${pwd}/models:/app/models rasa/rasa_core:stable train --domain project/domain.yml --stories project/data/stories.md --out models/rasa_core
```
After the training you can start the bot running:

```
docker-compose up
```

This will start the bot and install all the requirements (I'll try to reduce them in future).

To send message to the bot:

```
curl --request POST \
  --url http://localhost:5005/webhooks/rest/webhook \
  --header 'content-type: application/json' \
  --data '{
    "message": "ciao"
  }'
```

The chatbot should then answer something like:

```
[
  {
    "recipient_id": "default",
    "text": "Ciao, come posso aiutarti?"
  }
]
```

If the chatbot cannot understand you, the answer is []

The bot is not ready to understand everything,
but it should be ready to understand a typical conversation like this:

```
- Ciao

                Ciao, come posso aiutarti?
                
- quando siete aperti?
              
              siamo aperti dal martedi alla domenica,    
              per pranzo 11:00-15:00, per cena 18:00-23:00. 
              
- vorrei effettuare una prenotazione
                
               Per quale giorno voleva prenotare?

- martedi

               A che ora?
                
- 12           

               Per quante persone voleva effettuare la prenotazione? 
                
- 5
                Ecco la sua prenotazione:
                - giorno: martedi
                - orario: 12
                - numero persone: 5
                 Desidera confermarla?"

- si
                 la sua prenotazione è confermata.
 
- grazie, a presto

                  A presto.
 
```                
