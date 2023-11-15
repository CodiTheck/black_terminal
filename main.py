""" BLACK TERMINAL
"""
from __future__ import annotations

import os
import time
import datetime
from argparse import ArgumentParser

from strategy import Context, Strategy
from learning import Learning
from saving import UserSaving
from user import User
from folders import Folder
from console import Console


class App:

	def __init__(self):
		self.strategies = {
			'l': Learning(),
			's': UserSaving(),
		}

	def get_current_user(self) -> User:
		return User("Dr Mokira")

	def show_welcome_message(self):
		Console.print_message("\033[92m")
		Console.print_message(" +==============================================+\n")
		Console.print_message(" |           WELCONE IN BLACK TERMINAL          |\n")
		Console.print_message(" +==============================================+\n")
		Console.print_message("\033[0m")
		Console.make_new_line()

	def show_options(self):
		Console.print_message("\t + Enter [l] To learn;\n")
		Console.print_message("\t - Enter [r] To revision;\n")
		Console.print_message("\t - Enter [t] To test my skils;\n")
		Console.print_message("\t + Enter [s] To save performances;\n")
		Console.print_message("\t + Enter [q] To exit.\n")
		Console.make_new_line()

	def show(self, obj):
		Console.print_message(f"{obj}\n")

	def scan_option(self) -> int:
		option = ''
		while not option:
			option = input(" >_ ")

		return option

	def wait_user_press_enter(self):
		return input("Press only [ENTER] to continue ... ")

	def is_available(self, selected_option: str) -> bool:
		if selected_option in self.strategies:
			return True

	def strategy_at(self, key: str) -> Strategy:
		return self.strategies[key]

	def save_string(self, string):
		current_time = time.time()
		current_time = datetime.datetime.fromtimestamp(current_time)
		with open(f"{current_time}.txt", 'w', encoding='utf-8') as f:
			f.write(str(string))

	def exec(self, args) -> int:
		""" Main function. """
		Console.clear()

		folder = Folder(args.dirpath)
		user = self.get_current_user()
		context = Context(user, folder)

		while True:
			Console.clear()
			self.show_welcome_message()
			self.show(user)
			self.show_options()

			selected_option = self.scan_option()
			if selected_option != 'q':
				if self.is_available(selected_option):
					context.strategy = self.strategy_at(selected_option)
					context.run_strategy()
				else:
					Console.make_new_line()
					Console.print_message(
						"\033[93mThis option is not available yet. Coming soon!\n\033[0m"
					)
					self.wait_user_press_enter()
			else:
				# quit application:
				return 0


def main():
	try:
		print("Program loading into memory ...")
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
