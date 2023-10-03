

class User:
	
	def __init__(self, name: str):
		self._name = name
		self._score = 0.0

	@property
	def name(self) -> str:
		return self._name

	@name.setter
	def name(self, name: str):
		self._name = name

	@property
	def score(self) -> float:
		return self._score

	def increase_score(self, value: float):
		self._score += value

	def __str__(self) -> str:
		return (
			f"user name: {self._name}\n"
			f"score:     {self._score:.2f}\n"
		)
