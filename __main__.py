from simulation.simulation import Simulation
from agents.flock_agent import FlockAgent

if __name__ == '__main__':
	s = Simulation()
	a = FlockAgent(s)
	print(s.agents)

	s2 = Simulation()
	a2 = FlockAgent(s2)
	print(s.agents)



	s2+=s
	print(s2.agents)
