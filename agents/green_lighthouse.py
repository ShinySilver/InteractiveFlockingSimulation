from agents.agent import Agent
from agents.lighthouse_agent import LighthouseAgent


class GreenLighthouse(LighthouseAgent):
    def __init__(self, context, pos=(0, 0), nimbus: float = 1.0):
        super().__init__("green", context=context, pos=pos, nimbus=nimbus)