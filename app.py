# File name:app.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module is used to start the app

import config
from client.routes import client_blueprint
from api.routes import api_blueprint
from config import db
import api.init_challenges

# apply the configuration settings from config file
app = config.app

# flask blueprints are used to seperate the client routes from the app routes
# register the client blueprint
app.register_blueprint(client_blueprint)

# register the api blueprint
app.register_blueprint(api_blueprint)


# set headers to disable caching, and prevent clickjacking
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['X-Frame-Options'] = 'Deny'
    return response


if __name__ == "__main__":
    with app.app_context():
        # when the app starts populate the db.
        db.create_all()
        api.init_challenges.setup()
    app.run(host="0.0.0.0", port=8000, debug=True)
    #  change the host to match the IP of your machine
