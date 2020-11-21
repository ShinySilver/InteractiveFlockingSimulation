from agents.agent import Agent


class LighthouseAgent(Agent):
    def __init__(self, color, context, pos=(0, 0), focus: float = 1.0, nimbus: float = 1.0):
        super().__init__(context, pos, focus, nimbus)
        self.color = color
        self.id = None

    def prepare_update(self):
        pass

    def apply_update(self):
        pass

    def render(self, client):
        if self.id is None:
            self.id = client.create_oval(self.pos[0] - 10, self.pos[1] - 10, self.pos[0] + 10, self.pos[1] + 10, fill=self.color,
                               outline="yellow")
            return
        client.coords(self.id, self.pos[0] - 10, self.pos[1] - 10, self.pos[0] + 10, self.pos[1] + 10)