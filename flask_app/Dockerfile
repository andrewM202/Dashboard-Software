FROM python:3
# FROM python:3.7-alpine

LABEL MAINTAINER="Andrew Matt <andrewm1246@gmail.com>"

ENV MONGODB_HOST="host.docker.internal" \
    #MONGODB_HOST="mongodb://127.0.0.1:27017/politic" \ 
    FLASK_DEBUG=1 \ 
    FLASK_ENV=development \ 
    MONGODB_DB="politic" \ 
    SECRET_KEY="V8wVHAQG5uGfY93UzARtHLV4FQ8RJsZLWnnkW9eoaWY"

RUN mkdir /app
WORKDIR /app

# Copy all files
COPY . /app
ADD . /app
COPY gunicorn.sh /app

RUN pip install -r requirements.txt

# ENTRYPOINT ["python", "./app.py"]
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "app:app"]
# CMD [ "python", "./app.py" ]
# CMD ["/bin/bash", "./gunicorn.sh"]