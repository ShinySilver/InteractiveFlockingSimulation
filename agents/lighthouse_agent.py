from agents.agent import Agent


class LighthouseAgent(Agent):
    def __init__(self, color, context, pos=(0, 0), focus: float = 1.0, nimbus: float = 1.0, hwidth: int = 10):
        super().__init__(context, pos, focus, nimbus)
        self.color = color
        self.id = None
        self.hwidth = hwidth

    def prepare_update(self):
        pass

    def apply_update(self):
        pass

    def render(self, client):
        if self.id is None:
            self.id = (client.create_oval(self.pos[0] - self.hwidth, self.pos[1] - self.hwidth, self.pos[0] + self.hwidth, self.pos[1] + self.hwidth,
                                          fill=self.color, outline="yellow"),
                       client.create_oval(self.pos[0] - self.nimbus, self.pos[1] - self.nimbus, self.pos[0] + self.nimbus,
                                          self.pos[1] + self.nimbus, outline="yellow"))
            return
        client.coords(self.id[0], self.pos[0] - self.hwidth, self.pos[1] - self.hwidth, self.pos[0] + self.hwidth, self.pos[1] + self.hwidth)
        client.coords(self.id[1],self.pos[0] - self.nimbus, self.pos[1] - self.nimbus, self.pos[0] + self.nimbus,
                                          self.pos[1] + self.nimbus)