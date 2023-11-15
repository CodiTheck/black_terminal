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

	def _find(self, search: Response, responses: List[Response]) -> Response:
		""" Function to find the corresponding response
				in a list of responses
		"""
		max_score = 0
		curr_score = 0
		response_found = None

		for response in responses:
			for char in search.content:
				try:
					response.content.index(char)
					curr_score += 1
				except:
					pass

			if curr_score > max_score:
				max_score = curr_score
				response_found = response

			curr_score = 0

		return response_found

	def _verify(self, proposition: Response, response: Response) -> float:
		""" Function of response verification """
		if not response.content:
			return 1.0

		if not proposition.content:
			return 0.0

		total_score = 0.0
		tokenizer = StringTokenizer()
		pred_tokens = tokenizer.tokenize(proposition.content)
		targ_tokens = tokenizer.tokenize(response.content)

		encoder = Str2IntEncoder(targ_tokens)
		pred_tokens = encoder.tokenize(pred_tokens)
		token_infos = encoder.get_token_infos()

		# propos = []
		# for token, score in token_infos:
		#		total_score += score
		#		propos.append(token)

		# n_infos = len(token_infos)
		# if n_infos > 0:
		#		total_score /= n_infos

		score = self._analyser.get_analysis(proposition.content, response.content)
		total_score = (total_score + score)

		# self._propositions.append(propos)
		# self._responses.append(targ_tokens)
		# print(propos)
		# print(targ_tokens)
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

		for preds, targs in zip(self._propositions, self._responses):
			output = '* '
			if not preds:
				output += (f"\033[95mNo response given!\033[0m\n")
				yield output
				continue

			for pred, targ in zip(preds, targs):

				res = analyzer.get_analysis(pred, targ)
				for index, char in enumerate(pred):
					if res[index]:
						output += (f"\033[92m{char}\033[0m")
					else:
						output += (f"\033[91m{char}\033[0m")

				yield output
				output = ''

			output = '\n'


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
