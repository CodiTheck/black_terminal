from __future__ import annotations
from abc import ABC, abstractmethod

from user import User
from folders import Folder


class Strategy(ABC):

	@abstractmethod
	def run(self, user: User, folder: Folder):
		pass


class Context:

	def __init__(self, user: User, folder: Folder, strategy: Strategy = None):
		self._user = user
		self._folder = folder
		self._strategy = strategy

	@property
	def strategy(self) -> Strategy:
		return self._strategy

	@strategy.setter
	def strategy(self, strategy: Strategy):
		self._strategy = strategy

	def run_strategy(self):
		self._strategy.run(self._user, self._folder)
