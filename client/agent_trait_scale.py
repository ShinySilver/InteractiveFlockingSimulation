import tkinter as tk

class AgentTraitScale(tk.Scale):
	def __init__(self, master, context, agent_types, trait, **kwargs):
		super().__init__(master, label=" ".join(trait.split('_')), command=self.update_trait, **kwargs)
		self.agent_types = agent_types
		self.trait = trait
		self.context = context

	def update_trait(self, new_value):
		self.context.update_agent_trait(self.agent_types, self.trait, new_value)
