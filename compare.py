import os


class ScoringStringCompare:
	""" Token compare. """

	def __init__(self, min_chars: int = 2):
		self._min = min_chars
		pass

	def compare(self, pred: str , targ: str) -> float:
		""" Compare function of two string. """
		if not pred:
			return 0.0

		if not targ:
			return 1.0

		pred_len = len(pred)
		targ_len = len(targ)
		max_length = pred_len if pred_len > targ_len \
			else targ_len

		substr = ''
		sublen = 0
		index = -1
		count = 0
		score = 0.0
		for pos, char in enumerate(targ):
			substr += char
			if len(substr) >= self._min:
				try:
					index = pred.index(substr)
					# print(substr)
					count += 1
				except:
					if index != -1:
						sublen = len(substr)
						pred = pred.replace(pred[index:index+sublen], '')
						score += count
						index = -1

					substr = substr[-1]
					count = 1
			else:
				count += 1

		if index != -1:
			sublen = len(substr)
			pred = pred.replace(pred[index:index+sublen], '')
			score += count

		if max_length != 0.0:
			return score / max_length
		else:
			return 0.0


def main():
	target = 'Introvertie'
	predict = 'Instro'
	strcomp = ScoringStringCompare()
	score = strcomp.compare(predict, target)
	print("score =", score)


if __name__ == '__main__':
	try:
		main()
		os.sys.exit(0)
	except KeyboardInterrupt:
		os.sys.exit(125)
