import queue
import sys
import threading
import time
from collections.abc import Iterable

from agents.agent import Agent

class Simulation:
	def __init__(self, agents=[], width=400, thread_count=4):
		self.__agents = set(agents)
		self.width = width
		self.threads = []
		self.queue = queue.Queue(maxsize=300)
		for i in range(thread_count):
			self.threads+=[threading.Thread(target=self.__worker, daemon=True).start()]

	def __iadd__(self, other):
		if(isinstance(other, Simulation)):
			self.add_agents(other.get_agents())
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
		self.__agents |= agents

	def del_agents(self, agents):
		if(isinstance(agents, Agent)):
			agents = {agents}
		if(isinstance(agents, Iterable)):
			agents = set(agents)
		assert isinstance(agents, set)
		self.__agents -= agents

	def get_agents(self, types=Agent):
		return {a for a in self.__agents if isinstance(a, types)}

	def update_agent_trait(self, types, trait, new_value):
		agents = self.get_agents(types)
		# print(f"udpate_sim\n{agents}\n{type}\n{trait}\n{new_value}")
		for agent in agents:
			agent.__setattr__(trait, new_value)

	def __worker(self):
		while(True):
			agent = self.queue.get(block=True, timeout=None)
			agent.prepare_update()
			self.queue.task_done()

	def update(self):
		for agent in self.__agents:
			self.queue.put(agent)
		self.queue.join()
		for agent in self.__agents:
			agent.apply_update()
			pass

	def mainloop(self, period=0):
		t0 = time.time()
		while(True):
			self.update()
			time.sleep(0.1)
			if(period and time.time()-t0>period):
				break
