import tkinter as tk

class AgentTraitScale(tk.Frame):
	def __init__(self, master, context, agent_types, trait, **kwargs):
		super().__init__(master)
		self.agent_types = agent_types
		self.trait = trait
		self.context = context
		self.label = tk.Label(self, text=self.trait)
		self.label.pack()
		self.scale = tk.Scale(self, command=self.update_trait, **kwargs)
		self.scale.pack()

	def update_trait(self, new_value):
		self.context.update_agent_trait(self.agent_types, self.trait, new_value)
