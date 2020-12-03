from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
# load env vars from .env file
load_dotenv()

from apps.users.views import router as users

app = Flask(__name__)
app.register_blueprint(users, url_prefix="/api/v1/users")
CORS(app)

if __name__ == '__main__':
    app.run(debug=False)
