from abc import ABC
import numpy as np


class Agent(ABC):
    def __init__(self, pos=(0,0,0), focus:float=1.0, nimbus:float=1.0):
        """

        Parameters
        ----------
        focus @optional is the can-see distance modifier
        nimbus @optional is the can-be-seen distance modifier
        """
        self.squared_focus = focus**2
        self.squared_nimbus = nimbus**2
        self.pos = np.array(pos)

    def can_focus(self, agent):
        return np.sum(self.pos*self.pos-agent._pos*agent._pos)*self.squared_focus<1.0

    def in_nimbus_of(self, agent):
        return np.sum(self.pos*self.pos-agent._pos*agent._pos)*agent.squared_nimbus<1.0

    @abs
    def render(self):
        raise NotImplementedError()

    @abs
    def update(self):
        raise NotImplementedError()