"""
Web Server using Flask
Author: Maheshwar
"""
from flask import Flask
app = Flask(__name__)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'App is Running'

if __name__ == "__main__":
    print "Starting the server"
    app.run()
