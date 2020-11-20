from simulation.simulation import Simulation
from agents.flock_agent import FlockAgent

if __name__ == '__main__':
	s = Simulation()
	a = FlockAgent(s)

	s2 = Simulation()
	a2 = FlockAgent(s2)

	s2+=s

	s2.update() #1
	s2.update() #2
	# s2.mainloop()
