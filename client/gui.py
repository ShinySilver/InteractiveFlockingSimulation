import tkinter as tk
from client.agent_trait_scale import AgentTraitScale
from client.field import Field
from agents.flock_agent import FlockAgent

class GUI(tk.Tk):
	def __init__(self, context, **kwargs):
		super().__init__(**kwargs)

		scales_frame = tk.Frame(self)
		scales_frame.grid(row=0, column=0)
		field_frame = tk.Frame(self)
		field_frame.grid(row=0, column=1)

		AgentTraitScale(scales_frame, context, FlockAgent, "avoidance_distance", from_=0, to=2, tickinterval=0.1, orient=tk.HORIZONTAL).pack()


		tk.Button(self, text="debug", command=lambda:print(list(context.get_agents())[0].avoidance_distance)).grid(row=1, column=0, columnspan=2)

		self.field = Field(field_frame, context, bg="black")
		self.field.pack()
