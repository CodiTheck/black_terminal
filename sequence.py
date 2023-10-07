from dataclasses import dataclass
from typing import List, Dict, Tuple, Any
# from collections import Counter


class PositionalEncoding:

	def __init__(self):
		self._pe = []

	def predict(self, sequence: List[Any]) -> List[int]:
		tokens = []
		for word in sequence:
			try:
				index = self._tokens.index(word)
				tokens.append(index)
			except ValueError:
				tokens.append(-1)
		
		return tokens


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
