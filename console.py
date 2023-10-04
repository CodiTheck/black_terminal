import os
import time


class Console:
	DELAY = 0.005

	@classmethod
	def clear(cls):
		if os.sys.platform != 'nt':
			os.system('clear')
		else:
			os.system('cls')

	@classmethod
	def make_new_line(cls):
		print("\n")

	@classmethod
	def print_message(cls, message: str):
		for character in message:
			print(character, end='', flush=True)
			time.sleep(cls.DELAY)
