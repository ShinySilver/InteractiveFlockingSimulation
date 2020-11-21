import tkinter as tk
from client.agent_trait_scale import AgentTraitScale
from agents.flock_agent import FlockAgent

class GUI(tk.Tk):
	def __init__(self, context, width=400):
		super().__init__()


		self.context = context
		self.sim_width = width #px

		self.fps = tk.IntVar(self, 2)
		self.__running = None
		self.__id_auto_render = None

		settings_frame = tk.Frame(self, padx=15)
		settings_frame.grid(row=0, column=0)
		flock_settings_frame = tk.LabelFrame(settings_frame, text="flock settings")
		flock_settings_frame.pack()
		field_frame = tk.Frame(self, padx=15)
		field_frame.grid(row=0, column=1)

		AgentTraitScale(flock_settings_frame, context, FlockAgent, "avoidance_distance",
				from_=0, to=2, tickinterval=0.5, orient=tk.HORIZONTAL,
				length=self.sim_width//2, resolution=0.1).pack()

		# tk.Button(self, text="debug", command=self.auto_render).grid(row=1, column=0, columnspan=2)


		tk.Label(field_frame, text="FPS").pack()
		tk.Scale(field_frame, from_=0, to=30, length=self.sim_width, orient=tk.HORIZONTAL,
		 		variable=self.fps, command=self.check_wake_up).pack()
		self.field = tk.Canvas(field_frame, width=self.sim_width, height=self.sim_width, bg="black")
		self.field.pack()

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

	def cp_(self, pos):
		return (pos[0]%self.width, pos[1]%self.width)
