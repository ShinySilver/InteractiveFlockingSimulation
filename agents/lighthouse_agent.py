from agents.agent import Agent


class LighthouseAgent(Agent):
    def __init__(self, pos=(0, 0), focus: float = 1.0, nimbus: float = 1.0):
        Agent(self, pos, focus, nimbus)

    def prepare_update(self):
        pass

    def apply_update(self):
        pass

    def render(self, client):
        pass
