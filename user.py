from folders import Quiz, Response


class User:

	def __init__(self, name: str):
		self._name = name
		self._score = 0.0
		self._expected = 0.0

	@property
	def name(self) -> str:
		return self._name

	@name.setter
	def name(self, name: str):
		self._name = name

	@property
	def score(self) -> float:
		return self._score

	@property
	def expected(self) -> float:
		return self._expected

	def increase_score(self, value: float):
		self._score += value

	def increase_expected(self, value: float):
		self._expected += value

	def answer(self, quiz: Quiz, response_string: str):
		response = Response(response_string.strip())
		quiz.add(response)

	def __str__(self) -> str:
		return (
			"\033[97m"
			f"\t | USER NAME: {self._name}\n"
			f"\t | EXPECTED:  \033[94m{self._expected:.2f}\033[97m\n"
			f"\t | SCORE:     \033[5m{self._score:.2f}\n"
			"\033[0m"
		)
