import numpy as np


class Agent:
    def __init__(self, context, pos=(0, 0), focus: float = 50.0, nimbus: float = 100.0):
        """
        Parameters
        ----------
        focus @optional is the can-see distance modifier
        nimbus @optional is the can-be-seen distance modifier
        """
        self.context = context
        self.context += self
        self.focus = focus
        self.nimbus = nimbus
        self.pos = np.array(pos)

    def distance_to(self, agent):
        self.pos %= self.context.width
        return np.sqrt(np.sum(np.power((agent.pos - self.pos)%self.context.width, (2, 2))))

    def can_focus(self, agent, cached_distance=None):
        if cached_distance is not None:
            return cached_distance / self.focus < 1.0
        self.pos %= self.context.width
        return np.sqrt(np.sum(np.power((agent.pos - self.pos)%self.context.width, (2, 2)))) / self.focus < 1.0

    def in_nimbus_of(self, agent, cached_distance=None):
        if cached_distance is not None:
            return cached_distance / agent.nimbus < 1.0
        self.pos %= self.context.width
        return np.sqrt(np.sum(np.power((agent.pos - self.pos)%self.context.width, (2, 2)))) / agent.nimbus < 1.0

    def prepare_update(self):
        raise NotImplementedError()

    def apply_update(self):
        raise NotImplementedError()

    def render(self, client):
        raise NotImplementedError()
