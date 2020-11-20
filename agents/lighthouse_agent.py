from agents.agent import Agent


class LighthouseAgent(Agent):
    def __init__(self, context, pos=(0, 0), focus: float = 1.0, nimbus: float = 1.0):
        super().__init__(context, pos, focus, nimbus)

    def prepare_update(self):
        pass

    def apply_update(self):
        pass

    def render(self, client):
        pass
