import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Any
# from collections import Counter


class PositionalEncoding:

	def __init__(self, max_length: int):
		self._max_length = max_length
		self._pe = [0] * max_length

		pos = list(range(max_length))
		e2i = math.exp(-1 * math.log(10_000.0))

		alpha = self._mul(e2i, pos)
		pesin = self._apply(math.sin, alpha)
		pecos = self._apply(math.cos, alpha)

		for index in range(0, max_length, 2):
			self._pe[index] = pesin[index]

		for index in range(1, max_length, 2):
			self._pe[index] = pecos[index]

	def _mul(self, a: float, v: list) -> list:
		return [a*x for x in v]

	def _apply(self, f, v: list) -> list:
		return [f(x) for x in v]

	def predict(self, sequence: List[int]) -> List[float]:
		seq_length = len(sequence)
		if seq_length >= self._max_length:
			raise ValueError("Sequence in of max length.")

		return [self._pe[pos] + sequence[pos] for pos in range(seq_length)]


class SequenceAnalyser:
	""" Sequence Analyser """

	@dataclass
	class TokenAnalysis:
		predicted_position: int
		target_position: int
		verified_position: bool

	# def _punctuation_tokenize(self, string: str) -> List[str]:
	# 	""" Return a list of string tokined with punctuation tokenization method."""
	# 	return string.split(' ')

	def _sequence_identify(self,
												 sequence1: List[Any],
												 sequence2: List[Any]) -> Dict[int, str]:
		sequence_dict = {pos:element for pos, element in enumerate(sequence1)}
		for element in sequence2:
			sequence_dict[len(sequence_dict)] = element

		return sequence_dict

	def get_analysis(self,
									 pred_tokens: List[Any],
									 target_tokens: List[Any]) -> Dict[Any, TokenAnalysis]:

		result = {}
		pred_pos = -1
		for target_pos, pos_token in enumerate(target_tokens):
			analysis = self.TokenAnalysis()
			try:
				pred_pos = pred_tokens.index(pos_token)
			except ValueError:
				analysis.predicted_position = -1
				analysis.target_position = target_pos
				analysis.verified_position = False

			if pred_pos == target_pos:
				result[pos_token].append((-1, target_pos, False))
				analysis.predicted_position = pred_pos
				analysis.target_position = target_pos
				analysis.verified_position = True

			if pos_token not in result:
				result[pos_token] = []

			result[pos_token].append(analysis)


def test():
	pe = PositionalEncoding(10000)
	seq = list(range(100)) + list(range(100))
	seq_enc = pe.predict(seq)
	print(seq_enc)
	print(len(seq_enc) == len(set(seq_enc)))


if __name__ == '__main__':
	test()
