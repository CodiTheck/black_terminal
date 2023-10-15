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

		number = self._counts[occ.value]
		if number == 1:
			return self._sequence.index(occ.value)
		else:
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

	def _is_ordered(self, seq: List[Any]) -> bool:
		current_value = seq[0]
		for i in range(1, len(seq)):
			if current_value >= seq[i]:
				return False

			current_value = seq[i]

		return True

	def get_analysis(self,
									 pred_tokens: List[Any],
									 targ_tokens: List[Any]) -> List[int]:

		pred_len = len(pred_tokens)
		targ_len = len(targ_tokens)

		pred_seq = Sequence(pred_tokens)
		targ_seq = Sequence(targ_tokens)

		pred_positions = []
		targ_positions = []
		pos = -1

		for index in range(targ_len):
			occ = targ_seq[index]
			pos = pred_seq.indexof(occ)
			if pos != -1:
				pred_positions.append(pos)
				targ_positions.append(index)

		corr_positions = sorted(pred_positions)

		results = [-1]*targ_len
		index = 0
		for targ_index in range(targ_len):
			if targ_index in targ_positions:
				index = targ_positions.index(targ_index)
				if pred_positions[index] == corr_positions[index]:
					results[targ_index] = 1
				else:
					results[targ_index] = 0

		return results


def test():
	targ_seq = [0, 2, 1, 1, 9, 2, 0, 2]
	pred_seq = [0, 3, 2, 2, 1, 0, 3]
	analyser = SequenceAnalyser()
	res = analyser.get_analysis(pred_seq, targ_seq)
	print(res)


if __name__ == '__main__':
	test()
