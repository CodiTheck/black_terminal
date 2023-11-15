from strategy import Strategy
from user import User
from folders import Folder, Quiz
from controller import Corrector
from console import Console
from utils import inputf


class Learning(Strategy):

	def __init__(self):
		self._corrector = Corrector()

	def _scan_response(self, response_type: str = 'txt') -> str:
		print("\033[97m", end='')
		string = input(" >_ ")
		print("\033[0m", end='')
		# string = inputf()
		return string

	def _wait_user_press_enter(self):
		return input(" Press only [ENTER] to start the quiz... ")

	def _ask_user(self, message: str) -> str:
		return input(message)

	def run(self, user: User, folder: Folder):
		Console.clear()

		for index in range(len(folder)):
			Console.clear()
			paper = folder[index]

			paper.shuffle()

			Console.print_message(f"{paper}\n")
			Console.make_new_line()

			character = self._wait_user_press_enter()
			if character != '':
				return

			for index in range(len(paper)):
				Console.clear()
				Console.print_message(f"{user}\n")
				Console.print_message(
					f"\t \033[4mFolder:\033[0m \033[93m{folder.name.upper()}\033[0m\n"
				)
				Console.print_message(
					f"\t \033[4mPaper: \033[0m \033[93m{paper.name.upper()}\033[0m\n"
				)
				Console.make_new_line()

				quiz = paper[index]
				# self._corrector.true_responses = quiz.responses
				user.increase_expected(quiz.expected)

				# quiz = Quiz(question, nb_responses=len(true_responses))
				Console.print_message(" \033[4mQUESTION:\033[0m\n")
				Console.print_message(f"\033[94m{quiz}\033[0m\n")
				Console.make_new_line()

				Console.print_message("\033[97m \033[4mYour responses:\033[0m\n")

				res_type_index = 0
				while not quiz.completed:
					response = self._scan_response(quiz.response_types[res_type_index])
					user.answer(quiz, response)
					res_type_index += 1

				self._corrector.correct(quiz)
				user.increase_score(quiz.score)

				if quiz.accuracy_score < 100.0:
					# Console.make_new_line()
					# Console.print_message("\033[92m \033[4mANALYSIS\033[0m\n")
					# analysis_iterator = self._corrector.get_analysis()
					# for message in analysis_iterator:
					#		Console.print_message(f"{message} ")

					Console.make_new_line()
					Console.print_message("\033[93m \033[4mTRUE RESPONSES\033[0m\n")
					Console.print_message(f"\033[93m{quiz.responses}\033[0m")
				else:
					Console.print_message(
						f"\033[92m Congratulation {user.name}!\033[0m\n"
					)

				Console.make_new_line()
				Console.print_message(
					f" You optained \033[5m{quiz.accuracy_score:.2f} \033[0m%\n"
				)

				character = self._wait_user_press_enter()
				if character != '':
					break

				self._corrector.reset()

			# Console.make_new_line()
			# Console.print_message(
			# 	f"Your score is: \033[93m{user.score}\033[0m/{len(paper)}\n"
			# )
