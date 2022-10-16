import json

from flask import Blueprint, request, Response
from xfss.Auth import Auth
from xfss.HTTPStatus import RESOURCE_CREATED, OK, NOT_FOUND, NOT_ACCEPTABLE
from xfss.StatefulSession import StatefulSession

from src.Model.User import User

session_routes = Blueprint("session_routes", __name__)


@session_routes.post("/session")
@Auth.requires_payload({"email", "password"})
def new_session():
	user = User()
	user.email = request.json["email"]
	user.set_password(request.json["password"], True)
	if "role" in request.json:
		user.role = request.json["role"]

	token = StatefulSession.new_session(user.__dict__)

	return Response(
		json.dumps({"token": token}),
		status=RESOURCE_CREATED,
		mimetype="application/json"
	)


@session_routes.get("/session")
@StatefulSession.requires_token
def get_session():
	try:
		session_data = StatefulSession.get_data(request.headers.get("token"))
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


@session_routes.put("/session")
@StatefulSession.requires_token
def is_alive():
	return Response(status=OK)


@session_routes.patch("/session")
@StatefulSession.requires_token
def update_session():
	response = Response(status=NOT_ACCEPTABLE)
	new_data = None
	if request.json:
		new_data = StatefulSession.update_data(request.headers.get("token"), request.json)
	if new_data:
		response = Response(
			json.dumps(new_data),
			status=OK,
			mimetype="application/json"
		)
	return response


@session_routes.delete("/session")
@StatefulSession.requires_token
def delete_session():
	response = Response(status=NOT_FOUND)
	if StatefulSession.delete_session(request.headers.get("token")):
		response = Response(status=OK)
	return response
