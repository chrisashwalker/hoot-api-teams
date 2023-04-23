# Hoot Teams API
The teams management service for [Hoot](https://github.com/chrisashwalker/hoot) - a tiny Human Resources management system built upon microservices.  
Developed with Python Flask.

## Create virtual env
```
python -m venv env
```

## Activate env
```
source ./env/bin/activate
```

## Install requirements
```
python -m pip install -r ./src/requirements.txt
```

## Write requirements
```
pip freeze > ./src/requirements.txt
```

## Run
```
python -m flask --app src.app.main run --port 8003
```

## Hot reload
```
python -m flask --app src.app.main run --port 8003 --debug
```

## Build Docker image
```
docker build -t hoot-api-teams ./src
```

## Create and run docker container
```
docker run --name hoot-api-teams-container -p 8003:8003 hoot-api-teams 
```
