from agents.agent import Agent

class Simulation:
	def __init__(self, agents):
		self.__agents = agents

	def add_agents(self, agents):
		if(isinstance(agents, Agent)):
			agents = [agents]
		assert isinstance(agents, list)
		self.__agents += agents

	
