

class ScoringStringCompare:
	""" Token compare. """

	def __init__(self):
		# self._min = min_chars
		pass

	def compare(self, pred: str , targ: str) -> float:
		""" Compare function of two string. """
		pred_len = len(pred)
		targ_len = len(targ)
		max_length = pred_len if pred_len > targ_len \
			else targ_len

		substr = targ
		score = 0.0
		while substr != '':
			try:
				pred.index(substr)
				score = float(len(substr))
				break
			except ValueError:
				substr = substr[:-1]

		if max_length != 0.0:
			return score / max_length
		else:
			return 0.0
