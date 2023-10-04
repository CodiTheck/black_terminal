""" CODE LEARNING
"""
from __future__ import annotations

import os
from argparse import ArgumentParser

from strategy import Context, Strategy
from learning import Learning
from user import User
from folders import Folder
from console import Console


class App:

	def __init__(self):
		self.strategies_list = [
			Learning(),
		]

	def get_current_user(self) -> User:
		return User("Dr Mokira")

	def show_welcome_message(self):
		Console.print_message("+==============================================+\n")
		Console.print_message("|           WELCONE IN CODE LEARNING           |\n")
		Console.print_message("+==============================================+\n")
		Console.make_new_line()

	def show_options(self):
		Console.print_message("\t + Enter [1] To learn;\n")
		Console.print_message("\t + Enter [2] To revision;\n")
		Console.print_message("\t + Enter [3] To test my skils;\n")
		Console.print_message("\t + Enter [0] To exit.\n")
		Console.make_new_line()

	def scan_option(self) -> int:
		option = input(">_ ")
		return int(option)  # convert option to int.

	def is_available(self, selected_option: int) -> bool:
		corresponding_index = selected_option - 1
		if corresponding_index >= 0 \
			and corresponding_index < len(self.strategies_list):
			return True

	def strategy_at(self, index) -> Strategy:
		return self.strategies_list[index]

	def exec(self, args) -> int:
		""" Main function. """
		Console.clear()

		folder = Folder(args.dirpath)
		user = self.get_current_user()
		context = Context(user, folder)

		Console.clear()
		self.show_welcome_message()
		self.show_options()

		selected_option = self.scan_option()
		if selected_option != 0:
			if self.is_available(selected_option):
				corresponding_index = selected_option - 1
				context.strategy = self.strategy_at(corresponding_index)
				context.run_strategy()
				return 0
		else:
			# quit application:
			return 0


def main():
	try:
		parser = ArgumentParser(prog="CODE LEARNING")
		parser.add_argument(
			'dirpath',
			type=str,
			help="Directory path.",
		)
		args = parser.parse_args()

		app = App()
		retcode = app.exec(args)
		os.sys.exit(retcode)
	except KeyboardInterrupt:
		print("\033[91mCanceled by user.\033[0m")
		os.sys.exit(125)


if __name__ == '__main__':
	main()
