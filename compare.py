

class ScoringStringCompare:
	""" Token compare. """

	def __init__(self):
		pass

	def compare(self, string1: str , string2: str) -> float:
		""" Compare function of two string. """
		string_length1 = len(string1)
		string_length2 = len(string2)
		max_length = string_length1 if string_length1 > string_length2 \
			else string_length2

		score = 0.0
		for character1, character2 in zip(string1, string2):
			if character1 == character2:
				score += 1

		if max_length != 0.0:
			return score / max_length
		else:
			return 0.0
