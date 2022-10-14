from datetime import timedelta
from typing import Any

from flask import Flask
from flask_cors import CORS

from src.Config.RemoteConfig import RemoteConfig


def init_config(app: Flask) -> Any:
	CORS(app, supports_credentials=True)

	config: dict = RemoteConfig.load_whole()

	app.config["SECRET_KEY"] = config["SECRET_KEY"]
	# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=config["TLT"])
	app.host = config["HOST"]
	app.port = config["PORT"]

	return app
