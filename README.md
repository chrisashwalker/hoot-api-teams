## Create virtual env
python -m venv env

## Activate env
source ./env/bin/activate

## Install requirements
python -m pip install -r ./src/requirements.txt

## Write requirements
pip freeze > ./src/requirements.txt

## Run tests
python -m pytest -s

## Execute app
python -m src.app.main

## Create docker image
docker build -t hoot-api-teams ./src

## Run docker image
docker run --name hoot-api-teams-container -p 5000:80 hoot-api-teams 