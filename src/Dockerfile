FROM python:3.8-slim-buster
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code
CMD [ "python3", "-m" , "flask", "run"]
#WORKDIR /app
##ENV FLASK_RUN_HOST=127.0.0.1
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
#EXPOSE 5000
#EXPOSE 6379
#COPY . .
#CMD [ "python3", "-m" , "flask", "run"]