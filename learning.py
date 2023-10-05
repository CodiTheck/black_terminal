from strategy import Strategy
from user import User
from folders import Folder, Quiz
from controller import Corrector
from console import Console


class Learning(Strategy):

	def _scan_response(self) -> str:
		string = input(">_ ")
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
				Console.print_message(f"Folder name : {folder.name}\n")

				question, true_responses = paper[index]
				corrector.true_responses = true_responses

				quiz = Quiz(question, nb_responses=len(true_responses))
				Console.print_message(f"\033[94m{question}\033[0m\n")
				Console.make_new_line()

				while not quiz.completed:
					response = self._scan_response()
					user.answer(quiz, response)

				corrector.correct(quiz)
				user.increase_score(quiz.score)

				if quiz.accuracy_score < 100.0:
					Console.make_new_line()
					Console.print_message(corrector.get_analyse(quiz))

					Console.make_new_line()
					Console.print_message(f"\033[93m{true_responses}\033[0m")
				else:
					Console.print_message(f"\033[92mCongratulation {user.name}!\033[0m\n")

				Console.make_new_line()
				Console.print_message(
					f"You optained {quiz.accuracy_score:.2f} %\n"
				)

				character = self._wait_user_press_enter()
				if character != '':
					break

				# corrector.reset()

			Console.make_new_line()
			Console.print_message(
				f"Your score is: \033[93m{user.score}\033[0m/{len(paper)}\n"
			)
