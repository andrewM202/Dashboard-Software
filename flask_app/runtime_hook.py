# This file sets the environment variables for pyinstaller

from os import environ 

environ["MONGODB_HOST"]="mongodb://127.0.0.1:27017/politic"
environ["FLASK_DEBUG"]="1"
environ["FLASK_ENV"]="development"
environ["MONGODB_DB"]="politic"
environ["SECRET_KEY"]="V8wVHAQG5uGfY93UzARtHLV4FQ8RJsZLWnnkW9eoaWY"
environ["FLASK_HOST"]="127.0.0.1"