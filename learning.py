from strategy import Strategy
from user import User
from folders import Folder


class Learning(Strategy):

	def run(self, user: User, folder: Folder):
		print(f"{user}")
		print(f"Folder name : {folder.name}")

		corrector = Corrector()
		for index in range(len(folder)):
			paper = folder[index]
			clear_console()
			print(paper)

			for index in range(len(paper)):
				quiz = paper[index]
				while not quiz.completed:
					print(quiz)
					response = input(">_ ")

					corrector.controle(response, quiz)
					if corrector.valids():
						user.increase_score(quiz.getscore())

			print(f"Your score is: \033[93m{user.score}\033[0m")
