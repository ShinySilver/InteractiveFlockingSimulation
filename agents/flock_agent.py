from agents.agent import Agent


class FlockAgent(Agent):
    def __init__(self,
                 context,
                 avoidance_distance: float = 2.0,
                 alignment_strength: float = 0.5,
                 cohesion_strength: float = 0.3,
                 avoidance_strength: float = 0.2,
                 pos=(0, 0),
                 speed: float = 0.5,
                 rotation: float = 0.0,
                 rotation_speed: float = 3.0,
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
        super(context, pos, focus, nimbus)
        self.avoidance_distance = avoidance_distance
        self.alignment_strength = alignment_strength
        self.cohesion_strength = cohesion_strength
        self.avoidance_strength = avoidance_strength
        self.next_pos = pos
        self.rotation = rotation
        self.rotation_speed = rotation_speed

    def prepare_update(self):
        avoidance = (0, 0, 0)  # x, y, count
        alignement = (0, 0, 0)
        cohesion = (0, 0, 0)
        cache = 0.0
        for agent in self.context.agents:
            cache = self.squared_distance_to(agent)

    def apply_update(self):
        self.pos = self.next_pos
        self.rotation = self.next_rotation

    def render(self, client):
        pass
