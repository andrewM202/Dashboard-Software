FROM python:3.9.7
# FROM python:3.7-alpine

# Put label maintainer so everyone knows who built it!
LABEL MAINTAINER="Andrew Matt <andrewm1246@gmail.com>"

# Set environment variables
# host.docker.internal instead of localhost
ENV MONGODB_HOST="mongodb://host.docker.internal:27017/politic" \
    #MONGODB_HOST="mongodb://127.0.0.1:27017/politic" \ 
    FLASK_DEBUG=1 \ 
    FLASK_ENV=development \ 
    MONGODB_DB="politic" \ 
    SECRET_KEY="V8wVHAQG5uGfY93UzARtHLV4FQ8RJsZLWnnkW9eoaWY"

# Lets make an app directory in the container to hold our files
RUN mkdir /app
WORKDIR /app

# Copy all files into our app working directory
COPY . /app
ADD . /app

# Install our requirements.txt
RUN pip install -r requirements.txt

# ENTRYPOINT ["python", "./app.py"]
# Run our gunicorn web server
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "app:app", "--reload"]
# CMD [ "python", "./app.py" ]