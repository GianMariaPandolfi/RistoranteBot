python -m rasa_nlu.train -c nlu_config.yml --data data/nlu.md -o models --fixed_model_name nlu --project current --verbose

python -m rasa_core.train -d domain.yml -s data/stories.md -o models/rasa_core/current/dialogue -c policies.yml

python -m rasa_core.run -d models/rasa_core/current/dialogue -u models/current/nlu --endpoints config/endpoints.yml 