from agents.agent import Agent
from agents.lighthouse_agent import LighthouseAgent


class RedLighthouse(LighthouseAgent):
    def __init__(self, context, pos=(0, 0), focus: float = 1.0, nimbus: float = 1.0):
        super().__init__(context, pos, focus, nimbus)

    def render(self, client):
        # Where is ya red'ol lighthouse png?
        pass