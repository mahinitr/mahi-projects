from flask import Flask
import os
import logging
import logging.config
from log import getLogger

app = Flask(__name__)
app.logger_name = "pushkar"
logging_cfg = "\opt\pushkar\logging.cfg"

@app.route("/")
def home():
	return "Welcome to Pushkar!"


if __name__ == '__main__':
	logging.config.fileConfig(logging_cfg, disable_existing_loggers=False)
	app.logger.info("Starting Pushkar WebApp")
	app.run()