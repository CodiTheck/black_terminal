import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Any
# from collections import Counter

'''
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
'''


class Sequence:

	@dataclass
	class Occurrence:
		value: Any
		number: int

	def __init__(self, seq: List[Any]):
		self._sequence = []
		self._numbers = []
		self._counts = {}

		for x in seq:
			self._sequence.append(x)
			if x in self._counts:
				self._counts[x] += 1
				self._numbers.append(self._counts[x])
			else:
				self._counts[x] = 1
				self._numbers.append(1)

	def indexof(self, occ: Occurrence) -> int:
		if occ.value not in self._counts:
			return -1

		# number = self._counts[occ.value]
		# if number == 1:
		# 	return self._sequence.index(occ.value)
		# else:
		for index, (value, number) in enumerate(zip(self._sequence,
																								self._numbers)):
			if occ.value == value and occ.number == number:
				return index

		return -1

	def __len__(self) -> int:
		return len(self._sequence)

	def __getitem__(self, index: int) -> Occurrence:
		occ = self.Occurrence(None, -1)
		occ.value = self._sequence[index]
		occ.number = self._numbers[index]
		return occ


class SequenceAnalyser:
	""" Sequence Analyser """

	@dataclass
	class Result:
		tags: List[int]  # contains the target value as -2, -1, 0, 1.
		targ_index: List[int]  # contains the indexes of targeted tokens.
		pred_index: List[int]  # contains the indexes of predicted tokens.

		def __str__(self) -> str:
			return (
				f"TAG:    {len(self.tags):4d} {str(self.tags)}\n"
				f"TARGET: {len(self.targ_index):4d} {str(self.targ_index)}\n"
				f"PREDIC: {len(self.pred_index):4d} {str(self.pred_index)}\n"
			)

	def _is_ordered(self, seq: List[Any]) -> bool:
		current_value = seq[0]
		for i in range(1, len(seq)):
			if current_value >= seq[i]:
				return False

			current_value = seq[i]

		return True

	def get_analysis(self,
									 pred_tokens: List[Any],
									 targ_tokens: List[Any]) -> 'Result':

		pred_len = len(pred_tokens)
		targ_len = len(targ_tokens)

		pred_seq = Sequence(pred_tokens)
		targ_seq = Sequence(targ_tokens)

		results = []
		matching = []
		result = self.Result([], [], [])

		pos = -1
		max_pos = -1

		for index in range(pred_len):
			pred = pred_seq[index]
			pos = targ_seq.indexof(pred)
			if pos != -1:
				if pos > max_pos:
					result.tags.append(1)
					max_pos = pos
				else:
					result.tags.append(0)

				result.targ_index.append(pos)
				result.pred_index.append(index)
			else:
				result.tags.append(-2)
				result.targ_index.append(-1*index)
				result.pred_index.append(-1*index)

		# print(result.tags)
		for targ_index in range(targ_len):
			if targ_index not in result.targ_index:
				pos = -1
				for index, targ_position in enumerate(result.targ_index):
					if targ_position > targ_index:
						pos = index
						break

				if pos != -1:
					# results.insert(pos, -1)
					result.tags.insert(pos, -1)
					# matching.insert(pos, -1*targ_index)
					result.targ_index.insert(pos, -1*targ_index)
					result.pred_index.insert(pos, -1*targ_index)
				else:
					# results.append(-1)
					result.tags.append(-1)
					# matching.append(-1*targ_index)
					result.targ_index.append(-1*targ_index)
					result.pred_index.append(-1*targ_index)

		return result


def test():
	targ_seq = [7, 2, 1, 1, 9, 8, 2, 0, 2, 8]
	pred_seq = [7, 3, 2, 2, 1, 0, 3, 9, 2, 1]
	analyser = SequenceAnalyser()
	res = analyser.get_analysis(pred_seq, targ_seq)
	print(res)


if __name__ == '__main__':
	test()
