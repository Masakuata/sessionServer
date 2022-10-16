from typing import Any

from werkzeug.security import generate_password_hash, check_password_hash


class User:
	def __init__(self):
		self.email: str or None = None
		self.password: str or None = None
		self.role: Any = None

	def set_password(self, password: str, clean: bool = False) -> None:
		if clean:
			self.password = password
		else:
			self.password = generate_password_hash(password)

	@staticmethod
	def check_password(hashed: str, clean: str) -> bool:
		return check_password_hash(hashed, clean)
