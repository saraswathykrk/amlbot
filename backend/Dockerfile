FROM rasa/rasa:1.10.0-full

WORKDIR /app
COPY . /app
COPY ./data /app/data

RUN  rasa train

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD [ "run","-m","/app/models","--enable-api","--endpoints","endpoints.yml","--credentials","credentials.yml","--cors","*","--debug" ]