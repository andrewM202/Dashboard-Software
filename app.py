from flask import Flask, send_from_directory
from config import Config
import random

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Can remove this /admin/dashboard path in production, only needed
# For development so don't need to go back to root / path with 
# javascript changes to be served files
@app.route("/admin/dashboard")
def dashboard():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))

if __name__ == "__main__":
    app.run()