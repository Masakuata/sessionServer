import json

from flask import Blueprint, request, Response
from xf_auth.Auth import Auth
from xf_auth.HTTPStatus import RESOURCE_CREATED, OK, NOT_FOUND
from xf_auth.StatefulSession import StatefulSession

from src.Model.User import User

session_routes = Blueprint("session_routes", __name__)


@session_routes.post("/session")
@Auth.requires_payload({"email", "password", "role"})
def new_session():
	user = User()
	user.email = request.json["email"]
	user.set_password(request.json["password"], True)
	user.role = request.json["role"]

	token = StatefulSession.new_session(user.__dict__)

	return Response(
		json.dumps({"token": token}),
		status=RESOURCE_CREATED,
		mimetype="application/json"
	)


@session_routes.get("/session")
@Auth.requires_payload({"token"})
def get_session():
	try:
		session_data = StatefulSession.get_data(request.json["token"])
	except TypeError:
		session_data = None

	if session_data is not None:
		response = Response(
			json.dumps(session_data),
			status=OK,
			mimetype="application/json"
		)
	else:
		response = Response(status=NOT_FOUND)
	return response
