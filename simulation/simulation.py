import time
from collections.abc import Iterable

from agents.agent import Agent

class Simulation:
	def __init__(self, agents=[]):
		self.agents = set(agents)


	def __iadd__(self, other):
		if(isinstance(other, Simulation)):
			self.add_agents(other.agents)
		else:
			if not (isinstance(other, Agent) or isinstance(other, Iterable)):
				raise TypeError("Not a simulation or Agent(s)")
			self.add_agents(other)
		return self

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
		t0 = time.time()
		while(True):
			self.update()
			time.sleep(0.1)
			if(period and time.time()-t0>period):
				break
