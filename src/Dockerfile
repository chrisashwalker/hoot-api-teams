FROM python:3.9
RUN pip3 install --upgrade pip
COPY ./ ./
RUN  pip3 install -r requirements.txt
CMD ["python", "-m", "flask", "--app", "app.main", "run", "--port", "8003", "--debug"]