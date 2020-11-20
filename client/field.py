import tkinter as tk

class Field(tk.Canvas):
	def __init__(self, master, context=None, width=400, height=400,  **kwargs):
		super().__init__(master=master, width=width, height=height, **kwargs)

		self.context = context
		self.height = height
		self.width = width

	def render_all(self):
		for agent in self.context.agents:
			agent.render(self)

	def cp_(self, pos):
		return (pos[0]%width, pos[1]%height)
