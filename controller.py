import os
from typing import List
from folders import Response, Quiz, ResponsesList, Question

from tokenization import StringTokenizer, Str2IntEncoder
from sequence import SequenceAnalyser
from analyzer import TokenAnalyzer


class Corrector:

	def __init__(self):
		self._is_valid = False
		self._responses = []
		# self._scores = []
		self._responses_ordered = False

		self._results = []
		self._tokens = []
		self._targ_sequences = []
		self._pred_sequences = []

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

	def _correct_string(self, pred_string: str, targ_string: str) -> float:
		total_score = 0.0
		counts = 0

		tokenizer = StringTokenizer()
		tokens1 = tokenizer.tokenize(targ_string)
		tokens2 = tokenizer.tokenize(pred_string)

		# print("true_response:", str(tokens1))
		# print("given_response:", str(tokens2))

		encoder = Str2IntEncoder(tokens1)
		targ_seq, _ = encoder.tokenize(tokens1)
		pred_seq, info = encoder.tokenize(tokens2)

		# print("true_response:", str(targ_seq))
		# print("given_response:", str(pred_seq))
		# print("INFO:", _)

		for token, score in info:
			total_score += score

		# delete foreign token:
		# pred_seq = [token for token in pred_seq if token != -1]

		analyser = SequenceAnalyser()
		res = analyser.get_analysis(pred_seq, targ_seq)
		# print(res)

		for tag in res.tags:
			if tag == 1:
				total_score += 1.0
			elif tag == 0:
				total_score += 0.25

		counts = len(targ_seq) + len(tokens2)
		return (
			encoder.tokens_map,
			tokens1,
			tokens2,
			res,
			(total_score / counts),
		)

	def correct(self, quiz: Quiz):
		if self._responses_ordered:
			given_and_true = zip(quiz.responses, self._responses)
			for index, (given_response, true_response) in enumerate(given_and_true):
				tmap, targ, pred, res, score = self._correct_string(
					given_response.content,
					true_response.content,
				)
				quiz.increase_score(score)
				self._tokens.append(tmap)
				self._results.append(res)
				self._targ_sequences.append(targ)
				self._pred_sequences.append(pred)
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
							tmap, targ, pred, res, score = self._correct_string(
								given_response.content,
								true_response.content,
							)
							quiz.increase_score(score)
							self._tokens.append(tmap)
							self._results.append(res)
							self._targ_sequences.append(targ)
							self._pred_sequences.append(pred)
							responses_already_seen.append(given_response)

	def get_analysis(self) -> str:
		output = ''
		analyzer = TokenAnalyzer()
		zipped_iter = zip(
			self._tokens,
			self._results,
			self._pred_sequences,
			self._targ_sequences,
		)
		for tmap, res, pred, targ in zipped_iter:
			if not pred:
				output += '\033[95mNo comment!\033[0m'
				output += '\n'
				yield output

				output = ''
				continue

			result_iterator = zip(res.tags, res.pred_index, res.targ_index)
			# print('pred: ', len(pred))
			# print('targ: ', len(targ))
			for tag, pred_index, targ_index in result_iterator:
				if tag == -2:
					output += '\033[91m'
					# output += '\033[4m'
					output += str(pred[-1*pred_index])
					output += "\033[0m"
				elif tag == -1:
					output += '\033[96m'
					output += str(targ[-1*targ_index])
					output += '\033[0m'
				elif tag == 0 or tag == 1:
					if tag == 0:
						output += '\033[4m'

					pred_token = pred[pred_index]
					targ_token = targ[targ_index]
					# print('pred_index:', pred_index)
					# print('targ_index:', targ_index)

					result = analyzer.get_analysis(pred_token, targ_token)
					# print(result)

					for index, char in enumerate(pred_token):
						if result[index]:
							output += f"\033[92m{char}\033[0m"
						else:
							output += f"\033[91m{char}\033[0m"

					output += '\033[0m'

				yield output
				output = ''

			output += '\n'

		yield output

	def reset(self):
		self._responses.clear()
		self._pred_sequences.clear()
		self._targ_sequences.clear()
		self._results.clear()
		self._tokens.clear()

	def valids(self) -> bool:
		return self._is_valid


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

	quiz = Quiz(question, 1)
	quiz.add(pred_response)

	# instanciation of the corrector:
	corrector = Corrector()
	corrector.true_responses = true_responses_list

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
