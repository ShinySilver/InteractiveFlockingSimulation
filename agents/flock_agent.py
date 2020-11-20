from agents.agent import Agent


class FlockAgent(Agent):
    def __init__(self,
                 avoidance_distance: float = 1.5,
                 alignment_strength: float = 0.5,
                 cohesion_strength: float = 0.3,
                 avoidance_strength: float = 0.2,
                 speed: float = 1.0,
                 rotation_speed: float = 10.0,
                 pos=(0, 0, 0),
                 focus: float = 1.0,
                 nimbus: float = 1.0):
        """
        Parameters
        ----------
        avoidance_distance is the minimum distance before triggering avoidance mechanism override
        alignment_strength is the alignment behaviour modifier
        cohesion_strength is the cohesion behaviour modifier
        avoidance_strength is the avoidance behaviour modifier
        speed is the distance increment per tick
        rotation_speed is the rotation increment per tick
        pos @optional is the (x, y) initial position
        focus @optional is the can-see distance modifier
        nimbus @optional is the can-be-seen distance modifier
        """
        Agent(self, pos, focus, nimbus)

    def prepare_update(self):
        pass

    def apply_update(self):
        pass

    def render(self, client):
        pass
