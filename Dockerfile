FROM python:3.8-slim-buster
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
# Specify the Flask environment port
ENV PORT 5000

# By default, listen on port 5000
EXPOSE 5000
CMD [ "python3", "app.py" , "--host", "0.0.0.0"]