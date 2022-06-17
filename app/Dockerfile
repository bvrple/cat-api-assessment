FROM python:3.6
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
RUN adduser -D myuser
USER myuser
CMD gunicorn --bind 0.0.0.0:$PORT wsgi