## Create virtual env
python -m venv env

## Activate env
source ./env/bin/activate

## Install requirements
python -m pip install -r ./src/requirements.txt

## Write requirements
pip freeze > ./src/requirements.txt

## Execute app
python -m flask --app src.app.main run --port 8003

## Hot reload
python -m flask --app src.app.main run --port 8003 --debug

## Create docker image
docker build -t hoot-api-teams ./src

## Run docker image
docker run --rm --name hoot-api-teams-container -p 8003:8003 hoot-api-teams 