import numpy as np


class Agent:
    def __init__(self, context, pos=(0, 0), focus: float = 1.0, nimbus: float = 1.0):
        """
        Parameters
        ----------
        focus @optional is the can-see distance modifier
        nimbus @optional is the can-be-seen distance modifier
        """
        self.context = context
        self.context.agents+=[self]
        self.squared_focus = focus ** 2
        self.squared_nimbus = nimbus ** 2
        self.pos = np.array(pos)

    def squared_distance_to(self, agent):
        return np.sum(self.pos * self.pos - agent._pos * agent._pos)

    def can_focus(self, agent, cached_squared_distance=None):
        if cached_squared_distance is not None:
            return cached_squared_distance * self.squared_focus < 1.0
        return np.sum(self.pos * self.pos - agent._pos * agent._pos) * self.squared_focus < 1.0

    def in_nimbus_of(self, agent, cached_squared_distance=None):
        if cached_squared_distance is not None:
            return cached_squared_distance * agent.squared_nimbus < 1.0
        return np.sum(self.pos * self.pos - agent._pos * agent._pos) * agent.squared_nimbus < 1.0

    def prepare_update(self):
        raise NotImplementedError()

    def apply_update(self):
        raise NotImplementedError()

    def render(self, client):
        raise NotImplementedError()
