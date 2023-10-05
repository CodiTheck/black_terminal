from strategy import Strategy
from user import User
from folders import Folder, Quiz
from controller import Corrector
from console import Console


class Learning(Strategy):

	def _scan_response(self) -> str:
		print("\033[97m", end='')
		string = input(">_ ")
		print("\033[0m", end='')
		return string

	def _wait_user_press_enter(self):
		return input("Press only [ENTER] to start the quiz... ")

	def run(self, user: User, folder: Folder):
		Console.clear()

		corrector = Corrector()
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
					f"\t \033[4mPaper:\033[0m \033[93m{paper.name.upper()}\033[0m\n"
				)
				Console.make_new_line()

				question, true_responses = paper[index]
				corrector.true_responses = true_responses

				quiz = Quiz(question, nb_responses=len(true_responses))
				Console.print_message("\033[4mQUESTION:\033[0m\n")
				Console.print_message(f"\033[94m{question}\033[0m\n")
				Console.make_new_line()

				Console.print_message("\033[97m\033[4mYour responses:\033[0m\n")

				while not quiz.completed:
					response = self._scan_response()
					user.answer(quiz, response)

				corrector.correct(quiz)
				user.increase_score(quiz.score)

				if quiz.accuracy_score < 100.0:
					Console.make_new_line()
					Console.print_message("\033[92m\033[4mANALYSIS\033[0m\n")
					Console.print_message(corrector.get_analyse(quiz))

					Console.make_new_line()
					Console.print_message("\033[93m\033[4mTRUE RESPONSES\033[0m\n")
					Console.print_message(f"\033[93m{true_responses}\033[0m")
				else:
					Console.print_message(f"\033[92mCongratulation {user.name}!\033[0m\n")

				Console.make_new_line()
				Console.print_message(
					f"You optained \033[5m{quiz.accuracy_score:.2f} \033[0m%\n"
				)

				character = self._wait_user_press_enter()
				if character != '':
					break

				# corrector.reset()

			# Console.make_new_line()
			# Console.print_message(
			# 	f"Your score is: \033[93m{user.score}\033[0m/{len(paper)}\n"
			# )
