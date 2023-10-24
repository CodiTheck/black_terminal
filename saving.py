import time
import datetime

from console import Console
from strategy import Strategy
from user import User
from folders import Folder


class UserSaving(Strategy):

	def _scan_file_name(self) -> str:
		print("\033[92m", end='')
		string = input(" >_ ")
		print("\033[0m", end='')
		return string

	def wait_user_press_enter(self):
		return input("Press only [ENTER] to continue ... ")

	def _get_current_time_string(self) -> str:
		current_time = time.time()
		current_time = datetime.datetime.fromtimestamp(current_time)
		return current_time
	
	def save_string(self, string: str, file_name: str):
		with open(f"{file_name}.txt", 'w', encoding='utf-8') as f:
			f.write(str(string))

	def run(self, user: User, folder: Folder):
		current_time_string = self._get_current_time_string()
		Console.clear()
		Console.print_message(f"{user}\n")
		
		Console.make_new_line()
		Console.print_message(
			"\033[93mDo you want to save this performance?\033[0m\n"
		)
		Console.print_message("Enter [n] to cancel, or ")
		character = self.wait_user_press_enter()
		if character.lower() == 'n':
			return

		Console.print_message(
			f"Enter the file name [\033[92m{current_time_string}\033[0m]:\n"
		)
		file_name = self._scan_file_name()
		if not file_name:
			file_name = current_time_string

		self.save_string(
			(
				f"USER NAME:      {user.name}\n"
				f"EXPECTED SCORE: {user.expected}\n"
				f"YOUR SCORE:     {user.score}\n"
			),
			file_name,
		)

		Console.clear()
		Console.print_message("\033[93mSaving success!\033[0m\n")
		self.wait_user_press_enter()
