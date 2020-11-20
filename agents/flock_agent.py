from agents.agent import Agent
import numpy as np


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
        super().__init__(context, pos, focus, nimbus)
        self.avoidance_distance = avoidance_distance
        self.alignment_strength = alignment_strength
        self.cohesion_strength = cohesion_strength
        self.avoidance_strength = avoidance_strength
        self.speed = speed
        self.rotation = rotation
        self.rotation_speed = rotation_speed

        self.direction = np.array((np.cos(self.rotation),np.sin(self.rotation)))
        self.next_direction = self.direction.copy()

    def prepare_update(self):
        avoidance = [0, 0, 0]  # x, y, count
        alignment = [0, 0, 0]
        cohesion = [0, 0, 0]
        cache1, cache2 = 0.0, 0.0
        for agent in self.context.get_agents():
            if agent is self:
                continue
            cache1 = self.distance_to(agent)
            if cache1 != 0 and self.in_nimbus_of(agent, cache1):
                cache2 = (agent.pos - self.pos) / cache1
                cohesion[:2] += cache2
                cohesion[2] += 1
                if cache1 <= self.avoidance_distance:
                    avoidance[:2] += cache2 * -1.0
                    avoidance[2] += 1
                if self.can_focus(agent, cache1):
                    alignment[:2] += cache2
                    alignment[2] += 1
        if avoidance[2] + alignment[2] + cohesion[2] != 0:
            self.next_direction = [avoidance[i] / avoidance[2] * self.avoidance_strength
                      + alignment[i] / alignment[2] * self.alignment_strength
                      + cohesion[i] / cohesion[2] * self.cohesion_strength for i in [0, 1]]

    def apply_update(self):
        if(self.direction[0]*self.next_direction[0]-self.direction[1]*self.next_direction[1]>0):
            self.rotation += self.rotation_speed
        else:
            self.rotation -= self.rotation_speed
        self.pos = np.add(self.pos, (np.cos(self.rotation)*self.speed,np.sin(self.rotation)*self.speed))

    def render(self, client):
        pass