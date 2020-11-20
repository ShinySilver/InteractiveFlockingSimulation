import time
from collections.abc import Iterable

from agents.agent import Agent

class Simulation:
	def __init__(self, agents=set()):
		self.agents = agents
		self.__running = False

	def __iadd__(self, other):
		if(isinstance(other, Simulation)):
			# print(self.agents)
			# print(other.agents)
			self.add_agents(other.agents)
			# print(self.agents)
			# print(other.agents)


		else:
			if not (isinstance(other, Agent) or isinstance(other, Iterable)):
				raise TypeError("Not a simulation or Agent(s)")
			self.add_agents(other)

	def add_agents(self, agents):
		if(isinstance(agents, Agent)):
			agents = {agents}
		if(isinstance(agents, Iterable)):
			agents = set(agents)
		assert isinstance(agents, set)
		self.agents |= agents

	def del_agents(self, agents):
		if(isinstance(agents, Agent)):
			agents = {agents}
		if(isinstance(agents, Iterable)):
			agents = set(agents)
		assert isinstance(agents, set)
		self.agents - agents

	def update(self):
		for agent in self.agents:
			agent.prepare_update()
		for agent in self.agents:
			agent.apply_update()

	def mainloop(self, period=0):
		while(self.__running):
			self.update()
			time.sleep(0.1)
