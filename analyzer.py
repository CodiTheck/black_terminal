import os
from abc import ABC, abstractmethod
from typing import Any, List


class Analyzer(ABC):

	@abstractmethod
	def get_analysis(self, pred: Any, target: Any) -> Any:
		pass


class TokenAnalyzer(Analyzer):

	def __init__(self):
		super().__init__()

	def get_analysis(self, pred: str, targ: str) -> List[bool]:
		pred_len = len(pred)
		# targ_len = len(targ)

		results = [False]*pred_len
		substr = targ
		while substr != '':
			try:
				pos = pred.index(substr)
				for index in range(len(substr)):
					results[index + pos] = True

				break
			except ValueError:
				substr = substr[:-1]

		return results


def main():
	try:
		targ_seq = "autre"
		pred_seq = "d'autres"
		analyzer = TokenAnalyzer()
		res = analyzer.get_analysis(pred_seq, targ_seq)
		print(res)

		print(targ_seq)
		for index, char in enumerate(pred_seq):
			if res[index]:
				print(f"\033[92m{char}\033[0m", end='')
			else:
				print(f"\033[91m{char}\033[0m", end='')

		print()

		os.sys.exit(0)
	except KeyboardInterrupt:
		print("\033[91mCanceled by user.\033[0m")
		os.sys.exit(125)


if __name__ == '__main__':
	main()
