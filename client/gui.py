import tkinter as tk
from client.agent_trait_scale import AgentTraitScale
from agents.flock_agent import FlockAgent
from agents.lighthouse_agent import LighthouseAgent
from agents.green_lighthouse import GreenLighthouse
from agents.red_lighthouse import RedLighthouse
from random import random
import numpy as np

class GUI(tk.Tk):
	def __init__(self, context):
		super().__init__()

		# variables
		self.context = context
		self.sim_width = context.width #px

		self.fps = tk.IntVar(self, 30)
		self.__running = None
		self.__id_auto_render = None

		self.__sim_running = False
		self.__id_auto_sim = None
		self.tps = 20

		self.fpop = tk.IntVar(self, 40)
		self.lhpop = tk.IntVar(self, 0)

		# frames
		settings_frame = tk.Frame(self, padx=15)
		settings_frame.grid(row=0, column=0)
		flock_settings_frame = tk.LabelFrame(settings_frame, text="flock settings")
		flock_settings_frame.pack()
		field_frame = tk.Frame(self, padx=15)
		field_frame.grid(row=0, column=1)
		control_frame = tk.Frame(field_frame, pady=7)

		# all setting scales
		self.flock_settings = [
		AgentTraitScale(flock_settings_frame, context, FlockAgent, "nimbus",
				from_=0, to=200, tickinterval=50, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=10, variable=tk.DoubleVar(self, 100)),
		AgentTraitScale(flock_settings_frame, context, FlockAgent, "focus",
				from_=0, to=200, tickinterval=50, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=10, variable=tk.DoubleVar(self, 50)),
		AgentTraitScale(flock_settings_frame, context, FlockAgent, "avoidance_distance",
				from_=0, to=200, tickinterval=50, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=10, variable=tk.DoubleVar(self, 30)),
		AgentTraitScale(flock_settings_frame, context, FlockAgent, "alignment_strength",
				from_=0, to=1, tickinterval=0.5, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=0.1, variable=tk.DoubleVar(self, 0.5)),
		AgentTraitScale(flock_settings_frame, context, FlockAgent, "cohesion_strength",
				from_=0, to=1, tickinterval=0.5, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=0.1, variable=tk.DoubleVar(self, 0.3)),
		AgentTraitScale(flock_settings_frame, context, FlockAgent, "avoidance_strength",
				from_=0, to=1, tickinterval=0.5, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=0.1, variable=tk.DoubleVar(self, 0.2)),
		AgentTraitScale(flock_settings_frame, context, FlockAgent, "rotation_speed",
				from_=0, to=3, tickinterval=0.5, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=0.1, variable=tk.DoubleVar(self, 0.7))
		]
		for scale in self.flock_settings:
			scale.pack()

		# Field
		tk.Scale(field_frame, from_=0, to=30, length=self.sim_width, orient=tk.HORIZONTAL,
		 		variable=self.fps, command=self.check_wake_up, label="FPS").pack()
		self.field = tk.Canvas(field_frame, width=self.sim_width, height=self.sim_width, bg="black")
		self.field.pack()
		self.field.bind("<Button-1>", self.add_green_lighthouse)
		self.field.bind("<Button-2>", self.del_lighthouse)
		self.field.bind("<Button-3>", self.add_red_lighthouse)

		# controls
		control_frame.pack()

		tk.Scale(control_frame, from_=10, to=300, length=self.sim_width, orient=tk.HORIZONTAL,
		 		variable=self.fpop, label="FlockAgent population").grid(row=0, column=0, columnspan=2)

		tk.Button(control_frame, text="Setup", command=self.setup_sim).grid(row=2, column=0)
		self.go_stop_button = tk.Button(control_frame, text="Go", command=self.go_stop)
		self.go_stop_button.grid(row=2, column=1)

	def auto_render(self):
		self.__running = True
		self.render_all()
		fps = self.fps.get() #local copy non-atomic
		if(fps):
			self.__id_auto_render = self.after(int(1/fps*1000), self.auto_render)
		else:
			self.__running = False

	def cancel_auto_render(self):
		self.after_cancel(self.__id_auto_render)
		self.__running = None

	def check_wake_up(self, v):
		if(self.__running is not None and not self.__running):
			print(v)
			if(v != 0):
				self.__running = True
				self.auto_render()

	def render_all(self):
		for agent in self.context.get_agents():
			agent.render(self.field)

	def setup_sim(self):
		self.context.del_agents(self.context.get_agents())
		options = dict([(s.trait, float(s.get())) for s in self.flock_settings])
		print(options)
		for i in range(self.fpop.get()):
			FlockAgent(context=self.context, pos=(random()*self.sim_width, random()*self.sim_width), rotation=np.pi * 1.0 * np.random.random(), **options)
		self.auto_render()

	def go_stop(self):
		self.__sim_running = not self.__sim_running
		if(self.__sim_running):
			self.go_stop_button.configure(relief="sunken")
			self.auto_sim()
		else:
			self.go_stop_button.configure(relief="raised")
			self.after_cancel(self.__id_auto_sim)

	def auto_sim(self):
		self.context.update()
		self.__id_auto_sim = self.after(int(1/self.tps*1000), self.auto_sim)

	def __add_lighthouse(self, lhtype, pos):
		print(lhtype, pos)
		lhtype(self.context, pos, nimbus=100)

	def add_green_lighthouse(self, event):
		self.__add_lighthouse(GreenLighthouse, (event.x, event.y))

	def add_red_lighthouse(self, event):
		self.__add_lighthouse(RedLighthouse, (event.x, event.y))

	def del_lighthouse(self, event):
		lhs = self.context.get_agents(LighthouseAgent)
		for lh in lhs:
			if lh.collide_pos((event.x, event.y)):
				self.context.del_agents(lh)
				self.field.delete(*lh.id)
				self.field.update()
