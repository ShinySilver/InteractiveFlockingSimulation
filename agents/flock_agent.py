from agents.agent import Agent
import numpy as np

from agents.lighthouse_agent import LighthouseAgent


class FlockAgent(Agent):
    def __init__(self,
                 context,
                 avoidance_distance: float = 20.0,
                 alignment_strength: float = 0.5,
                 cohesion_strength: float = 0.3,
                 avoidance_strength: float = 0.2,
                 pos=(0, 0),
                 speed: float = 10.0,
                 rotation: float = 0.0,
                 rotation_speed: float = 2.0,
                 focus: float = 50.0,
                 nimbus: float = 100.0):
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

        # TODO: Add modifier balancing / normalization

        self.direction = np.array((np.cos(self.rotation), np.sin(self.rotation)))
        self.next_direction = self.direction.copy()

        self.id = None

    def prepare_update(self):
        avoidance = [0, 0, 0]  # x, y, count
        alignment = [0, 0, 0]
        cohesion = [0, 0, 0]
        distance, relpos = 0.0, 0.0

        # Flock behaviour handling
        for agent in self.context.get_agents(FlockAgent):
            if agent is self:
                continue
            distance = self.distance_to(agent)
            if self.in_nimbus_of(agent, distance):
                if distance != 0:
                    relpos = (agent.pos - self.pos) / distance
                else:
                    relpos = (0,0)
                cohesion[0] = cohesion[0] + relpos[0]
                cohesion[1] = cohesion[1] + relpos[1]
                cohesion[2] += 1
                if self.can_focus(agent, distance):
                    alignment[0] = alignment[0] + relpos[0]
                    alignment[1] = alignment[1] + relpos[1]
                    alignment[2] += 1
                if distance <= self.avoidance_distance:
                    avoidance[0] = avoidance[0] + relpos[0] * -1
                    avoidance[1] = avoidance[1] + relpos[1] * -1
                    avoidance[2] += 1
        if avoidance[2] + alignment[2] + cohesion[2] != 0:
            tmp = (avoidance, alignment, cohesion)
            tmp2 = (self.avoidance_strength, self.alignment_strength, self.cohesion_strength)
            self.next_direction = [np.sum([tmp[j][i] / tmp[j][2] * tmp2[j] for j in range(3) if tmp[j][2] > 0]) for i in
                                   range(2)]

        # Lighthouse behaviour
        for agent in self.context.get_agents(LighthouseAgent):
            # if in nimbus
            # go toward left/right
            # if in focus
            # avoidance
            pass

    def apply_update(self):
        vector_1 = self.direction.copy()
        vector_2 = self.next_direction.copy()

        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)

        angle1 = np.arccos(unit_vector_1[0])
        angle2 = np.arccos(unit_vector_2[0])
        angle = (angle2-angle1)

        if(abs(angle)<self.rotation_speed):
            self.rotation = angle2
        elif angle>0:
            self.rotation += self.rotation_speed
        else:
            self.rotation -= self.rotation_speed

        self.direction = self.next_direction
        delta = (np.cos(self.rotation) * self.speed, np.sin(self.rotation) * self.speed)
        self.pos = self.pos + delta


    def render(self, client):
        if self.id is None:
            self.id = client.create_oval(self.pos[0] - 5, self.pos[1] - 5, self.pos[0] + 5, self.pos[1] + 5, fill="blue",
                               outline="white")
            return
        client.coords(self.id, self.pos[0] - 5, self.pos[1] - 5, self.pos[0] + 5, self.pos[1] + 5)
