import xfss
from flask import Blueprint, Response, request
from xfss.Auth import Auth
from xfss.HTTPStatus import OK, FORBIDDEN, NOT_FOUND, NOT_ACCEPTABLE
from xfss.StatefulSession import StatefulSession

requirements_routes = Blueprint("requirements_routes", __name__)


@requirements_routes.get("/requires_token")
@StatefulSession.requires_token
def requires_token():
	return Response(status=OK)


@requirements_routes.get("/requires_role")
@xfss.requires_payload({"role"})
@StatefulSession.requires_token
def requires_role():
	role = request.json["role"]
	session = StatefulSession.get_session(request.headers.get("token"))
	if session is not None:
		if type(role) == str:
			if session["data"][Auth.role_attribute] == role:
				response = Response(status=OK)
			else:
				response = Response(status=FORBIDDEN)
		elif type(role) == list:
			if session["data"][Auth.role_attribute] in role:
				response = Response(status=OK)
			else:
				response = Response(status=FORBIDDEN)
		else:
			response = Response(status=NOT_ACCEPTABLE)
	else:
		response = Response(status=NOT_FOUND)
	return response
