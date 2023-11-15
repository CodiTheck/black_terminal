import re
import json
import os
import random
from typing import List, Tuple


class Question:

	def __init__(self, content: str):
		self._content = content

	@property
	def content(self) -> str:
		return self._content

	def __str__(self) -> str:
		return self._content


class Response:

	def __init__(self, content: str):
		self._content = content

	@property
	def content(self) -> str:
		return self._content

	def __eq__(self, response: 'Response') -> bool:
		""" If the content text of this response is equal to
				the content text of another response then we return
				True, otherwise, False will be returned.
		"""
		# print()
		# print(self._content)
		# print(response.content)
		# print(self._content == response.content)
		return self._content == response.content

	def __str__(self) -> str:
		return self._content


class ResponsesList:

	def __init__(self,
							 string: str = '',
							 responses_list: List[str] = [],
							 ordered: bool = False):
		self._responses = []
		self._ordered = ordered

		responses = []
		if string:
			responses = re.split('\n\n+', string)
		elif responses_list:
			responses = responses_list

		for response in responses:
			response = response.replace('\n', ' ')
			response = response.strip()
			self._responses.append(Response(response))

	@property
	def ordered(self) -> bool:
		""" Returns True if the responses must be ordered """
		return self._ordered

	def __len__(self):
		return len(self._responses)

	def __contains__(self, response: Response):
		return response in self._responses

	def __getitem__(self, index: int) -> Response:
		return self._responses[index]

	def items(self) -> List[Response]:
		return self._responses

	def __str__(self) -> str:
		response_string = ''
		for index, response in enumerate(self._responses):
			if self._ordered:
				response_string += f"{index + 1}. "
			else:
				response_string += "* "

			response_string += f"{response}\n"

		return response_string


class Quiz:

	def __init__(self,
							 question: Question,
							 responses: ResponsesList,
							 response_types: List[str],
							 transition: str = '',
							 ordered: bool = False):

		self._question = question
		self._transition = transition
		self._responses = responses
		self._response_types = response_types
		self._ordered = ordered

		self._propositions = []
		self._score = 0.0
		self._length = len(responses) + (1 if transition else 0)
		self._expected = float(self._length)

	@property
	def score(self) -> float:
		""" Returns the the score value """
		return self._score

	@property
	def accuracy_score(self) -> float:
		""" Returns the score like purcentage """
		return self._score * 100.0 / self._expected if self._expected else 100.0

	@property
	def transition(self) -> str:
		""" Returns the transition of this quiz """
		return self._transition

	@property
	def responses(self) -> ResponsesList:
		""" Returns the list of responses class """
		return self._responses

	@property
	def response_types(self) -> List[str]:
		""" Returns the list of response types """
		return self._response_types

	@property
	def propositions(self) -> List[Response]:
		return self._propositions

	@property
	def ordered(self) -> bool:
		""" Returns True if the answsers must be ordered """
		return self._ordered

	@property
	def expected(self) -> float:
		""" Returns the expected score """
		return self._expected

	@property
	def completed(self) -> bool:
		""" Returns True, if all the questions
				of this quiz have a response. ie the length
				of responses list is equal to total number 
				of responses expected.
		"""
		return len(self._propositions) >= self._length

	def increase_score(self, value: float):
		self._score += value

	def add(self, response: Response):
		if not self.completed:
			self._propositions.append(response)

	def get_true_response(self) -> str:
		""" Returns the transition and all the responses """
		return (f"{self._transition}\n" if self._transition else '') \
			+ str(self._responses)

	def __str__(self) -> str:
		return f"\033[92m{self._question}\033[0m"


class Paper:

	def __init__(self, file_path):
		if not os.path.isfile(file_path):
			raise FileNotFoundError(
				f"This file is not found at this path: {file_path}"
			)

		_, self._name = os.path.split(file_path)
		self._content = ''
		with open(file_path, 'r', encoding='utf-8') as file:
			self._content = file.read()

		self._questions = []
		self._transitions = []
		self._responses = []
		self._ordered_res = []
		self._response_types = []
		self._parse_file()

		if len(self._questions) != len(self._responses):
			raise ValueError(
				f"Some questions have not answer."
			)

	@property
	def name(self) -> str:
		return self._name

	@property
	def content(self) -> str:
		return self._content

	def _parse_file(self):
		""" Function of file parsing """
		content_loaded = json.loads(self._content)
		if content_loaded:
			question = ''
			transition = ''
			response = ''
			response_type = ''
			responses = []
			response_types = []

			for quiz in content_loaded['paper']:
				question = quiz.get('question')
				transition = quiz.get('transition', '')
				response = quiz.get('response')
				responses = [response] if response else quiz.get('responses', [])

				response_type = quiz.get('response_type', 'txt')
				response_types = [response_type]*len(responses) if response_type \
					else quiz.get('response_types', [])

				self._questions.append(Question(question))
				self._responses.append(
					ResponsesList(responses_list=responses)
				)
				self._ordered_res.append(quiz.get('ordered', False))
				self._response_types.append(response_types)
				self._transitions.append(transition)

	def shuffle(self):
		""" Function used to shuffle questions and responses """
		index_list = list(range(len(self._questions)))
		if index_list:
			random.shuffle(index_list)
			questions = []
			responses = []
			response_types = []
			ordered_res = []
			transitions = []
			for index in index_list:
				questions.append(self._questions[index])
				responses.append(self._responses[index])
				ordered_res.append(self._ordered_res[index])
				response_types.append(self._response_types)
				transitions.append(self._transitions[index])

			self._questions.clear()
			self._responses.clear()
			self._ordered_res.clear()
			self._response_types.clear()
			self._transitions.clear()

			self._questions.extend(questions)
			self._responses.extend(responses)
			self._ordered_res.extend(ordered_res)
			self._response_types.extend(response_types)
			self._transitions.extend(transitions)

	def __len__(self) -> int:
		return len(self._questions)

	def __getitem__(self, index) -> Quiz:
		return Quiz(self._questions[index],
					  self._responses[index],
					  self._response_types[index],
					  self._transitions[index],
					  self._ordered_res[index],)

	def __str__(self) -> str:
		content = ""
		paper_content = zip(self._questions, self._responses)
		for index, (question, response) in enumerate(paper_content):
			content += "\033[94m"
			content += "Q" + str(index + 1) + ": " + str(question) + "\n"
			content += "\033[93m"
			content += "R" + str(index + 1) + ":\n" \
				+ str(response) + '\n'
			content += "\033[0m"

		return content


class Folder:

	def __init__(self, dir_path: str):
		if not os.path.isdir(dir_path):
			raise FileNotFoundError(
				f"This folder is not found at this path: {dir_path}"
			)

		self._dir_path = dir_path
		self._file_names = os.listdir(dir_path)
		_, self._name = os.path.split(dir_path)

	@property
	def name(self) -> str:
		return self._name

	def __len__(self) -> int:
		return len(self._file_names)

	def __getitem__(self, index) -> Paper:
		file_path = os.path.join(self._dir_path, self._file_names[index])
		return Paper(file_path)

	def __str__(self) -> str:
		return self._name
