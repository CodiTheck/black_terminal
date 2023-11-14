import os
from typing import List
from folders import Response, Quiz, ResponsesList, Question

from tokenization import StringTokenizer, Str2IntEncoder
from sequence import SequenceAnalyser
from analyzer import TokenAnalyzer, SementicAnalyser


class Corrector:

	def __init__(self):
		self._propositions = []
		self._responses = []
		self._analyser = SementicAnalyser()

	def _find(self) -> Response:
		...

	def _verify(self, proposition: Response, response: Response) -> float:
		""" Function of response verification """
		total_score = 0.0
		tokenizer = StringTokenizer()
		pred_tokens = tokenizer.tokenize(proposition.content)
		targ_tokens = tokenizer.tokenize(response.content)

		encoder = Str2IntEncoder(targ_tokens)
		pred_tokens = encoder.tokenize(pred_tokens)
		token_infos = encoder.get_token_infos()

		propos = []
		for token, score in token_infos:
			total_score += score
			propos.append(token)

		total_score /= len(token_infos)

		score = self._analyser.get_analysis(proposition.content, response.content)
		total_score = (total_score + score) / 2

		self._propositions.append(propos)
		self._responses.append(targ_tokens)
		return total_score

	def correct(self, quiz: Quiz):
		""" Function of quiz correction """
		if quiz.ordered:
			iterator = zip(quiz.propositions, quiz.responses)
			for proposition, response in iterator:
				score = self._verify(proposition, response)
				quiz.increase_score(score)
		else:
			responses = quiz.responses[:]
			for proposition in quiz.propositions:
				response = self._find(proposition, responses)
				if response:
					responses.remove(response)
					score = self._verify(proposition, response)
					quiz.increase_score(score)


	def get_analysis(self) -> str:
		""" Function that makes analysis and return results like strings """
		output = ''
		analyzer = TokenAnalyzer()

		for pred, targ in zip(self._propositions, self._responses):
			res = analyzer.get_analysis(pred, targ)
			for index, char in enumerate(pred):
				if res[index]:
					output += (f"\033[92m{char}\033[0m")
				else:
					output += (f"\033[91m{char}\033[0m")

			yield output
			output = ''


	def reset(self):
		""" Function of controller reset """
		self._propositions.clear()
		self._responses.clear()


def main():
	""" Main function. """
	question = Question("Definie les pointeurs.")
	# print(f"Question: {question}")
	true_responses_list = ResponsesList(responses_list=[
		"Un pointeurs est une variable qui permet de stocker l'adresse mémoire d'une autre variable."
	])
	# print(f"TrueResponse: {true_responses_list}")
	pred_response = Response(
		"Un pointeurs sert à stocker l'adresse mémoire d'autres variables."
	)
	# print(f"PredResponse: {pred_response}")

	quiz = Quiz(question, true_responses_list, ['txt'])
	quiz.add(pred_response)

	# instanciation of the corrector:
	corrector = Corrector()

	corrector.correct(quiz)
	print("Score got: ", quiz.score)

	correction_iterator = corrector.get_analysis()
	for message in correction_iterator:
		print(message, end=' ')


if __name__ == '__main__':
	try:
		main()
		os.sys.exit(0)
	except KeyboardInterrupt:
		print("Canceled by user.")
		os.sys.exit(125)
