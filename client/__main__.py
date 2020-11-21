import tkinter as tk
from client.gui import GUI
from simulation.simulation import Simulation
from agents.flock_agent import FlockAgent

if __name__ == '__main__':
	sim = Simulation()
	for i in range(10):
		FlockAgent(sim)
	ui = GUI(sim)
	ui.mainloop()
