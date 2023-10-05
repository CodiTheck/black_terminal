from typing import List
from folders import Response, Quiz, ResponsesList


class Corrector:

	def __init__(self):
		self._is_valid = False
		self._responses = []
		# self._scores = []
		self._responses_ordered = False

	@property
	def true_responses(self) -> ResponsesList:
		return self._responses

	@true_responses.setter
	def true_responses(self, responses: ResponsesList):
		self._responses.clear()
		# self._scores.clear()

		# self._scores.extend([1.0] * len(responses))
		self._responses.extend(responses.items())
		self._responses_ordered = responses.ordered

	def define_score(self, score: float, at: int):
		# self._scores[at] = score
		pass

	def define_scores(self, scores: List[float]):
		for index, score in enumerate(scores):
			self.define_score(score, at=index)

	def _compare_score(self, string1: str, string2: str) -> float:
		string_length1 = len(string1)
		string_length2 = len(string2)
		max_length = string_length1 if string_length1 > string_length2 \
			else string_length2

		score = 0
		for character1, character2 in zip(string1, string2):
			if character1 == character2:
				score += 1

		if max_length != 0.0:
			return score / max_length
		else:
			return 0.0

	def _find_true_response(self, response: str) -> int:
		max_score = self._compare_score(self._responses[0].content, response.content)
		index_candidate = None if max_score == 0.0 else 0

		true_responses_length = len(self._responses)
		for index in range(1, true_responses_length):
			score = self._compare_score(self._responses[index].content, response.content)
			if score > max_score:
				max_score = score
				index_candidate = index

		return index_candidate

	def correct(self, quiz: Quiz):
		if self._responses_ordered:
			given_and_true = zip(quiz.responses, self._responses)
			for index, (given_response, true_response) in enumerate(given_and_true):
				if given_response == true_response:
					quiz.increase_score(1.0)
				else:
					quiz.increase_score(
						self._compare_score(
							given_response.content,
							true_response.content,
						)
					)
		else:
			responses_already_seen = []
			for given_response in quiz.responses:
				if given_response not in responses_already_seen:
					if given_response in self._responses:
						quiz.increase_score(1.0)
						responses_already_seen.append(given_response)
					else:
						index = self._find_true_response(given_response)
						if index is not None:
							true_response = self._responses[index]
							score = self._compare_score(
								given_response.content,
								true_response.content,
							)
							quiz.increase_score(score)
							responses_already_seen.append(given_response)

	def _get_string_analysis(self, string1: str, string2: str) -> str:
		string_length1 = len(string1)
		string_length2 = len(string2)
		result = ''

		for character1, character2 in zip(string1, string2):
			if character1 == character2:
				result += f"\033[92m{character1}\033[0m"
			else:
				result += f"\033[91m{character2}\033[0m"

		return result

	def get_analyse(self, quiz) -> str:
		result = ''

		if self._responses_ordered:
			given_and_true = zip(quiz.responses, self._responses)
			for index, (given_response, true_response) in enumerate(given_and_true):
				if given_response == true_response:
					result += "\033[92m"
					# result += f"{index + 1}." + str(given_response) + "\n"
					result += f"{index + 1}."
					result += self._get_string_analysis(
						true_response.content,
						given_response.content,
					) + "\n"
				else:
					result += "\033[91m"
					result += f"{index + 1}." + str(given_response) + "\n"

				result += "\033[0m"
		else:
			responses_already_seen = []
			for given_response in quiz.responses:
				if given_response not in responses_already_seen \
					and given_response in self._responses:

					result += "\033[92m"
					result += "*" + str(given_response) + "\n"
					result += "\033[0m"
				else:
					index = self._find_true_response(given_response)
					if index is not None:
						true_response = self._responses[index]
						result += self._get_string_analysis(
							true_response.content,
							given_response.content,
						) + "\n"
					else:
						if given_response.content:
							result += "\033[91m"
							result += "* " + str(given_response) + "\n"
							result += "\033[0m"
						else:
							result += "\033[95m"
							result += "You didn't answer!\n"
							result += "\033[0m"

			return result

	def reset(self):
		self._responses.clear()
		self._scores.clear()

	def valids(self) -> bool:
		return self._is_valid
