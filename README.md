# RistoranteBot

1 docker run -v ${pwd}:/app/project -v ${pwd}/models/rasa_nlu:/app/models spacy_it:latest run python -m rasa_nlu.train -c project/nlu_config.yml -d project/data/nlu.md  -o models  --project current

2 docker run -v ${pwd}:/app/project -v ${pwd}/models:/app/models rasa/rasa_core:latest train --domain project/domain.yml --stories project/data/stories.md --out models/rasa_core

3 docker-compose up
