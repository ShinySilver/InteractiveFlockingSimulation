import tkinter as tk
from client.gui import GUI
from simulation.simulation import Simulation
import cProfile

if __name__ == '__main__':
	sim = Simulation()
	ui = GUI(sim)
	ui.title("Interactive Multi-Agents Flocking Simulation")
	pr = cProfile.Profile()
	pr.enable()
	ui.mainloop()
	pr.disable()
	pr.dump_stats('stats.cprofile')
