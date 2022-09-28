FROM python:3.8-slim-buster

EXPOSE 5000
WORKDIR /src

# development configuration
ENV FLASK_APP="app.py:app"
ENV FLASK_ENV="development"
ENV FLASK_DEBUG = 1

# setup python enviroment
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# copy source code
COPY src/ .

# run application
CMD ["flask", "run", "--host=0.0.0.0"]
