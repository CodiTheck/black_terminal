import os


class Quiz:

	def __init__(self,
							 question: str,
							 answer: str,
							 answers_count: int = None,
							 ordered: bool = False):

		self._question = question
		self._answer = answer
		self._answers_count = answers_count
		self._ordered = ordered

		self._scores = []
		self._answers = []
		self._answered = []
		self._completed = False

		if answers_count == 1:
			self._scores = [1.0]
			self._answers = [answer]

	@property
	def completed(self) -> bool:
		return self._completed
	
	@property
	def ordered(self) -> bool:
		return self._ordered

	def __len__(self) -> int:
		return len(self._answers)

	def __str__(self) -> str:
		return self._question


class Paper:

	def __init__(self, file_path):
		if not os.path.isfile(file_path):
			raise FileNotFoundError(
				f"This file is not found at this path: {file_path}"
			)

		self.content = ''
		with open(file_path, 'r', encoding='utf-8') as file:
			self._content = file.read()

		self._questions = []
		self._answers = []
		self._parse_file()

		if len(self._questions) != len(self._answers):
			raise ValueError(
				f"Some questions have not answer."
			)

	@property
	def content(self) -> str:
		return self._content

	def _parse_file(self):
		question = ''
		answer = ''
		token = ''

		isquestion = False
		isanswer = False

		for character in self._content:
			if character == '[':
				if isquestion:
					isquestion = False
					self._questions.append(question.strip())
					question = ''

				if isanswer:
					isanswer = False
					self._answers.append(answer.strip())
					answer = ''

				continue

			if not isquestion and not isanswer:
				token += character
				continue

			if character == ']':
				token = ''
				if token.upper() == 'QUESTION':
					isquestion = True
				elif token.upper() == 'ANSWER':
					isanswer = True

				continue

			if isquestion:
				question += character

			if isanswer:
				answer += character

	def __len__(self) -> int:
		return len(self._questions)

	def __getitem__(self, index) -> Quiz:
		return Quiz(question=self._questions[index], answer=self._answers[index])

	def __str__(self) -> str:
		questions = ""
		for index, question in enumerate(self._questions):
			questions += str(index + 1) + ". " + question + "\n"

		return questions


class Folder:

	def __init__(self, dir_path: str):
		if not os.path.isdir(dir_path):
			raise FileNotFoundError(
				f"This folder is not found at this path: {dir_path}"
			)

		self._dir_path = dir_path
		self._file_names = os.listdir(dir_path)

	def __len__(self) -> int:
		return len(self._file_names)

	def __getitem__(self, index) -> Paper:
		file_path = os.path.join(self._dir_path, self._file_names[index])
		return Paper(file_path)
