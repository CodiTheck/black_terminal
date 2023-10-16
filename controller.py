from typing import List
from folders import Response, Quiz, ResponsesList

from tokenization import StringTokenizer, Str2IntEncoder
from sequence import SequenceAnalyser
from analyzer import TokenAnalyzer


class Corrector:

	def __init__(self):
		self._is_valid = False
		self._responses = []
		# self._scores = []
		self._responses_ordered = False

		self._matchings = []
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

		print("true_response:", str(tokens1))
		print("given_response:", str(tokens2))

		encoder = Str2IntEncoder(tokens1)
		targ_seq, _ = encoder.tokenize(tokens1)
		pred_seq, info = encoder.tokenize(tokens2)

		print("true_response:", str(targ_seq))
		print("given_response:", str(pred_seq))
		print("INFO:", _)

		for token, score in info:
			total_score += score

		# delete foreign token:
		# pred_seq = [token for token in pred_seq if token != -1]

		analyser = SequenceAnalyser()
		res, matches = analyser.get_analysis(pred_seq, targ_seq)
		print(matches)

		for tag in res:
			if tag == 1:
				total_score += 1.0
			elif tag == 0:
				total_score += 0.25

		counts = len(targ_seq) + len(tokens2)
		return (
			encoder.tokens_map,
			tokens1,
			tokens2,
			matches,
			res,
			(total_score / counts), 
		)

	def correct(self, quiz: Quiz):
		if self._responses_ordered:
			given_and_true = zip(quiz.responses, self._responses)
			for index, (given_response, true_response) in enumerate(given_and_true):
				tmap, targ, pred, matches, res, score = self._correct_string(
					given_response.content,
					true_response.content,
				)
				quiz.increase_score(score)
				self._tokens.append(tmap)
				self._matchings.append(matches)
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
							tmap, targ, pred, matches, res, score = self._correct_string(
								given_response.content,
								true_response.content,
							)
							quiz.increase_score(score)
							self._tokens.append(tmap)
							self._matchings.append(matches)
							self._results.append(res)
							self._targ_sequences.append(targ)
							self._pred_sequences.append(pred)
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

	def get_analyse(self) -> str:
		output = ''
		analyzer = TokenAnalyzer()
		zipped_iter = zip(
			self._tokens,
			self._matchings,
			self._results,
			self._targ_sequences,
			self._pred_sequences,
		)
		for tmap, matches, res, pred, targ in zipped_iter:
			for index, tag in zip(matches, res):
				if tag == -2:
					output += '\033[91m'
					# output += '\033[4m'
					output += str(pred[-1*index])
					output += "\033[0m"
				elif tag == -1:
					output += '\033[96m'
					output += '_'
					output += '\033[0m'
				elif tag == 0:
					output += '\033[4m'
					targ_token = targ[index]
					analyzer.get_analysis()
				
				yield output
				output = ''

	def reset(self):
		self._responses.clear()
		self._scores.clear()
		self._pred_sequences.clear()
		self._targ_sequences.clear()
		self._results.clear()
		self._matchings.clear()
		self._tokens.clear()

	def valids(self) -> bool:
		return self._is_valid
