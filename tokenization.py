import os
from abc import ABC, abstractclassmethod
from typing import List, Any

from compare import ScoringStringCompare


class Tokenizer(ABC):

	@abstractclassmethod
	def tokenize(self, string: str) -> List[Any]:
		""" Function that is used to tokenize a string sequence. """
		pass


class StringTokenizer(Tokenizer):
	""" This class allows to tokenize a string sequence. """

	def tokenize(self, string: str) -> List[str]:
		""" Function of tokenization. """
		return string.split(" ")


class Str2IntEncoder(Tokenizer):

	def __init__(self, base: List[str], alpha: float = 0.55):
		super().__init__()
		self._alpha = alpha
		self._base_tokens = list(set(base))
		self._str_compare = ScoringStringCompare()
		# print(f"\033[92m{self._base_tokens}\033[0m")

	def _get_max_score_and_index(self, token: str) -> int:
		max_score = self._str_compare.compare(token, self._base_tokens[0])
		max_index = 0

		score = 0
		for index_ref, token_ref in enumerate(self._base_tokens[1:]):
			score = self._str_compare.compare(token, token_ref)
			if score > max_score:
				max_score = score
				max_index = index_ref + 1

		return max_score, max_index

	def tokenize(self, tokens_seq: List[str]) -> List[int]:
		if not self._base_tokens:
			raise ValueError("Base tokens must be a list of strings.")

		ints_seq = [-1]*len(tokens_seq)
		tokens_info = []
		max_index = 0
		max_score = 0.0

		for index, token in enumerate(tokens_seq):
			max_score, max_index = self._get_max_score_and_index(token)
			if max_score >= self._alpha:
				ints_seq[index] = max_index
				tokens_info.append((token, max_score))

		return ints_seq, tokens_info


def main():
	try:
		true_response = "Un pointeur est une variable qui permet de stocker l'adresse mémoire d'une autre variable."
		given_response = "Un pointeur est une variable qui stocke l'adresse d'autres variables"

		tokenizer = StringTokenizer()
		tokens1 = tokenizer.tokenize(true_response)
		tokens2 = tokenizer.tokenize(given_response)

		print("true_response:", str(tokens1))
		print("given_response:", str(tokens2))

		encoder = Str2IntEncoder(tokens1)
		tokens1, _ = encoder.tokenize(tokens1)
		tokens2, _ = encoder.tokenize(tokens2)

		print("true_response:", str(tokens1))
		print("given_response:", str(tokens2))
		print("INFO:", _)

		os.sys.exit(0)
	except KeyboardInterrupt:
		print("\033[91mCanceled by user.\033[0m")
		os.sys.exit(125)

if __name__ == '__main__':
	main()
