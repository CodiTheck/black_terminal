""" CODE LEARNING
"""
from __future__ import annotations

import os
from argparse import ArgumentParser

from strategy import Context
from learning import Learning


class App:

	def __init__(self):
		self.strategies = [
			Lea

	def exec(self, args) -> int:
		""" Main function. """
		self.clear_console()

		print("+===========================================================+")
		print("|              WELCONE IN CODE LEARNING                     |")
		print("+===========================================================+")
		print("\n")

		print("\t + Enter [1] To learn;")
		print("\t + Enter [2] To revision;")
		print("\t + Enter [3] To test my skils;")
		print("\t + Enter [0] To exit.")
		print("\n")

		option = input(">_ ")

		if option == 1:
			# run learning process:

		elif option == 2:
			# run revision process:

		elif option == 3:
			# run skills testing:

		else:
			# quit application:
			return 0


def main():
	try:
		parser = ArgumentParser(prog="CODE LEARNING")
		parser.add_argument(
			'--dirpath',
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
