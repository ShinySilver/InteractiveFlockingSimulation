
class IAgent:
    def __init__(self, pos=(0,0,0), focus:float=1.0, nimbus:float=1.0):
        """

        Parameters
        ----------
        focus @optional is the can-see distance modifier
        nimbus @optional is the can-be-seen distance modifier
        """
        self._focus = focus
        self._nimbus = nimbus
        self._pos = pos

    def can_focus(self, agent):
        return abs(self._pos-agent.pos)

    

    def render(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()