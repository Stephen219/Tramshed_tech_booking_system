import os
from flask import Flask
app = Flask(__name__)
ALLOWED_EXTENSIONS = set('txt','pdf','jpg','jpeg','gif' )


if __name__ == "__main__":
    app.run(debug=True)