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
        self.pos = self._clamp(self.pos, 0, self.context.width)
        return np.sqrt(np.sum(np.power(self._shortest(agent.pos - self.pos, 0, self.context.width), 2)))

    def can_focus(self, agent, cached_distance=None):
        if cached_distance is not None:
            return cached_distance / self.focus < 1.0
        self.pos = self._clamp(self.pos, 0, self.context.width)
        return np.sqrt(np.sum(np.power(self._shortest(agent.pos - self.pos, 0, self.context.width),
                                       2))) / self.focus < 1.0

    def in_nimbus_of(self, agent, cached_distance=None):
        if cached_distance is not None:
            return cached_distance / agent.nimbus < 1.0
        self.pos = self._clamp(self.pos, 0, self.context.width)
        return np.sqrt(np.sum(np.power(self._shortest(agent.pos - self.pos, 0, self.context.width),
                                       2))) / agent.nimbus < 1.0

    def prepare_update(self):
        raise NotImplementedError()

    def apply_update(self):
        raise NotImplementedError()

    def render(self, client):
        raise NotImplementedError()

    def _clamp(self, x, x0, x1):
        for i in range(len(x)):
            while x[i]<x0:
                x[i]+=x1-x0
            while x[i]>x1:
                x[i]-=x1-x0
        return x

    def _shortest(self, x, x0, x1):
        for i in range(len(x)):
            if abs(x[i]-(x1-x0)/2.0)<x[i]:
                x[i] = abs(x[i]-(x1-x0)/2.0)
            if abs(x[i]+(x1-x0)/2.0)<x[i]:
                x[i] = abs(x[i]+(x1-x0)/2.0)
        return x

